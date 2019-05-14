#!/usr/bin/env python3

"""Module containing the AppendLigand class and the command line interface."""
import os
import re
import argparse
import shutil
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class AppendLigand():
    """This class takes a ligand ITP file and inserts it in a topology.

    Args:
        input_top_zip_path (str): Path the input topology TOP and ITP files zipball.
        input_itp_path (str): Path to the ligand ITP file to be inserted in the topology.
        output_top_zip_path (str): Path/Name the output topology TOP and ITP files zipball.
        properties (dic):
    """

    def __init__(self, input_top_zip_path, input_itp_path, output_top_zip_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_top_zip_path = input_top_zip_path
        self.input_itp_path = input_itp_path
        self.output_top_zip_path = output_top_zip_path

        # Properties specific for BB

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

        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=out_log)
        top_dir = os.path.dirname(top_file)
        itp_name = os.path.basename(self.input_itp_path)

        with open(top_file, 'r') as top_f:
            top_lines = top_f.readlines()
            top_f.close()

        forcefield_pattern = r'#include.*forcefield.itp\"'
        for index, line in enumerate(top_lines):
            if re.search(forcefield_pattern, line):
                break
        top_lines.insert(index+1, '\n')
        top_lines.insert(index+2,'; Including ligand ITP\n')
        top_lines.insert(index+3, '#include "' + itp_name + '"\n')
        top_lines.insert(index+4,'\n')

        inside_moleculetype_section = False
        with open(self.input_itp_path, 'r') as itp_file:
            moleculetype_pattern = r'\[ moleculetype \]'
            for line in itp_file:
                if re.search(moleculetype_pattern, line):
                    inside_moleculetype_section = True
                    continue
                if inside_moleculetype_section and not line.startswith(';'):
                    print(line)
                    moleculetype = line.strip().split()[0].strip()
                    break

        molecules_pattern = r'\[ molecules \]'
        inside_molecules_section = False
        for index, line in enumerate(top_lines):
            if re.search(molecules_pattern, line):
                inside_molecules_section = True
                continue
            if inside_molecules_section and not line.startswith(';'):
                break
        top_lines.insert(index, moleculetype+(20-len(moleculetype))*' '+'1'+'\n')

        new_top = fu.create_name(path=top_dir, prefix=self.prefix, step=self.step, name='ligand.top')
        with open(new_top, 'w') as new_top_f:
            new_top_f.write("".join(top_lines))

        shutil.copy2(self.input_itp_path,top_dir)
        fu.zip_top(zip_file=self.output_top_zip_path, top_file=new_top, out_log=out_log)
        return 0

def main():
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS editconf module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_zip_path', required=True)
    required_args.add_argument('--input_itp_path', required=True)
    required_args.add_argument('--output_top_zip_path', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    AppendLigand(input_top_zip_path=args.input_top_zip_path, input_itp_path=args.input_itp_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()

if __name__ == '__main__':
    main()
