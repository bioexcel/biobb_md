#!/usr/bin/env python3

"""Module containing the Editconf class and the command line interface."""
import os
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError


class Editconf:
    """
    | biobb_md Editconf
    | Wrapper class for the `GROMACS editconf <http://manual.gromacs.org/current/onlinehelp/gmx-editconf.html>`_ module.
    | The GROMACS solvate module generates a box around the selected structure.

    Args:
        input_gro_path (str): Path to the input GRO file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/editconf.gro>`_. Accepted formats: gro (edam:format_2033).
        output_gro_path (str): Path to the output GRO file. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_editconf.gro>`_. Accepted formats: gro (edam:format_2033).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **distance_to_molecule** (*float*) - (1.0) [0~100|0.1] Distance of the box from the outermost atom in nm. ie 1.0nm = 10 Angstroms.
            * **box_type** (*str*) - ("cubic") Geometrical shape of the solvent box. Values: cubic (rectangular box with all sides equal), triclinic (triclinic box), dodecahedron (rhombic dodecahedron), octahedron (truncated octahedron).
            * **center_molecule** (*bool*) - (True) Center molecule in the box.
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

    Info:
        * wrapped_software:
            * name: GROMACS Solvate
            * version: >5.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_gro_path: str, output_gro_path: str, properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {"input_gro_path": input_gro_path},
            "out": {"output_gro_path": output_gro_path}
        }

        # Properties specific for BB
        self.distance_to_molecule = properties.get('distance_to_molecule', 1.0)
        self.box_type = properties.get('box_type', 'cubic')
        self.center_molecule = properties.get('center_molecule', True)

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
        """Execute the :class:`Editconf <gromacs.editconf.Editconf>` object."""
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

        cmd = [self.gmx_path, 'editconf',
               '-f', container_io_dict["in"]["input_gro_path"],
               '-o', container_io_dict["out"]["output_gro_path"],
               '-d', str(self.distance_to_molecule),
               '-bt', self.box_type]

        if self.center_molecule:
            cmd.append('-c')
            fu.log('Centering molecule in the box.', out_log, self.global_log)

        fu.log("Distance of the box to molecule: %6.2f" % self.distance_to_molecule, out_log, self.global_log)
        fu.log("Box type: %s" % self.box_type, out_log, self.global_log)

        new_env = None
        if self.gmx_lib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmx_lib

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


def editconf(input_gro_path: str, output_gro_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`Editconf <gromacs.editconf.Editconf>` class and
    execute the :meth:`launch() <gromacs.editconf.Editconf.launch>` method."""

    return Editconf(input_gro_path=input_gro_path, output_gro_path=output_gro_path,
                    properties=properties, **kwargs).launch()


def main():
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS gmx editconf module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_gro_path', required=True)
    required_args.add_argument('--output_gro_path', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    editconf(input_gro_path=args.input_gro_path, output_gro_path=args.output_gro_path,
             properties=properties)


if __name__ == '__main__':
    main()
