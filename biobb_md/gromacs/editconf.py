#!/usr/bin/env python3

"""Module containing the Editconf class and the command line interface."""
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError

class Editconf():
    """Wrapper class for the GROMACS editconf (http://manual.gromacs.org/current/onlinehelp/gmx-editconf.html) module.

    Args:
        input_gro_path (str): Path to the input GRO file.
        output_gro_path (str): Path to the output GRO file.
        properties (dic):
            | - **distance_to_molecule** (*float*) - (1.0) Distance of the box from the outermost atom in nm. ie 1.0nm = 10 Angstroms.
            | - **box_type** (*str*) - ("cubic") Geometrical shape of the solvent box. Available box types: (http://manual.gromacs.org/current/onlinehelp/gmx-editconf.html) -bt option.
            | - **center_molecule** (*bool*) - (True) Center molecule in the box.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_gro_path, output_gro_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_gro_path = input_gro_path
        self.output_gro_path = output_gro_path

        # Properties specific for BB
        self.distance_to_molecule = properties.get('distance_to_molecule', 1.0)
        self.box_type = properties.get('box_type', 'cubic')
        self.center_molecule = properties.get('center_molecule', True)

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
        """Launches the execution of the GROMACS editconf module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)
        if self.gmx_version < 512:
            raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
        fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)

        cmd = [self.gmx_path, 'editconf',
               '-f', self.input_gro_path,
               '-o', self.output_gro_path,
               '-d', str(self.distance_to_molecule),
               '-bt', self.box_type]

        if self.center_molecule:
            cmd.append('-c')
            fu.log('Centering molecule in the box.', out_log, self.global_log)

        fu.log("Distance of the box to molecule: %6.2f" % self.distance_to_molecule, out_log, self.global_log)
        fu.log("Box type: %s" % self.box_type, out_log, self.global_log)

        command = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log)
        return command.launch()

def main():
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS editconf module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_gro_path', required=True)
    required_args.add_argument('--output_gro_path', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Editconf(input_gro_path=args.input_gro_path, output_gro_path=args.output_gro_path, properties=properties).launch()

if __name__ == '__main__':
    main()
