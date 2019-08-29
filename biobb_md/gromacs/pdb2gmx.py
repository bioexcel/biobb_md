#!/usr/bin/env python3

"""Module containing the Pdb2gmx class and the command line interface."""
import os
import argparse
import shutil
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError

class Pdb2gmx():
    """Wrapper class for the GROMACS pdb2gmx (http://manual.gromacs.org/current/onlinehelp/gmx-pdb2gmx.html) module.

    Args:
        input_pdb_path (str): Path to the input PDB file.
        output_gro_path (str): Path to the output GRO file.
        output_top_zip_path (str): Path the output TOP topology in zip format.
        properties (dic):
            | - **output_top_path** (*str*) - ("p2g.top") Path of the output TOP file.
            | - **output_itp_path** (*str*) - ("p2g.itp") Path of the output itp file.
            | - **water_type** (*str*) - ("spce") Water molecule type. Valid values: tip3p, spce, etc.
            | - **force_field** (*str*) - ("amber99sb-ildn") Force field to be used during the conversion. Valid values: amber99sb-ildn, oplsaa, etc.
            | - **ignh** (*bool*) - (False) Should pdb2gmx ignore the hidrogens in the original structure.
            | - **his** (*str*) - (None) Histidine protonation array.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_pdb_path, output_gro_path,
                 output_top_zip_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_pdb_path = input_pdb_path
        self.output_gro_path = output_gro_path
        self.output_top_zip_path = output_top_zip_path

        # Properties specific for BB
        self.output_top_path = properties.get('output_top_path', 'p2g.top')
        self.output_itp_path = properties.get('output_itp_path', 'posre.itp')
        self.water_type = properties.get('water_type', 'spce')
        self.force_field = properties.get('force_field', 'amber99sb-ildn')
        self.ignh = properties.get('ignh', False)
        self.his = properties.get('his', None)

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
        """Launches the execution of the GROMACS pdb2gmx module."""
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
            output_file_list = [self.output_top_zip_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        self.output_top_path = fu.create_name(step=self.step, name=self.output_top_path)
        self.output_itp_path = fu.create_name(step=self.step, name=self.output_itp_path)
        cmd_docker = []
        cmd = [self.gmx_path, "pdb2gmx",
               "-f", self.input_pdb_path,
               "-o", self.output_gro_path,
               "-p", self.output_top_path,
               "-water", self.water_type,
               "-ff", self.force_field,
               "-i", self.output_itp_path]


        if self.docker_path:
            fu.log('Docker execution enabled', out_log)
            unique_dir = os.path.abspath(fu.create_unique_dir())
            shutil.copy2(self.input_pdb_path, unique_dir)
            docker_input_pdb_path = os.path.join(self.docker_volume_path, os.path.basename(self.input_pdb_path))
            docker_output_gro_path = os.path.join(self.docker_volume_path, os.path.basename(self.output_gro_path))
            docker_output_top_path = os.path.join(self.docker_volume_path, os.path.basename(self.output_top_path))
            cmd_docker = [self.docker_path, 'run',
                   '-v', unique_dir+':'+self.docker_volume_path,
                   '--user', str(os.getuid()),
                   self.docker_image]

            cmd = [self.gmx_path, "pdb2gmx",
                   "-f", docker_input_pdb_path,
                   "-o", docker_output_gro_path,
                   "-p", docker_output_top_path,
                   "-water", self.water_type,
                   "-ff", self.force_field,
                   "-i", os.path.basename(self.output_itp_path)]

        if self.his:
            cmd.append("-his")
            cmd = ['echo', self.his, '|'] + cmd
            if self.docker_path:
                cmd = ['"' + " ".join(cmd) + '"']
                cmd_docker.extend(['/bin/bash', '-c'])
        if self.ignh:
            cmd.append("-ignh")
        new_env = None
        if self.gmxlib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmxlib

        returncode = cmd_wrapper.CmdWrapper(cmd_docker + cmd, out_log, err_log, self.global_log, new_env).launch()

        if self.docker_path:
            tmp_files.append(unique_dir)
            shutil.copy2(os.path.join(unique_dir, os.path.basename(self.output_gro_path)), self.output_gro_path)
            self.output_top_path = os.path.join(unique_dir, os.path.basename(self.output_top_path))

        # zip topology
        fu.log('Compressing topology to: %s' % self.output_top_zip_path, out_log, self.global_log)
        tmp_files.extend(fu.zip_top(zip_file=self.output_top_zip_path, top_file=self.output_top_path, out_log=out_log))

        if self.remove_tmp:
            tmp_files.append(self.output_top_path)
            tmp_files.append(self.output_itp_path)
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS pdb2gmx module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True)
    required_args.add_argument('--output_gro_path', required=True)
    required_args.add_argument('--output_top_zip_path', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Pdb2gmx(input_pdb_path=args.input_pdb_path, output_gro_path=args.output_gro_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()

if __name__ == '__main__':
    main()
