#!/usr/bin/env python3

"""Module containing the MakeNdx class and the command line interface."""
import os
import shutil
import argparse
import pathlib as pl
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError

class MakeNdx():
    """Wrapper of the GROMACS make_ndx (http://manual.gromacs.org/current/onlinehelp/gmx-make_ndx.html) module.

    Args:
        input_structure_path (str): Path to the input GRO/PDB/TPR file.
        output_ndx_path (str): Path to the output index NDX file.
        properties (dic):
            | - **selection** (*str*) - ("a CA C N O") Heavy atoms. Atom selection string.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_structure_path, output_ndx_path, input_ndx_path=None, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = input_structure_path
        self.output_ndx_path = output_ndx_path
        #Optional files
        self.input_ndx_path = input_ndx_path

        # Properties specific for BB
        self.selection = properties.get('selection', "a CA C N O")

        # Properties common in all GROMACS BB
        self.gmxlib = properties.get('gmxlib', None)
        self.gmx_path = properties.get('gmx_path', 'gmx')
        self.gmx_nobackup = properties.get('gmx_nobackup', True)
        self.gmx_nocopyright = properties.get('gmx_nocopyright', True)
        if self.gmx_nobackup:
            self.gmx_path += ' -nobackup'
        if self.gmx_nocopyright:
            self.gmx_path += ' -nocopyright'
        if not properties.get('docker_path'):
            self.gmx_version = get_gromacs_version(self.gmx_path)

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # Docker Specific
        self.docker_path = properties.get('docker_path')
        self.docker_image = properties.get('docker_image', 'mmbirb/pmx')
        self.docker_volume_path = properties.get('docker_volume_path', '/inout')

        # Check the properties
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self):
        """Launches the execution of the GROMACS make_ndx module."""
        tmp_files = []


        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        #Check GROMACS version
        if not self.docker_path:
            if self.gmx_version < 512:
                raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
            fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)

        #Restart if needed
        if self.restart:
            output_file_list = [self.output_ndx_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        cmd_docker = []
        cmd = ['echo', '\"'+self.selection+' \n q'+'\"', '|',
               self.gmx_path, 'make_ndx',
               '-f', self.input_structure_path,
               '-o', self.output_ndx_path]

        if self.docker_path:
            fu.log('Docker execution enabled', out_log)
            unique_dir = pl.Path((fu.create_unique_dir())).resolve()
            shutil.copy2(self.input_structure_path, unique_dir)
            docker_input_structure_path = pl.Path(self.docker_volume_path, pl.Path(self.input_structure_path).name)
            docker_output_ndx_path = pl.Path(self.docker_volume_path, pl.Path(self.output_ndx_path).name)
            cmd_docker = [self.docker_path, 'run',
                          '-v', str(unique_dir)+':'+str(self.docker_volume_path),
                          '--user', str(os.getuid()),
                          self.docker_image]

            cmd = ['echo', '\"'+self.selection+' \n q'+'\"', '|',
                   self.gmx_path, 'make_ndx',
                   '-f', docker_input_structure_path,
                   '-o', docker_output_ndx_path]

        if self.input_ndx_path and pl.Path(self.input_ndx_path).exists():
            cmd.append('-n')
            if self.docker_path:
                shutil.copy2(self.input_ndx_path, unique_dir)
                cmd.append(str(pl.Path(self.docker_volume_path, pl.Path(self.input_ndx_path).name)))
            else:
                cmd.append(self.input_ndx_path)

        if self.docker_path:
            cmd = ['"' + " ".join(cmd) + '"']
            cmd_docker.extend(['/bin/bash', '-c'])

        new_env = None
        if self.gmxlib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmxlib

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log, new_env).launch()

        if self.docker_path:
            tmp_files.append(unique_dir)
            shutil.copy2(pl.Path(unique_dir, os.Path(self.output_gro_path).name), self.output_gro_path)

        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS make_ndx module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure_path', required=True)
    required_args.add_argument('--output_ndx_path', required=True)
    parser.add_argument('--input_ndx_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    MakeNdx(input_structure_path=args.input_structure_path, output_ndx_path=args.output_ndx_path, input_ndx_path=args.input_ndx_path, properties=properties).launch()

if __name__ == '__main__':
    main()
