#!/usr/bin/env python3

"""Module containing the Pdb2gmx class and the command line interface."""
import os
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError


class Pdb2gmx:
    """Wrapper class for the `GROMACS pdb2gmx <http://manual.gromacs.org/current/onlinehelp/gmx-pdb2gmx.html>`_ module.

    Args:
        input_pdb_path (str): Path to the input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/egfr.pdb>`_. Accepted formats: pdb.
        output_gro_path (str): Path to the output GRO file. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_pdb2gmx.gro>`_. Accepted formats: gro.
        output_top_zip_path (str): Path the output TOP topology in zip format. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_pdb2gmx.zip>`_. Accepted formats: zip.
        properties (dic):
            * **output_top_path** (*str*) - ("p2g.top") Path of the output TOP file.
            * **output_itp_path** (*str*) - ("p2g.itp") Path of the output itp file.
            * **water_type** (*str*) - ("spce") Water molecule type. Valid values: spc, spce, tip3p, tip4p, tip5p, tips3p.
            * **force_field** (*str*) - ("amber99sb-ildn") Force field to be used during the conversion. Valid values: gromos45a3, charmm27, gromos53a6, amber96, amber99, gromos43a2, gromos54a7, gromos43a1, amberGS, gromos53a5, amber99sb, amber03, amber99sb-ildn, oplsaa, amber94.
            * **ignh** (*bool*) - (False) Should pdb2gmx ignore the hidrogens in the original structure.
            * **his** (*str*) - (None) Histidine protonation array.
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

    """

    def __init__(self, input_pdb_path: str, output_gro_path: str, output_top_zip_path: str, properties: dict = None,
                 **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path},
            "out": {"output_gro_path": output_gro_path, "output_top_zip_path": output_top_zip_path}
        }

        # Properties specific for BB
        self.output_top_path = properties.get('output_top_path', 'p2g.top')
        self.output_itp_path = properties.get('output_itp_path', 'posre.itp')
        self.water_type = properties.get('water_type', 'spce')
        self.force_field = properties.get('force_field', 'amber99sb-ildn')
        self.ignh = properties.get('ignh', False)
        self.his = properties.get('his', None)

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
    def launch(self) -> int:
        """Launches the execution of the GROMACS pdb2gmx module."""
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

        output_top_path = fu.create_name(prefix=self.prefix, step=self.step, name=self.output_top_path)
        output_itp_path = fu.create_name(prefix=self.prefix, step=self.step, name=self.output_itp_path)

        cmd = [self.gmx_path, "pdb2gmx",
               "-f", container_io_dict["in"]["input_pdb_path"],
               "-o", container_io_dict["out"]["output_gro_path"],
               "-p", output_top_path,
               "-water", self.water_type,
               "-ff", self.force_field,
               "-i", output_itp_path]

        if self.his:
            cmd.append("-his")
            cmd = ['echo', self.his, '|'] + cmd
        if self.ignh:
            cmd.append("-ignh")

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

        if self.container_path:
            output_top_path = os.path.join(container_io_dict.get("unique_dir"), output_top_path)

        # zip topology
        fu.log('Compressing topology to: %s' % container_io_dict["out"]["output_top_zip_path"], out_log,
               self.global_log)
        fu.zip_top(zip_file=self.io_dict["out"]["output_top_zip_path"], top_file=output_top_path, out_log=out_log)

        tmp_files.append(self.output_top_path)
        tmp_files.append(self.output_itp_path)
        tmp_files.append(container_io_dict.get("unique_dir"))
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def main():
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS pdb2gmx module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True)
    required_args.add_argument('--output_gro_path', required=True)
    required_args.add_argument('--output_top_zip_path', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    Pdb2gmx(input_pdb_path=args.input_pdb_path, output_gro_path=args.output_gro_path,
            output_top_zip_path=args.output_top_zip_path, properties=properties).launch()


if __name__ == '__main__':
    main()
