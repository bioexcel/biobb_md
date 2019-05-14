#!/usr/bin/env python3

"""Module containing the MDrun class and the command line interface."""
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError

class Mdrun():
    """Wrapper of the GROMACS of the mdrun module.

    Args:
        input_tpr_path (str): Path to the portable binary run input file TPR.
        output_trr_path (str): Path to the GROMACS uncompressed raw trajectory file TRR.
        output_gro_path (str): Path to the output GROMACS structure GRO file.
        output_edr_path (str): Path to the output GROMACS portable energy file EDR.
        output_log_path (str): Path to the output GROMACS trajectory log file LOG.
        output_xtc_path (str)[Optional]: Path to the GROMACS compressed trajectory file XTC.
        output_cpt_path (str)[Optional]: Path to the output GROMACS checkpoint file CPT.
        output_dhdl_path (str)[Optional]: Path to the output dhdl.xvg file only used when free energy calculation is turned on.
        properties (dic):
            | - **num_threads** (*int*) - (0) Let GROMACS guess. The number of threads that are going to be used.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            | - **mpi_bin** (*str*) - (None) Path to the MPI runner. Usually "mpirun" or "srun".
            | - **mpi_np** (*str*) - (None) Number of MPI processes. Usually an integer bigger than 1.
            | - **mpi_hostlist** (*str*) - (None) Path to the MPI hostlist file.
    """

    def __init__(self, input_tpr_path, output_trr_path,
                 output_gro_path, output_edr_path,
                 output_log_path, output_xtc_path=None,
                 output_cpt_path=None, output_dhdl_path=None,
                 properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_tpr_path = input_tpr_path
        self.output_trr_path = output_trr_path
        self.output_gro_path = output_gro_path
        self.output_edr_path = output_edr_path
        self.output_log_path = output_log_path
        #Optional files
        self.output_xtc_path = output_xtc_path
        self.output_cpt_path = output_cpt_path
        self.output_dhdl_path = output_dhdl_path

        # Properties specific for BB
        self.num_threads = str(properties.get('num_threads', 0))
        self.mpi_bin = properties.get('mpi_bin')
        self.mpi_np = properties.get('mpi_np')
        self.mpi_hostlist = properties.get('mpi_hostlist')

        # Properties common in all GROMACS BB
        self.gmx_path = properties.get('gmx_path', 'gmx')
        if not self.mpi_bin:
            self.gmx_version = get_gromacs_version(self.gmx_path)

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

        # Check the properties
        fu.check_properties(self, properties)

    def launch(self):
        """Launches the execution of the GROMACS mdrun module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)
        if not self.mpi_bin:
            if self.gmx_version < 512:
                raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
            fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)

        cmd = [self.gmx_path, 'mdrun',
               '-s', self.input_tpr_path,
               '-o', self.output_trr_path,
               '-c', self.output_gro_path,
               '-e', self.output_edr_path,
               '-g', self.output_log_path,
               '-nt', self.num_threads]
        if self.mpi_bin:
            mpi_cmd = [self.mpi_bin]
            if self.mpi_np:
                mpi_cmd.append('-np')
                mpi_cmd.append(str(self.mpi_np))
            if self.mpi_hostlist:
                mpi_cmd.append('-H')
                mpi_cmd.append(self.mpi_hostlist)
        if self.output_xtc_path:
            cmd.append('-x')
            cmd.append(self.output_xtc_path)
        if self.output_cpt_path:
            cmd.append('-cpo')
            cmd.append(self.output_cpt_path)
        if self.output_dhdl_path:
            cmd.append('-dhdl')
            cmd.append(self.output_dhdl_path)

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()
        if not self.output_xtc_path:
            tmp_files = ['traj_comp.xtc']
            removed_files = [f for f in tmp_files if fu.rm(f)]
            fu.log('Removed: %s' % str(removed_files), out_log, self.global_log)
        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS mdrun module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_tpr_path', required=True)
    required_args.add_argument('--output_trr_path', required=True)
    required_args.add_argument('--output_gro_path', required=True)
    required_args.add_argument('--output_edr_path', required=True)
    required_args.add_argument('--output_log_path', required=True)
    parser.add_argument('--output_xtc_path', required=False)
    parser.add_argument('--output_cpt_path', required=False)
    parser.add_argument('--output_dhdl_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Mdrun(input_tpr_path=args.input_tpr_path, output_trr_path=args.output_trr_path, output_gro_path=args.output_gro_path, output_edr_path=args.output_edr_path, output_log_path=args.output_log_path, output_xtc_path=args.output_xtc_path, output_cpt_path=args.output_cpt_path, output_dhdl_path=args.output_dhdl_path, properties=properties).launch()

if __name__ == '__main__':
    main()
