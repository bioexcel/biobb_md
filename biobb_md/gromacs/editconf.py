#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class Editconf(object):
    """Wrapper class for the GROMACS editconf module.

    Args:
        input_gro_path (str): Path to the input GRO file.
        output_gro_path (str): Path to the output GRO file.
        properties (dic):
            | - **distance_to_molecule** (*float*) - (1.0) Distance of the box from the outermost atom in nm. ie 1.0nm = 10 Angstroms.
            | - **box_type** (*str*) - ("cubic") Geometrical shape of the solvent box. Available box types: octahedron, cubic, etc.
            | - **center_molecule** (*bool*) - (True) Center molecule in the box.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_gro_path, output_gro_path, properties, **kwargs):
        self.input_gro_path = input_gro_path
        self.output_gro_path = output_gro_path
        # Properties specific for BB
        self.distance_to_molecule = properties.get('distance_to_molecule',1.0)
        self.box_type = properties.get('box_type', 'cubic')
        self.center_molecule = properties.get('center_molecule',True)
        # Common in all BB
        self.gmx_path = properties.get('gmx_path','gmx')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')


    def launch(self):
        """Launches the execution of the GROMACS editconf module.
        """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)

        cmd = [self.gmx_path, 'editconf',
               '-f', self.input_gro_path,
               '-o', self.output_gro_path,
               '-d', str(self.distance_to_molecule),
               '-bt', self.box_type]

        if self.center_molecule:
            cmd.append('-c')
            out_log.info('Centering molecule in the box.')
            if self.global_log:
                self.global_log.info(fu.get_logs_prefix()+'Centering molecule in the box.')

        out_log.info('Distance of the box to molecule: '+str(self.distance_to_molecule))
        out_log.info('Box type: '+self.box_type)
        if self.global_log:
            self.global_log.info(fu.get_logs_prefix()+'Distance of the box to molecule: '+str(self.distance_to_molecule))
            self.global_log.info(fu.get_logs_prefix()+'Box type: '+self.box_type)

        command = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log)
        return command.launch()

def main():
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS editconf module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_gro_path', required=True)
    parser.add_argument('--output_gro_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Editconf(input_gro_path=args.input_gro_path, output_gro_path=args.output_gro_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
