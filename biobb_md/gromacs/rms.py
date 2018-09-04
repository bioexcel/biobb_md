#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class Rms(object):
    """Wrapper of the GROMACS rms module.

    Args:
        input_structure_path (str): Path to the input GRO/PDB/TPR file.
        input_traj_path (str): Path to the GROMACS trajectory file XTC/TRR.
        output_xvg_path (str): Path to the XVG output file.
        properties (dic):
            | - **xvg** (*str*) - ("none") XVG plot formatting: xmgrace, xmgr, none.
            | - **selection** (*str*) - ("Protein-H") Group where the rms will be performed: System, Protein, Protein-H...
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_structure_path, input_traj_path, output_xvg_path,
                 properties, **kwargs):

        self.input_structure_path = input_structure_path
        self.input_traj_path = input_traj_path
        self.output_xvg_path = output_xvg_path
        # Properties specific for BB
        self.xvg = properties.get('xvg', "none")
        self.selection = properties.get('selection', "Protein-H")
        # Common in all BB
        self.gmx_path = properties.get('gmx_path','gmx')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')


    def launch(self):
        """Launches the execution of the GROMACS rms module.
        """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)

        cmd = ['echo', '\"'+self.selection+' '+self.selection+'\"', '|',
               self.gmx_path, 'rms',
               '-s', self.input_structure_path,
               '-f', self.input_traj_path,
               '-o', self.output_xvg_path,
               '-xvg', self.xvg]

        return cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS cluster module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_structure_path', required=True)
    parser.add_argument('--input_traj_path', required=True)
    parser.add_argument('--output_xvg_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Rms(input_structure_path=args.input_structure_path, input_traj_path=args.input_traj_path, output_xvg_path=args.output_xvg_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
