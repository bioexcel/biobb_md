#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class Genion(object):
    """Wrapper class for the GROMACS genion module.

    Args:
        input_tpr_path (str): Path to the input portable run input TPR file.
        output_gro_path (str): Path to the input structure GRO file.
        input_top_zip_path (str): Path the input TOP topology in zip format.
        output_top_zip_path (str): Path the output topology TOP and ITP files zipball.
        properties (dic):
            | - **output_top_path** (*str*) - ("gio.top") Path the output topology TOP file.
            | - **replaced_group** (*str*) - ("SOL") Group of molecules that will be replaced by the solvent.
            | - **neutral** (*bool*) - (False) Neutralize the charge of the system.
            | - **concentration** (*float*) - (0.05) Concentration of the ions in (mol/liter).
            | - **seed** (*int*) - (1993) Seed for random number generator.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_tpr_path, output_gro_path, input_top_zip_path,
                 output_top_zip_path, properties, **kwargs):
        self.input_tpr_path = input_tpr_path
        self.output_gro_path = output_gro_path
        self.input_top_zip_path = input_top_zip_path
        self.output_top_zip_path = output_top_zip_path
        # Properties specific for BB
        self.output_top_path = properties.get('output_top_path','gio.top')
        self.replaced_group = properties.get('replaced_group','SOL')
        self.neutral = properties.get('neutral',False)
        self.concentration = properties.get('concentration',0.05)
        self.seed = properties.get('seed',1993)
        # Common in all BB
        self.gmx_path = properties.get('gmx_path','gmx')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')

    def launch(self):
        """Launches the execution of the GROMACS genion module.
        """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)

        if self.concentration:
            out_log.info('To reach up '+str(self.concentration)+' mol/litre concentration')
            if self.global_log:
                self.global_log.info(fu.get_logs_prefix()+'To reach up '+str(self.concentration)+' mol/litre concentration')

        self.output_top_path = fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name=self.output_top_path)

        # Unzip topology to topology_out
        fu.unzip_top(zip_file=self.input_top_zip_path, top_file=self.output_top_path, out_log=out_log)

        cmd = ['echo', '\"'+self.replaced_group+'\"', '|',
               self.gmx_path, 'genion',
               '-s', self.input_tpr_path,
               '-o', self.output_gro_path,
               '-p', self.output_top_path]


        if self.neutral:
            cmd.append('-neutral')

        if self.concentration:
            cmd.append('-conc')
            cmd.append(str(self.concentration))

        if self.seed is not None:
            cmd.append('-seed')
            cmd.append(str(self.seed))

        command = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log)
        returncode = command.launch()

        # zip new_topology
        fu.zip_top(zip_file=self.output_top_zip_path, out_log=out_log)
        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS genion module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_tpr_path', required=True)
    parser.add_argument('--output_gro_path', required=True)
    parser.add_argument('--input_top_zip_path', required=True)
    parser.add_argument('--output_top_zip_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Genion(input_tpr_path=args.input_tpr_path, output_gro_path=args.output_gro_path, input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
