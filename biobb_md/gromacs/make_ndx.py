#!/usr/bin/env python3

"""Module containing the MakeNdx class and the command line interface."""
import os
import argparse
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError


class MakeNdx(BiobbObject):
    """
    | biobb_md MakeNdx
    | Wrapper of the `GROMACS make_ndx <http://manual.gromacs.org/current/onlinehelp/gmx-make_ndx.html>`_ module.
    | The GROMACS make_ndx module, generates an index file using the atoms of the selection.

    Args:
        input_structure_path (str): Path to the input GRO/PDB/TPR file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/make_ndx.tpr>`_. Accepted formats: gro (edam:format_2033), pdb (edam:format_1476), tpr (edam:format_2333).
        output_ndx_path (str): Path to the output index NDX file. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_make_ndx.ndx>`_. Accepted formats: ndx (edam:format_2330).
        input_ndx_path (str) (Optional): Path to the input index NDX file. File type: input. Accepted formats: ndx (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **selection** (*str*) - ("a CA C N O") Heavy atoms. Atom selection string.
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

            from biobb_md.gromacs.make_ndx import make_ndx
            prop = { 'selection': 'a CA C N O' }
            make_ndx(input_structure_path='/path/to/myStructure.gro',
                     output_ndx_path='/path/to/newIndex.ndx',
                     properties=prop)

    Info:
        * wrapped_software:
            * name: GROMACS MakeNdx
            * version: >5.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """
    def __init__(self, input_structure_path: str, output_ndx_path: str, input_ndx_path: str = None,
                 properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure_path": input_structure_path, "input_ndx_path": input_ndx_path},
            "out": {"output_ndx_path": output_ndx_path}
        }

        # Properties specific for BB
        self.selection = properties.get('selection', "a CA C N O")

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
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`MakeNdx <gromacs.make_ndx.MakeNdx>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Create command line
        self.cmd = ['echo', '-e', '\'' + self.selection + '\\nq' + '\'', '|',
               self.gmx_path, 'make_ndx',
               '-f', self.stage_io_dict["in"]["input_structure_path"],
               '-o', self.stage_io_dict["out"]["output_ndx_path"]
               ]

        if self.stage_io_dict["in"].get("input_ndx_path")\
                and Path(self.stage_io_dict["in"].get("input_ndx_path")).exists():
            self.cmd.append('-n')
            self.cmd.append(self.stage_io_dict["in"].get("input_ndx_path"))

        if self.gmx_lib:
            self.environment = os.environ.copy()
            self.environment['GMXLIB'] = self.gmx_lib

        # Check GROMACS version
        if not self.container_path:
            if self.gmx_version < 512:
                raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
            fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), self.out_log)

        # create_cmd_line and execute_command
        self.run_biobb()

        # Retrieve results
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.append(self.stage_io_dict.get("unique_dir"))
        self.remove_tmp_files()

        return self.return_code


def make_ndx(input_structure_path: str, output_ndx_path: str,
             input_ndx_path: str = None, properties: dict = None, **kwargs) -> int:
    """Create :class:`MakeNdx <gromacs.make_ndx.MakeNdx>` class and
    execute the :meth:`launch() <gromacs.make_ndx.MakeNdx.launch>` method."""
    return MakeNdx(input_structure_path=input_structure_path,
                   output_ndx_path=output_ndx_path,
                   input_ndx_path=input_ndx_path,
                   properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS make_ndx module.",
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
    make_ndx(input_structure_path=args.input_structure_path,
             output_ndx_path=args.output_ndx_path,
             input_ndx_path=args.input_ndx_path,
             properties=properties)


if __name__ == '__main__':
    main()
