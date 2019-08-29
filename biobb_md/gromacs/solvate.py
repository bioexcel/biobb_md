#!/usr/bin/env python3

"""Module containing the Editconf class and the command line interface."""
import os
import shutil
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError

class Solvate():
    """Wrapper of the GROMACS solvate (http://manual.gromacs.org/current/onlinehelp/gmx-editconf.html) module.

    Args:
        input_solute_gro_path (str): Path to the input GRO file.
        output_gro_path (str): Path to the output GRO file.
        input_top_zip_path (str): Path the input TOP topology in zip format.
        output_top_zip_path (str): Path the output topology in zip format.
        properties (dic):
            | - **output_top_path** (*str*) - ("solvate.top") Path the output TOP file.
            | - **intput_solvent_gro_path** (*str*) - ("spc216.gro") Path to the GRO file contanining the structure of the solvent.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_solute_gro_path, output_gro_path, input_top_zip_path, output_top_zip_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_solute_gro_path = input_solute_gro_path
        self.output_gro_path = output_gro_path
        self.input_top_zip_path = input_top_zip_path
        self.output_top_zip_path = output_top_zip_path

        # Properties specific for BB
        self.input_solvent_gro_path = properties.get('input_solvent_gro_path', 'spc216.gro')

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

    def launch(self):
        """Launches the execution of the GROMACS solvate module."""
        tmp_files = []

        #Create local logs
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        #Check GROMACS version
        if not self.docker_path:
            if self.gmx_version < 512:
                raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
            fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)

        #Restart if needed
        if self.restart:
            output_file_list = [self.output_gro_path, self.output_top_zip_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        # Unzip topology
        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=out_log)
        tmp_files.append(os.path.dirname(top_file))

        cmd_docker = []
        cmd = [self.gmx_path, 'solvate',
               '-cp', self.input_solute_gro_path,
               '-cs', self.input_solvent_gro_path,
               '-o', self.output_gro_path,
               '-p', top_file]

        if self.docker_path:
            fu.log('Docker execution enabled', out_log)
            unique_dir = os.path.abspath(fu.create_unique_dir())
            shutil.copy2(self.input_solute_gro_path, unique_dir)
            docker_input_solute_gro_path = os.path.join(self.docker_volume_path, os.path.basename(self.input_solute_gro_path))
            top_dir = os.path.basename(os.path.dirname(top_file))
            shutil.copytree(top_dir, os.path.join(unique_dir, top_dir))
            docker_top_file = os.path.join(self.docker_volume_path, top_dir, os.path.basename(top_file))
            docker_output_gro_path = os.path.join(self.docker_volume_path, os.path.basename(self.output_gro_path))
            cmd_docker = [self.docker_path, 'run',
                          '-v', unique_dir+':'+self.docker_volume_path,
                          '--user', str(os.getuid()),
                          self.docker_image]

            cmd = [self.gmx_path, 'solvate',
                   '-cp', docker_input_solute_gro_path,
                   '-cs', self.input_solvent_gro_path,
                   '-o', docker_output_gro_path,
                   '-p', docker_top_file]

        new_env = None
        if self.gmxlib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmxlib

        returncode = cmd_wrapper.CmdWrapper(cmd_docker + cmd, out_log, err_log, self.global_log, new_env).launch()

        if self.docker_path:
            tmp_files.append(unique_dir)
            shutil.copy2(os.path.join(unique_dir, os.path.basename(self.output_gro_path)), self.output_gro_path)
            top_file = os.path.join(unique_dir, top_dir, os.path.basename(top_file))

        # zip topology
        fu.log('Compressing topology to: %s' % self.output_top_zip_path, out_log, self.global_log)
        fu.zip_top(zip_file=self.output_top_zip_path, top_file=top_file, out_log=out_log)

        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS solvate module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_solute_gro_path', required=True)
    required_args.add_argument('--output_gro_path', required=True)
    required_args.add_argument('--input_top_zip_path', required=True)
    required_args.add_argument('--output_top_zip_path', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Solvate(input_solute_gro_path=args.input_solute_gro_path, output_gro_path=args.output_gro_path, input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()

if __name__ == '__main__':
    main()
