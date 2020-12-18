#!/usr/bin/env python3

"""Module containing the Select class and the command line interface."""
import os
import argparse
from pathlib import Path
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError


class Gmxselect:
    """
    | biobb_md Gmxselect
    | Wrapper of the `GROMACS select <http://manual.gromacs.org/current/onlinehelp/gmx-select.html>`_ module.
    | The GROMACS select module writes out basic data about dynamic selections. It can be used for some simple analyses, or the output can be combined with output from other programs and/or external analysis programs to calculate more complex things.

    Args:
        input_structure_path (str): Path to the input GRO/PDB/TPR file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/make_ndx.tpr>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033), tpr (edam:format_2333).
        output_ndx_path (str): Path to the output index NDX file. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_select.ndx>`_. Accepted formats: ndx (edam:format_2330).
        input_ndx_path (str) (Optional): Path to the input index NDX file. File type: input. Accepted formats: ndx (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **selection** (*str*) - ("a CA C N O") Heavy atoms. Atom selection string.
            * **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            * **gmx_lib** (*str*) - (None) Path set GROMACS GMXLIB environment variable.
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

            from biobb_md.gromacs.gmxselect import gmxselect
            prop = { 'selection': '"Mynewgroup" group "Protein-H" and not same residue as within 0.4 of resname ARG' }
            gmxselect(input_structure_path='/path/to/myStructure.gro',
                      output_ndx_path='/path/to/newIndex.ndx',
                      properties=prop)

    Info:
        * wrapped_software:
            * name: GROMACS Gmxselect
            * version: >5.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_structure_path: str, output_ndx_path: str, input_ndx_path: str = None,
                 properties: dict = None, **kwargs) -> None:
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
    def launch(self) -> int:
        """Execute the :class:`Gmxselect <gromacs.gmxselect.Gmxselect>` object."""
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

        if container_io_dict["in"].get("input_ndx_path") and Path(
                container_io_dict["in"].get("input_ndx_path")).exists():
            cmd.append('-n')
            cmd.append(container_io_dict["in"].get("input_ndx_path"))

        cmd.append('-select')
        cmd.append("\'"+self.selection+"\'")

        new_env = None
        if self.gmx_lib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmx_lib

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


def gmxselect(input_structure_path: str, output_ndx_path: str,
              input_ndx_path: str = None, properties: dict = None,
              **kwargs) -> int:
    """Create :class:`Gmxselect <gromacs.gmxselect.Gmxselect>` class and
    execute the :meth:`launch() <gromacs.gmxselect.Gmxselect.launch>` method."""
    return Gmxselect(input_structure_path=input_structure_path,
                     output_ndx_path=output_ndx_path,
                     input_ndx_path=input_ndx_path,
                     properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS select module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure_path', required=True)
    required_args.add_argument('--output_ndx_path', required=True)
    parser.add_argument('--input_ndx_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    gmxselect(input_structure_path=args.input_structure_path,
              output_ndx_path=args.output_ndx_path,
              input_ndx_path=args.input_ndx_path,
              properties=properties)


if __name__ == '__main__':
    main()
