#!/usr/bin/env python3

"""Module containing the Select class and the command line interface."""
import os
import argparse
import pathlib as pl
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError


class Select:
    """Wrapper of the GROMACS select (http://manual.gromacs.org/current/onlinehelp/gmx-select.html) module.

    Args:
        input_structure_path (str): Path to the input GRO/PDB/TPR file.
        output_ndx_path (str): Path to the output index NDX file.
        input_ndx_path (str)[Optional]: Path to the input index NDX file.
        properties (dic):
            * **selection** (*str*) - ("a CA C N O") Heavy atoms. Atom selection string.
            * **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*string*) - (None)  Path to the binary executable of your container.
            * **container_image** (*string*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*string*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*string*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*string*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*string*) - ("/bin/bash") Path to the binary executable of the container shell.
    """

    def __init__(self, input_structure_path, output_ndx_path, input_ndx_path=None, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure_path": input_structure_path},
            "out": {"output_ndx_path": output_ndx_path, "input_ndx_path": input_ndx_path}
        }

        # Properties specific for BB
        self.selection = properties.get('selection', "a CA C N O")

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

    @launchlogger
    def launch(self):
        """Launches the execution of the GROMACS select module."""
        tmp_files = []

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

        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        cmd = [self.gmx_path, 'select',
               '-s', container_io_dict["in"]["input_structure_path"],
               '-on', container_io_dict["out"]["output_ndx_path"]
               ]

        if container_io_dict["in"].get("input_ndx_path") and pl.Path(
                container_io_dict["in"].get("input_ndx_path")).exists():
            cmd.append('-n')
            cmd.append(container_io_dict["in"].get("input_ndx_path"))

        cmd.append('-select')
        cmd.append("\'"+self.selection+"\'")

        new_env = None
        if self.gmxlib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmxlib

        if self.container_path:
            if self.container_path.endswith('singularity'):
                fu.log('Using Singularity image %s' % self.container_image, out_log, self.global_log)
                cmd = [self.container_path, 'exec', '--bind',
                                   container_io_dict.get("unique_dir") + ':' + self.container_volume_path,
                                   self.container_image, " ".join(cmd)]

            elif self.container_path.endswith('docker'):
                fu.log('Using Docker image %s' % self.container_image, out_log, self.global_log)
                docker_cmd = [self.container_path, 'run', ]
                if self.container_working_dir:
                    docker_cmd.append('-w')
                    docker_cmd.append(self.container_working_dir)
                if self.container_volume_path:
                    docker_cmd.append('-v')
                    docker_cmd.append(container_io_dict.get("unique_dir") + ':' + self.container_volume_path)
                if self.container_user_id:
                    docker_cmd.append('--user')
                    docker_cmd.append(self.container_user_id)
                docker_cmd.append(self.container_image)
                docker_cmd.append(" ".join(cmd))
                cmd = docker_cmd
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log, new_env).launch()
        fu.copy_to_host(self.container_path, container_io_dict, self.io_dict)

        tmp_files.append(container_io_dict.get("unique_dir"))
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS select module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Common name for workflow properties set")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/configuration.html")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure_path', required=True)
    required_args.add_argument('--output_ndx_path', required=True)
    parser.add_argument('--input_ndx_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    # Specific call of each building block
    Select(input_structure_path=args.input_structure_path, output_ndx_path=args.output_ndx_path,
           input_ndx_path=args.input_ndx_path, properties=properties).launch()


if __name__ == '__main__':
    main()
