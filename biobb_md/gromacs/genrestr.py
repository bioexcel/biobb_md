#!/usr/bin/env python3

"""Module containing the Genrestr class and the command line interface."""
import os
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError

class Genrestr():
    """Wrapper class for the GROMACS genrestr (http://manual.gromacs.org/current/onlinehelp/gmx-genrestr.html) module.

    Args:
        input_structure_path (str): Path to the input structure PDB, GRO or TPR format.
        input_ndx_path (str): Path to the input GROMACS index file, NDX format.
        output_itp_path (str): Path the output ITP topology file with restrains.
        properties (dic):
            | - **restrained_group** (*str*) - ("system") Index group that will be restrained.
            | - **force_constants** (*str*) - ("500 500 500") Array of three floats defining the force constants
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_structure_path, input_ndx_path, output_itp_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = input_structure_path
        self.input_ndx_path = input_ndx_path
        self.output_itp_path = output_itp_path

        # Properties specific for BB
        self.force_constants = str(properties.get('force_constants', '500 500 500'))
        self.restrained_group = properties.get('restrained_group', 'system')

        # Properties common in all GROMACS BB
        self.gmxlib = properties.get('gmxlib', None)
        self.gmx_path = properties.get('gmx_path', 'gmx')
        self.gmx_nobackup = properties.get('gmx_nobackup', True)
        self.gmx_nocopyright = properties.get('gmx_nocopyright', True)
        if self.gmx_nobackup:
            self.gmx_path += ' -nobackup'
        if self.gmx_nocopyright:
            self.gmx_path += ' -nocopyright'
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

    def launch(self):
        """Launches the execution of the GROMACS genrestr module."""
        tmp_files = []

        #Create local logs
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        #Check GROMACS version
        if self.gmx_version < 512:
            raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
        fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)

        #Restart if needed
        if self.restart:
            output_file_list = [self.output_itp_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        cmd = ['echo', '\"'+self.restrained_group+'\"', '|',
               self.gmx_path, "genrestr",
               "-f", self.input_structure_path,
               "-n", self.input_ndx_path,
               "-o", self.output_itp_path,
               "-fc", self.force_constants]

        new_env = None
        if self.gmxlib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmxlib

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log, self.gmxlib).launch()

        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS genion module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure_path', required=True)
    required_args.add_argument('--input_ndx_path', required=True)
    required_args.add_argument('--output_itp_path', required=True)
    ####

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Genrestr(input_structure_path=args.input_structure_path, input_ndx_path=args.input_ndx_path, output_itp_path=args.output_itp_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
