#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class Solvate(object):
    """Wrapper of the GROMACS solvate module.

    Args:
        input_solute_gro_path (str): Path to the input GRO file.
        output_gro_path (str): Path to the output GRO file.
        input_top_zip_path (str): Path the input TOP topology in zip format.
        output_top_zip_path (str): Path the output topology in zip format.
        properties (dic):
            | - **output_top_path** (*str*) - ("solvate.top") Path the output TOP file.
            | - **intput_solvent_gro_path** (*str*) - ("spc216.gro") Path to the GRO file contanining the structure of the solvent.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_solute_gro_path, output_gro_path,
                 input_top_zip_path, output_top_zip_path, properties, **kwargs):
        self.input_solute_gro_path = input_solute_gro_path
        self.output_gro_path = output_gro_path
        self.input_top_zip_path = input_top_zip_path
        self.output_top_zip_path = output_top_zip_path
        # Properties specific for BB
        self.output_top_path = properties.get('output_top_path','solvate.top')
        self.input_solvent_gro_path = properties.get('input_solvent_gro_path','spc216.gro')
        # Common in all BB
        self.gmx_path = properties.get('gmx_path','gmx')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')

    def launch(self):
        """Launches the execution of the GROMACS solvate module.
        """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)
        self.output_top_path = fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name=self.output_top_path)

        fu.unzip_top(zip_file=self.input_top_zip_path, top_file=self.output_top_path, out_log=out_log)

        cmd = [self.gmx_path, 'solvate',
               '-cp', self.input_solute_gro_path,
               '-cs', self.input_solvent_gro_path,
               '-o',  self.output_gro_path,
               '-p',  self.output_top_path]

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        fu.zip_top(zip_file=self.output_top_zip_path, out_log=out_log)
        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS solvate module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_solute_gro_path', required=True)
    parser.add_argument('--output_gro_path', required=True)
    parser.add_argument('--input_top_zip_path', required=True)
    parser.add_argument('--output_top_zip_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Solvate(input_solute_gro_path=args.input_solute_gro_path, output_gro_path=args.output_gro_path, input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
