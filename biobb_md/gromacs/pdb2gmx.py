#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class Pdb2gmx(object):
    """Wrapper class for the GROMACS pdb2gmx module.

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
                 output_top_zip_path, properties, **kwargs):
        self.input_pdb_path = input_pdb_path
        self.output_gro_path = output_gro_path
        self.output_top_zip_path = output_top_zip_path
        # Properties specific for BB
        self.output_top_path = properties.get('output_top_path','p2g.top')
        self.output_itp_path = properties.get('output_itp_path','p2g.itp')
        self.water_type = properties.get('water_type','spce')
        self.force_field = properties.get('force_field','amber99sb-ildn')
        self.ignh = properties.get('ignh',False)
        # Common in all BB
        self.gmx_path = properties.get('gmx_path','gmx')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')

    def launch(self):
        """Launches the execution of the GROMACS pdb2gmx module.
        """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)

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
        out_log.info('Compressing topology to: '+self.output_top_zip_path)
        if self.global_log:
            self.global_log.info(fu.get_logs_prefix()+'Compressing topology to: '+self.output_top_zip_path)
        fu.zip_top(zip_file=self.output_top_zip_path, out_log=out_log)

        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS pdb2gmx module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_pdb_path', required=True)
    parser.add_argument('--output_gro_path', required=True)
    parser.add_argument('--output_top_zip_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Pdb2gmx(input_pdb_path=args.input_pdb_path, output_gro_path=args.output_gro_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
