#!/usr/bin/env python3

"""Module containing the MakeNdx class and the command line interface."""
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
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
    """

    def __init__(self, input_structure_path, output_ndx_path,
                 input_ndx_path=None, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = input_structure_path
        self.output_ndx_path = output_ndx_path
        #Optional files
        self.input_ndx_path = input_ndx_path

        # Properties specific for BB
        self.selection = properties.get('selection', "a CA C N O")

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
        """Launches the execution of the GROMACS make_ndx module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)
        if self.gmx_version < 512:
            raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
        fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)

        cmd = ['echo', '\"'+self.selection+' \n q'+'\"', '|',
               self.gmx_path, 'make_ndx',
               '-f', self.input_structure_path,
               '-o', self.output_ndx_path]

        if self.input_ndx_path:
            cmd.append('-n')
            cmd.append(self.input_ndx_path)

        return cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

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
