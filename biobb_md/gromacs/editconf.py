#!/usr/bin/env python3

"""Editconf Module"""
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class Editconf(object):
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

        # IN OUT files
        self.input_gro_path = input_gro_path
        self.output_gro_path = output_gro_path

        # Properties specific for BB
        self.gmx_path = properties.get('gmx_path', 'gmx')
        self.gmx_version = fu.gromacs_version(self.gmx_path)
        self.distance_to_molecule = properties.get('distance_to_molecule', 1.0)
        self.box_type = properties.get('box_type', 'cubic')
        self.center_molecule = properties.get('center_molecule', True)

        # Properties common in all BB
        self.global_log = properties.get('global_log', None)
        self.console_log = properties.get('console_log', True)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')


    def launch(self):
        """Launches the execution of the GROMACS editconf module.
        """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, console=self.console_log)

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
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS editconf module.")
    parser.add_argument('--config', required=True)
    parser.add_argument('--system', required=False)
    parser.add_argument('--step', required=False)

    #Specific args of each building block
    parser.add_argument('--input_gro_path', required=True)
    parser.add_argument('--output_gro_path', required=True)
    ####

    args = parser.parse_args()
    args.config = args.config or "{}"
    if args.step:
        properties = settings.ConfReader(config=args.config, system=args.system).get_prop_dic()[args.step]
    else:
        properties = settings.ConfReader(config=args.config, system=args.system).get_prop_dic()

    #Specific call of each building block
    Editconf(input_gro_path=args.input_gro_path, output_gro_path=args.output_gro_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
