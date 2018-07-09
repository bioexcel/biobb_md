#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class MakeNdx(object):
    """Wrapper of the GROMACS make_ndx module.

    Args:
        input_structure_path (str): Path to the input GRO/PDB/TPR file.
        output_ndx_path (str): Path to the output index NDX file.
        properties (dic):
            | - **selection** (*str*) - ("a CA C N O") Heavy atoms. Atom selection string.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_structure_path, output_ndx_path,
                 input_ndx_path=None, properties=None, **kwargs):
        self.input_structure_path = input_structure_path
        self.output_ndx_path = output_ndx_path
        #Optional files
        self.input_ndx_path = input_ndx_path
        # Properties specific for BB
        self.selection = properties.get('selection', "a CA C N O")
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

        cmd = ['echo', '\"'+self.selection+' \n q'+'\"', '|',
               self.gmx_path, 'make_ndx',
               '-f', self.input_structure_path,
               '-o', self.output_ndx_path]

        if self.input_ndx_path:
            cmd.append('-n')
            cmd.append(self.input_ndx_path)

        return cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS make_ndx module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_structure_path', required=True)
    parser.add_argument('--output_ndx_path', required=True)
    parser.add_argument('--input_ndx_path', required=False)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    MakeNdx(input_structure_path=args.input_structure_path, output_ndx_path=args.output_ndx_path, input_ndx_path=args.input_ndx_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
