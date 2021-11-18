#!/usr/bin/env python3

"""Module containing the Pdb2gmx class and the command line interface."""
import os
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError


class Pdb2gmx(BiobbObject):
    """
    | biobb_md Pdb2gmx
    | Wrapper class for the `GROMACS pdb2gmx <http://manual.gromacs.org/current/onlinehelp/gmx-pdb2gmx.html>`_ module.
    | The GROMACS pdb2gmx module, reads a .pdb (or .gro) file, reads some database files, adds hydrogens to the molecules and generates coordinates in GROMACS (GROMOS), or optionally .pdb, format and a topology in GROMACS format. These files can subsequently be processed to generate a run input file.

    Args:
        input_pdb_path (str): Path to the input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/egfr.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_gro_path (str): Path to the output GRO file. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_pdb2gmx.gro>`_. Accepted formats: gro (edam:format_2033).
        output_top_zip_path (str): Path the output TOP topology in zip format. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_pdb2gmx.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **water_type** (*str*) - ("spce") Water molecule type. Values: spc, spce, tip3p, tip4p, tip5p, tips3p.
            * **force_field** (*str*) - ("amber99sb-ildn") Force field to be used during the conversion.  Values: gromos45a3, charmm27, gromos53a6, amber96, amber99, gromos43a2, gromos54a7, gromos43a1, amberGS, gromos53a5, amber99sb, amber03, amber99sb-ildn, oplsaa, amber94.
            * **ignh** (*bool*) - (False) Should pdb2gmx ignore the hidrogens in the original structure.
            * **his** (*str*) - (None) Histidine protonation array.
            * **merge** (*bool*) - (False) Merge all chains into a single molecule.
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

            from biobb_md.gromacs.pdb2gmx import pdb2gmx
            prop = { 'his': '0 0 1 1 0 0 0' }
            pdb2gmx(input_pdb_path='/path/to/myStructure.pdb',
                    output_gro_path='/path/to/newStructure.gro',
                    output_top_zip_path='/path/to/newTopology.zip',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: GROMACS Pdb2gmx
            * version: >5.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_pdb_path: str, output_gro_path: str, output_top_zip_path: str, properties: dict = None,
                 **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path},
            "out": {"output_gro_path": output_gro_path, "output_top_zip_path": output_top_zip_path}
        }

        # Properties specific for BB
        self.internal_top_name = properties.get('internal_top_name', 'p2g.top') # Excluded from documentation for simplicity
        self.internal_itp_name = properties.get('internal_itp_name', 'posre.itp') # Excluded from documentation for simplicity
        self.water_type = properties.get('water_type', 'spce')
        self.force_field = properties.get('force_field', 'amber99sb-ildn')
        self.ignh = properties.get('ignh', False)
        self.his = properties.get('his', None)
        self.merge = properties.get('merge', False)

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
        self.check_properties(properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Pdb2gmx <gromacs.pdb2gmx.Pdb2gmx>` object."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        internal_top_name = fu.create_name(prefix=self.prefix, step=self.step, name=self.internal_top_name)
        internal_itp_name = fu.create_name(prefix=self.prefix, step=self.step, name=self.internal_itp_name)

        # Create command line
        self.cmd = [self.gmx_path, "pdb2gmx",
                    "-f", self.stage_io_dict["in"]["input_pdb_path"],
                    "-o", self.stage_io_dict["out"]["output_gro_path"],
                    "-p", internal_top_name,
                    "-water", self.water_type,
                    "-ff", self.force_field,
                    "-i", internal_itp_name]

        if self.his:
            self.cmd.append("-his")
            self.cmd = ['echo', self.his, '|'] + self.cmd
        if self.ignh:
            self.cmd.append("-ignh")
        if self.merge:
            self.cmd.append("-merge")
            self.cmd.append("all")

        if self.gmx_lib:
            self.environment = os.environ.copy()
            self.environment['GMXLIB'] = self.gmx_lib

        # Check GROMACS version
        if not self.container_path:
            if self.gmx_version < 512:
                raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
            fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), self.out_log)

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        if self.container_path:
            internal_top_name = os.path.join(self.stage_io_dict.get("unique_dir"), internal_top_name)

        # zip topology
        fu.log('Compressing topology to: %s' % self.io_dict["out"]["output_top_zip_path"], self.out_log,
               self.global_log)
        fu.zip_top(zip_file=self.io_dict["out"]["output_top_zip_path"], top_file=internal_top_name, out_log=self.out_log)

        # Remove temporal files
        self.tmp_files.extend([self.internal_top_name, self.internal_itp_name, self.stage_io_dict.get("unique_dir")])
        self.remove_tmp_files()

        return self.return_code


def pdb2gmx(input_pdb_path: str, output_gro_path: str, output_top_zip_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`Pdb2gmx <gromacs.pdb2gmx.Pdb2gmx>` class and
    execute the :meth:`launch() <gromacs.pdb2gmx.Pdb2gmx.launch>` method."""

    return Pdb2gmx(input_pdb_path=input_pdb_path, output_gro_path=output_gro_path,
                   output_top_zip_path=output_top_zip_path, properties=properties,
                   **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
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
    pdb2gmx(input_pdb_path=args.input_pdb_path, output_gro_path=args.output_gro_path,
            output_top_zip_path=args.output_top_zip_path, properties=properties)


if __name__ == '__main__':
    main()
