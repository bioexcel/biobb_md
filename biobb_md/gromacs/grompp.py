#!/usr/bin/env python3

"""Module containing the Grompp class and the command line interface."""
import os
import argparse
import shutil
from pathlib import Path
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError


class Grompp:
    """
    | biobb_md.gromacs.grompp Grompp
    | Wrapper of the `GROMACS grompp <http://manual.gromacs.org/current/onlinehelp/gmx-grompp.html>`_ module.
    | The GROMACS preprocessor module needs to be fed with the input system and the dynamics parameters to create a portable binary run input file TPR. The dynamics parameters are specified in the mdp section of the configuration YAML file. The parameter names and defaults are the same as the ones in the `official MDP specification <http://manual.gromacs.org/current/user-guide/mdp-options.html>`_.

    Args:
        input_gro_path (str): Path to the input GROMACS structure GRO file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.gro>`_. Accepted formats: gro (edam:format_2330).
        input_top_zip_path (str): Path to the input GROMACS topology TOP and ITP files in zip format. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.zip>`_. Accepted formats: zip (edam:format_3987).
        output_tpr_path (str): Path to the output portable binary run file TPR. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_grompp.tpr>`_. Accepted formats: tpr (edam:format_2333).
        input_cpt_path (str) (Optional): Path to the input GROMACS checkpoint file CPT. File type: input. Accepted formats: cpt (edam:format_2333).
        input_ndx_path (str) (Optional): Path to the input GROMACS index files NDX. File type: input. Accepted formats: ndx (edam:format_2330).
        input_mdp_path (str) (Optional): Path of the input GROMACS `MDP file <http://manual.gromacs.org/current/user-guide/mdp-options.html>`_. File type: input. Accepted formats: mdp (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **mdp** (*dict*) - (defaults dict) MDP options specification. (Used if *input_mdp_path* is None)
                * **type** (*str*) - ("minimization") Default options for the mdp file. Each creates a different mdp file. Values: `minimization <https://biobb-md.readthedocs.io/en/latest/_static/mdp/minimization.mdp>`_ (Creates a minimization), `nvt <https://biobb-md.readthedocs.io/en/latest/_static/mdp/nvt.mdp>`_ (Creates a nvt), `npt <https://biobb-md.readthedocs.io/en/latest/_static/mdp/npt.mdp>`_ (Creates a npt), `free <https://biobb-md.readthedocs.io/en/latest/_static/mdp/free.mdp>`_ (Creates a free MD), index (Creates an empty mdp file).
            * **maxwarn** (*int*) - (10) [0-1000|1] Maximum number of allowed warnings.
            * **gmx_lib** (*str*) - (None) Path set GROMACS GMXLIB environment variable.
            * **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*string*) - (None)  Path to the binary executable of your container.
            * **container_image** (*string*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*string*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*string*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*string*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*string*) - ("/bin/bash") Path to the binary executable of the container shell.

    Info:
        * wrapped_software:
            * name: GROMACS Grompp
            * version: >5.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl


    """

    def __init__(self, input_gro_path: str, input_top_zip_path: str, output_tpr_path: str,
                 input_cpt_path: str = None, input_ndx_path: str = None, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {"input_gro_path": input_gro_path, "input_cpt_path": input_cpt_path, "input_ndx_path": input_ndx_path},
            "out": {"output_tpr_path": output_tpr_path}
        }
        # Should not be copied inside container
        self.input_top_zip_path = input_top_zip_path

        # Properties specific for BB
        self.input_mdp_path = properties.get('input_mdp_path', None)
        self.output_mdp_path = properties.get('output_mdp_path', 'grompp.mdp')
        self.output_top_path = properties.get('output_top_path', 'grompp.top')
        #TODO REVIEW: When select is implemented.
        self.maxwarn = str(properties.get('maxwarn', 10))
        self.mdp = {k: str(v) for k, v in properties.get('mdp', dict()).items()}
        #TODO REVIEW:  this two attributes
        self.nsteps = ''
        self.dt = ''

        # container Specific
        self.container_path = properties.get('container_path')
        self.container_image = properties.get('container_image', 'gromacs/gromacs:latest')
        self.container_volume_path = properties.get('container_volume_path', '/data')
        self.container_working_dir = properties.get('container_working_dir')
        self.container_user_id = properties.get('container_user_id')
        self.container_shell_path = properties.get('container_shell_path', '/bin/bash')

        # Properties common in all GROMACS BB
        self.gmxlib = properties.get('gmxlib', None)
        self.gmx_path = properties.get('gmx_path', 'gmx')
        self.gmx_nobackup = properties.get('gmx_nobackup', True)
        self.gmx_nocopyright = properties.get('gmx_nocopyright', True)
        if self.gmx_nobackup:
            self.gmx_path += ' -nobackup'
        if self.gmx_nocopyright:
            self.gmx_path += ' -nocopyright'
        if not self.container_path:
            self.gmx_version = get_gromacs_version(self.gmx_path)

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # Check the properties
        fu.check_properties(self, properties)

    def create_mdp(self, path: str = None) -> str:
        """Creates an MDP file using the properties file settings"""
        mdp_list = []

        self.output_mdp_path = path

        sim_type = self.mdp.get('type', 'minimization')
        minimization = (sim_type == 'minimization')
        nvt = (sim_type == 'nvt')
        npt = (sim_type == 'npt')
        free = (sim_type == 'free')
        index = (sim_type == 'index')
        md = (nvt or npt or free)
        mdp_list.append(";Type of MDP: " + sim_type)

        # Position restrain
        if not free:
            mdp_list.append("\n;Position restrain")
            mdp_list.append("Define = " + self.mdp.pop('define', '-DPOSRES'))

        # Run parameters
        mdp_list.append("\n;Run parameters")
        self.nsteps = self.mdp.pop('nsteps', '5000')
        mdp_list.append("nsteps = " + self.nsteps)
        if minimization:
            mdp_list.append("integrator = " + self.mdp.pop('integrator', 'steep'))
            mdp_list.append("emtol = " + self.mdp.pop('emtol', '1000.0'))
            mdp_list.append("emstep = " + self.mdp.pop('emstep', '0.01'))
        if md:
            mdp_list.append("integrator = " + self.mdp.pop('integrator', 'md'))
            self.dt = self.mdp.pop('dt', '0.002')
            mdp_list.append("dt = " + self.dt)

        # Output control
        if md:
            mdp_list.append("\n;Output control")
            if nvt or npt:
                mdp_list.append("nstxout = " + self.mdp.pop('nstxout', '500'))
                mdp_list.append("nstvout = " + self.mdp.pop('nstvout', '500'))
                mdp_list.append("nstenergy = " + self.mdp.pop('nstenergy', '500'))
                mdp_list.append("nstlog = " + self.mdp.pop('nstlog', '500'))
                mdp_list.append("nstcalcenergy = " + self.mdp.pop('nstcalcenergy', '100'))
                mdp_list.append("nstcomm = " + self.mdp.pop('nstcomm', '100'))
                mdp_list.append("nstxout-compressed = " + self.mdp.pop('nstxout-compressed', '1000'))
                mdp_list.append("compressed-x-precision = " + self.mdp.pop('compressed-x-precision', '1000'))
                mdp_list.append("compressed-x-grps = " + self.mdp.pop('compressed-x-grps', 'System'))
            if free:
                mdp_list.append("nstcomm = " + self.mdp.pop('nstcomm', '100'))
                mdp_list.append("nstxout = " + self.mdp.pop('nstxout', '5000'))
                mdp_list.append("nstvout = " + self.mdp.pop('nstvout', '5000'))
                mdp_list.append("nstenergy = " + self.mdp.pop('nstenergy', '5000'))
                mdp_list.append("nstlog = " + self.mdp.pop('nstlog', '5000'))
                mdp_list.append("nstcalcenergy = " + self.mdp.pop('nstcalcenergy', '100'))
                mdp_list.append("nstxout-compressed = " + self.mdp.pop('nstxout-compressed', '1000'))
                mdp_list.append("compressed-x-grps = " + self.mdp.pop('compressed-x-grps', 'System'))
                mdp_list.append("compressed-x-precision = " + self.mdp.pop('compressed-x-precision', '1000'))

        # Bond parameters
        if md:
            mdp_list.append("\n;Bond parameters")
            mdp_list.append("constraint-algorithm = " + self.mdp.pop('constraint-algorithm', 'lincs'))
            mdp_list.append("constraints = " + self.mdp.pop('constraints', 'h-bonds'))
            mdp_list.append("lincs-iter = " + self.mdp.pop('lincs-iter', '1'))
            mdp_list.append("lincs-order = " + self.mdp.pop('lincs-order', '4'))
            if nvt:
                mdp_list.append("continuation = " + self.mdp.pop('continuation', 'no'))
            if npt or free:
                mdp_list.append("continuation = " + self.mdp.pop('continuation', 'yes'))

        # Neighbour searching
        mdp_list.append("\n;Neighbour searching")
        mdp_list.append("cutoff-scheme = " + self.mdp.pop('cutoff-scheme', 'Verlet'))
        mdp_list.append("ns-type = " + self.mdp.pop('ns-type', 'grid'))
        mdp_list.append("rcoulomb = " + self.mdp.pop('rcoulomb', '1.0'))
        mdp_list.append("vdwtype = " + self.mdp.pop('vdwtype', 'cut-off'))
        mdp_list.append("rvdw = " + self.mdp.pop('rvdw', '1.0'))
        mdp_list.append("nstlist = " + self.mdp.pop('nstlist', '10'))
        mdp_list.append("rlist = " + self.mdp.pop('rlist', '1'))

        # Eletrostatics
        mdp_list.append("\n;Eletrostatics")
        mdp_list.append("coulombtype = " + self.mdp.pop('coulombtype', 'PME'))
        if md:
            mdp_list.append("pme-order = " + self.mdp.pop('pme-order', '4'))
            mdp_list.append("fourierspacing = " + self.mdp.pop('fourierspacing', '0.12'))
            mdp_list.append("fourier-nx = " + self.mdp.pop('fourier-nx', '0'))
            mdp_list.append("fourier-ny = " + self.mdp.pop('fourier-ny', '0'))
            mdp_list.append("fourier-nz = " + self.mdp.pop('fourier-nz', '0'))
            mdp_list.append("ewald-rtol = " + self.mdp.pop('ewald-rtol', '1e-5'))

        # Temperature coupling
        if md:
            mdp_list.append("\n;Temperature coupling")
            mdp_list.append("tcoupl = " + self.mdp.pop('tcoupl', 'V-rescale'))
            mdp_list.append("tc-grps = " + self.mdp.pop('tc-grps', 'Protein Non-Protein'))
            mdp_list.append("tau-t = " + self.mdp.pop('tau-t', '0.1	  0.1'))
            mdp_list.append("ref-t = " + self.mdp.pop('ref-t', '300 	  300'))

        # Pressure coupling
        if md:
            mdp_list.append("\n;Pressure coupling")
            if nvt:
                mdp_list.append("pcoupl = " + self.mdp.pop('pcoupl', 'no'))
            if npt or free:
                mdp_list.append("pcoupl = " + self.mdp.pop('pcoupl', 'Parrinello-Rahman'))
                mdp_list.append("pcoupltype = " + self.mdp.pop('pcoupltype', 'isotropic'))
                mdp_list.append("tau-p = " + self.mdp.pop('tau-p', '1.0'))
                mdp_list.append("ref-p = " + self.mdp.pop('ref-p', '1.0'))
                mdp_list.append("compressibility = " + self.mdp.pop('compressibility', '4.5e-5'))
                mdp_list.append("refcoord-scaling = " + self.mdp.pop('refcoord-scaling', 'com'))

        # Dispersion correction
        if md:
            mdp_list.append("\n;Dispersion correction")
            mdp_list.append("DispCorr = " + self.mdp.pop('DispCorr', 'EnerPres'))

        # Velocity generation
        if md:
            mdp_list.append("\n;Velocity generation")
            if nvt:
                mdp_list.append("gen-vel = " + self.mdp.pop('gen-vel', 'yes'))
                mdp_list.append("gen-temp = " + self.mdp.pop('gen-temp', '300'))
                mdp_list.append("gen-seed = " + self.mdp.pop('gen-seed', '-1'))
            if npt or free:
                mdp_list.append("gen-vel = " + self.mdp.pop('gen-vel', 'no'))

        # Periodic boundary conditions
        mdp_list.append("\n;Periodic boundary conditions")
        mdp_list.append("pbc = " + self.mdp.pop('pbc', 'xyz'))

        if index:
            mdp_list =[";This mdp file has been created by the pymdsetup.gromacs_wrapper.grompp.create_mdp()"]

        mdp_list.insert(0, ";This mdp file has been created by the pymdsetup.gromacs_wrapper.grompp.create_mdp()")

        # Adding the rest of parameters in the config file to the MDP file
        # if the parameter has already been added replace the value
        parameter_keys = [parameter.split('=')[0].strip().replace('_','-') for parameter in mdp_list]
        for k, v in self.mdp.items():
            config_parameter_key = str(k).strip().replace('_','-')
            if config_parameter_key != 'type':
                if config_parameter_key in parameter_keys:
                    mdp_list[parameter_keys.index(config_parameter_key)] = config_parameter_key + ' = '+str(v)
                else:
                    mdp_list.append(config_parameter_key + ' = '+str(v))

        with open(self.output_mdp_path, 'w') as mdp:
            for line in mdp_list:
                mdp.write(line + '\n')

        return self.output_mdp_path

    @launchlogger
    def launch(self) -> int:
        """Launches the execution of the GROMACS grompp module.

        Examples:
            This is a use example of how to use the Grommpp module from Python

            >>> from biobb_md.gromacs.grompp import Grompp
            >>> prop = { 'mdp':{ 'type': 'minimization', 'emtol':'500', 'nsteps':'5000'}}
            >>> Grompp(input_gro_path='/path/to/myStructure.gro', input_top_zip_path='/path/to/myTopology.zip', output_tpr_path='/path/to/NewCompiledBin.tpr', properties=prop).launch()

        """
        tmp_files = []
        mdout = 'mdout.mdp'
        tmp_files.append(mdout)

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check GROMACS version
        if not self.container_path:
            if self.gmx_version < 512:
                raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
            fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)

        # Restart if needed
        if self.restart:
            if fu.check_complete_files(self.io_dict["out"].values()):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Unzip topology to topology_out
        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=out_log)
        top_dir = str(Path(top_file).parent)
        tmp_files.append(top_dir)

        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        if self.input_mdp_path:
            self.output_mdp_path = self.input_mdp_path
        else:
            mdp_dir = fu.create_unique_dir()
            tmp_files.append(mdp_dir)
            self.output_mdp_path = self.create_mdp(path=str(Path(mdp_dir).joinpath(self.output_mdp_path)))

        md = self.mdp.get('type', 'minimization')
        if md not in ('index', 'free'):
            fu.log('Will run a %s md of %s steps' % (md, self.nsteps), out_log, self.global_log)
        elif md == 'index':
            fu.log('Will create a TPR to be used as structure file')
        else:
            fu.log('Will run a %s md of %s' % (md, fu.human_readable_time(int(self.nsteps)*float(self.dt))), out_log, self.global_log)

        if self.container_path:
            fu.log('Container execution enabled', out_log)

            shutil.copy2(self.output_mdp_path, container_io_dict.get("unique_dir"))
            self.output_mdp_path = str(Path(self.container_volume_path).joinpath(Path(self.output_mdp_path).name))

            shutil.copytree(top_dir, str(Path(container_io_dict.get("unique_dir")).joinpath(Path(top_dir).name)))
            top_file = str(Path(self.container_volume_path).joinpath(Path(top_dir).name, Path(top_file).name))

        cmd = [self.gmx_path, 'grompp',
               '-f', self.output_mdp_path,
               '-c', container_io_dict["in"]["input_gro_path"],
               '-r', container_io_dict["in"]["input_gro_path"],
               '-p', top_file,
               '-o', container_io_dict["out"]["output_tpr_path"],
               '-po', mdout,
               '-maxwarn', self.maxwarn]

        if container_io_dict["in"].get("input_cpt_path") and Path(container_io_dict["in"]["input_cpt_path"]).exists():
            cmd.append('-t')
            if self.container_path:
                shutil.copy2(container_io_dict["in"]["input_cpt_path"], container_io_dict.get("unique_dir"))
                cmd.append(str(Path(self.container_volume_path).joinpath(Path(container_io_dict["in"]["input_cpt_path"]).name)))
            else:
                cmd.append(container_io_dict["in"]["input_cpt_path"])
        if container_io_dict["in"].get("input_ndx_path") and Path(container_io_dict["in"]["input_ndx_path"]).exists():
            cmd.append('-n')
            if self.container_path:
                shutil.copy2(container_io_dict["in"]["input_ndx_path"], container_io_dict.get("unique_dir"))
                cmd.append(Path(self.container_volume_path).joinpath(Path(container_io_dict["in"]["input_ndx_path"]).name))
            else:
                cmd.append(container_io_dict["in"]["input_ndx_path"])

        new_env = None
        if self.gmxlib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmxlib

        cmd = fu.create_cmd_line(cmd, container_path=self.container_path,
                                 host_volume=container_io_dict.get("unique_dir"),
                                 container_volume=self.container_volume_path,
                                 container_working_dir=self.container_working_dir,
                                 container_user_uid=self.container_user_id,
                                 container_shell_path=self.container_shell_path,
                                 container_image=self.container_image,
                                 out_log=out_log, global_log=self.global_log)
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log, new_env).launch()
        fu.copy_to_host(self.container_path, container_io_dict, self.io_dict)

        tmp_files.append(container_io_dict.get("unique_dir"))
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS grompp module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_gro_path', required=True)
    required_args.add_argument('--input_top_zip_path', required=True)
    required_args.add_argument('--output_tpr_path', required=True)
    parser.add_argument('--input_cpt_path', required=False)
    parser.add_argument('--input_ndx_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    Grompp(input_gro_path=args.input_gro_path, input_top_zip_path=args.input_top_zip_path,
           output_tpr_path=args.output_tpr_path, input_cpt_path=args.input_cpt_path,
           input_ndx_path=args.input_ndx_path, properties=properties).launch()


if __name__ == '__main__':
    main()
