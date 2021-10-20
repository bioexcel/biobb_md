#!/usr/bin/env python3

"""Module containing the Grompp class and the command line interface."""
import os
import argparse
import shutil
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError
from biobb_md.gromacs.common import create_mdp
from biobb_md.gromacs.common import mdp_preset


class Grompp(BiobbObject):
    """
    | biobb_md Grompp
    | Wrapper of the `GROMACS grompp <http://manual.gromacs.org/current/onlinehelp/gmx-grompp.html>`_ module.
    | The GROMACS preprocessor module needs to be fed with the input system and the dynamics parameters to create a portable binary run input file TPR. The simulation parameters can be specified by two methods:  1.The predefined mdp settings defined at simulation_type property or  2.A custom mdp file defined at the input_mdp_path argument.  These two methods are mutually exclusive. In both cases can be further modified by adding parameters to the mdp section in the yaml configuration file. The simulation parameter names and default values can be consulted in the `official MDP specification <http://manual.gromacs.org/current/user-guide/mdp-options.html>`_.

    Args:
        input_gro_path (str): Path to the input GROMACS structure GRO file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.gro>`_. Accepted formats: gro (edam:format_2033).
        input_top_zip_path (str): Path to the input GROMACS topology TOP and ITP files in zip format. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.zip>`_. Accepted formats: zip (edam:format_3987).
        output_tpr_path (str): Path to the output portable binary run file TPR. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_grompp.tpr>`_. Accepted formats: tpr (edam:format_2333).
        input_cpt_path (str) (Optional): Path to the input GROMACS checkpoint file CPT. File type: input. Accepted formats: cpt (edam:format_2333).
        input_ndx_path (str) (Optional): Path to the input GROMACS index files NDX. File type: input. Accepted formats: ndx (edam:format_2330).
        input_mdp_path (str) (Optional): Path to the input GROMACS `MDP file <http://manual.gromacs.org/current/user-guide/mdp-options.html>`_. File type: input. Accepted formats: mdp (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **mdp** (*dict*) - ({}) MDP options specification.
            * **simulation_type** (*str*) - (None) Default options for the mdp file. Each one creates a different mdp file. Values: `minimization <https://biobb-md.readthedocs.io/en/latest/_static/mdp/minimization.mdp>`_ (Energy minimization using steepest descent algorithm is used), `nvt <https://biobb-md.readthedocs.io/en/latest/_static/mdp/nvt.mdp>`_ (substance N Volume V and Temperature T are conserved), `npt <https://biobb-md.readthedocs.io/en/latest/_static/mdp/npt.mdp>`_ (substance N pressure P and Temperature T are conserved), `free <https://biobb-md.readthedocs.io/en/latest/_static/mdp/free.mdp>`_ (No design constraints applied; Free MD), `ions <https://biobb-md.readthedocs.io/en/latest/_static/mdp/minimization.mdp>`_ (Synonym of minimization), index (Creates an empty mdp file).
            * **maxwarn** (*int*) - (0) [0~1000|1] Maximum number of allowed warnings. If simulation_type is index default is 10.
            * **gmx_lib** (*str*) - (None) Path set GROMACS GMXLIB environment variable.
            * **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_md.gromacs.grompp import grompp

            prop = { 'simulation_type': 'minimization',
                     'mdp':
                        { 'emtol':'500',
                          'nsteps':'5000'}}
            grompp(input_gro_path='/path/to/myStructure.gro',
                   input_top_zip_path='/path/to/myTopology.zip',
                   output_tpr_path='/path/to/newCompiledBin.tpr',
                   properties=prop)

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
                 input_cpt_path: str = None, input_ndx_path: str = None, input_mdp_path: str = None,
                 properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_gro_path": input_gro_path, "input_cpt_path": input_cpt_path,
                   "input_ndx_path": input_ndx_path, "input_mdp_path": input_mdp_path},
            "out": {"output_tpr_path": output_tpr_path}
        }
        # Should not be copied inside container
        self.input_top_zip_path = input_top_zip_path

        # Properties specific for BB
        self.output_mdp_path = properties.get('output_mdp_path', 'grompp.mdp')
        self.output_top_path = properties.get('output_top_path', 'grompp.top')
        self.simulation_type = properties.get('simulation_type')
        self.maxwarn = str(properties.get('maxwarn', 0))
        if self.simulation_type and self.simulation_type != 'index':
            self.maxwarn = str(properties.get('maxwarn', 10))
        self.mdp = {k: str(v) for k, v in properties.get('mdp', dict()).items()}

        # container Specific
        self.container_path = properties.get('container_path')
        self.container_image = properties.get('container_image', 'gromacs/gromacs:latest')
        self.container_volume_path = properties.get('container_volume_path', '/data')
        self.container_working_dir = properties.get('container_working_dir')
        self.container_user_id = properties.get('container_user_id')
        self.container_shell_path = properties.get('container_shell_path', '/bin/bash')

        # Properties common in all GROMACS BB
        self.gmx_lib = properties.get('gmx_lib', None)
        self.gmx_path = properties.get('gmx_path', 'gmx')
        self.gmx_nobackup = properties.get('gmx_nobackup', True)
        self.gmx_nocopyright = properties.get('gmx_nocopyright', True)
        if self.gmx_nobackup:
            self.gmx_path += ' -nobackup'
        if self.gmx_nocopyright:
            self.gmx_path += ' -nocopyright'
        if not self.container_path:
            self.gmx_version = get_gromacs_version(self.gmx_path)

        # Check the properties
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Grompp <gromacs.grompp.Grompp>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Unzip topology to topology_out
        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=self.out_log)
        top_dir = str(Path(top_file).parent)

        # Create MDP file
        mdp_dir = fu.create_unique_dir()
        self.output_mdp_path = create_mdp(output_mdp_path=str(Path(mdp_dir).joinpath(self.output_mdp_path)),
                                          input_mdp_path=self.io_dict["in"]["input_mdp_path"],
                                          preset_dict=mdp_preset(self.simulation_type),
                                          mdp_properties_dict=self.mdp)

        # Copy extra files to container: MDP file and topology folder
        if self.container_path:
            fu.log('Container execution enabled', self.out_log)

            shutil.copy2(self.output_mdp_path, self.stage_io_dict.get("unique_dir"))
            self.output_mdp_path = str(Path(self.container_volume_path).joinpath(Path(self.output_mdp_path).name))

            shutil.copytree(top_dir, str(Path(self.stage_io_dict.get("unique_dir")).joinpath(Path(top_dir).name)))
            top_file = str(Path(self.container_volume_path).joinpath(Path(top_dir).name, Path(top_file).name))

        self.cmd = [self.gmx_path, 'grompp',
               '-f', self.output_mdp_path,
               '-c', self.stage_io_dict["in"]["input_gro_path"],
               '-r', self.stage_io_dict["in"]["input_gro_path"],
               '-p', top_file,
               '-o', self.stage_io_dict["out"]["output_tpr_path"],
               '-po', 'mdout.mdp',
               '-maxwarn', self.maxwarn]

        if self.stage_io_dict["in"].get("input_cpt_path") and Path(self.stage_io_dict["in"]["input_cpt_path"]).exists():
            self.cmd.append('-t')
            if self.container_path:
                shutil.copy2(self.stage_io_dict["in"]["input_cpt_path"], self.stage_io_dict.get("unique_dir"))
                self.cmd.append(str(Path(self.container_volume_path).joinpath(Path(self.stage_io_dict["in"]["input_cpt_path"]).name)))
            else:
                self.cmd.append(self.stage_io_dict["in"]["input_cpt_path"])
        if self.stage_io_dict["in"].get("input_ndx_path") and Path(self.stage_io_dict["in"]["input_ndx_path"]).exists():
            self.cmd.append('-n')
            if self.container_path:
                shutil.copy2(self.stage_io_dict["in"]["input_ndx_path"], self.stage_io_dict.get("unique_dir"))
                self.cmd.append(Path(self.container_volume_path).joinpath(Path(self.stage_io_dict["in"]["input_ndx_path"]).name))
            else:
                self.cmd.append(self.stage_io_dict["in"]["input_ndx_path"])

        if self.gmx_lib:
            self.environment = os.environ.copy()
            self.environment['GMXLIB'] = self.gmx_lib

        # Check GROMACS version
        if not self.container_path:
            if self.gmx_version < 512:
                raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
            fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), self.out_log)

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), top_dir, mdp_dir, 'mdout.mdp'])
        self.remove_tmp_files()

        return self.return_code


def grompp(input_gro_path: str, input_top_zip_path: str, output_tpr_path: str,
           input_cpt_path: str = None, input_ndx_path: str = None, input_mdp_path: str = None,
           properties: dict = None, **kwargs) -> int:
    """Create :class:`Grompp <gromacs.grompp.Grompp>` class and
    execute the :meth:`launch() <gromacs.grompp.Grompp.launch>` method."""

    return Grompp(input_gro_path=input_gro_path, input_top_zip_path=input_top_zip_path,
                  output_tpr_path=output_tpr_path, input_cpt_path=input_cpt_path,
                  input_ndx_path=input_ndx_path, input_mdp_path=input_mdp_path,
                  properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
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
    parser.add_argument('--input_mdp_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    grompp(input_gro_path=args.input_gro_path, input_top_zip_path=args.input_top_zip_path,
           output_tpr_path=args.output_tpr_path, input_cpt_path=args.input_cpt_path,
           input_ndx_path=args.input_ndx_path, input_mdp_path=args.input_mdp_path,
           properties=properties)


if __name__ == '__main__':
    main()
