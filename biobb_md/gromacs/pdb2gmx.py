#!/usr/bin/env python3

"""Module containing the Pdb2gmx class and the command line interface."""
import argparse
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
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
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
        self.output_itp_path = properties.get('output_itp_path', 'p2g.itp')
        self.water_type = properties.get('water_type', 'spce')
        self.force_field = properties.get('force_field', 'amber99sb-ildn')
        self.ignh = properties.get('ignh', False)

        # Properties common in all GROMACS BB
        self.gmx_path = properties.get('gmx_path', 'gmx')
        self.gmx_version = get_gromacs_version(self.gmx_path)

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

        # Check the properties
        fu.check_properties(self, properties)

    def launch(self):
        """Launches the execution of the GROMACS pdb2gmx module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)
        if self.gmx_version < 512:
            raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
        fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)


        self.output_top_path = fu.create_name(prefix=self.prefix, step=self.step, name=self.output_top_path)
        self.output_itp_path = fu.create_name(prefix=self.prefix, step=self.step, name=self.output_itp_path)

        cmd = [self.gmx_path, "pdb2gmx",
               "-f", self.input_pdb_path,
               "-o", self.output_gro_path,
               "-p", self.output_top_path,
               "-water", self.water_type,
               "-ff", self.force_field,
               "-i", self.output_itp_path]

        if self.ignh:
            cmd.append("-ignh")

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        # zip topology
        fu.log('Compressing topology to: %s' % self.output_top_zip_path, out_log, self.global_log)
        fu.zip_top(zip_file=self.output_top_zip_path, top_file=self.output_top_path, out_log=out_log)
        tmp_files = [self.output_top_path, self.output_itp_path]
        removed_files = [f for f in tmp_files if fu.rm(f)]
        fu.log('Removed: %s' % str(removed_files), out_log, self.global_log)
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
