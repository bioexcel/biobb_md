#!/usr/bin/env python3

"""Module containing the Ndx2resttop class and the command line interface."""
import os
import fnmatch
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu

class Ndx2resttop():
    """Generate a restrained topology from an index NDX file.

    Args:
        input_ndx_path (str): Path to the input NDX index file.
        input_top_zip_path (str): Path the input TOP topology in zip format.
        output_top_zip_path (str): Path the output TOP topology in zip format.
        properties (dic):
            | - **force_constants** (*float[3]*): ("500 500 500") Array of three floats defining the force constants.
            | - **ref_rest_chain_triplet_list** (*str*): (None) Triplet list composed by (reference group, restrain group, chain) list.
    """

    def __init__(self, input_ndx_path, input_top_zip_path,
                 output_top_zip_path, properties, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_ndx_path = input_ndx_path
        self.input_top_zip_path = input_top_zip_path
        self.output_top_zip_path = output_top_zip_path

        # Properties specific for BB
        self.force_constants = properties.get('force_constants', '500 500 500')
        self.ref_rest_chain_triplet_list = properties.get('ref_rest_chain_triplet_list')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

        # Check the properties
        fu.check_properties(self, properties)

    def launch(self):
        """Launch the topology generation."""
        out_log, _ = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=out_log)

        # Create index list of index file :)
        index_dic={}
        lines = open(self.input_ndx_path,'r').read().splitlines()
        for index, line in enumerate(lines):
            if line.startswith('['):
                index_dic[line] = index,
                label = line
                if index > 0:
                    index_dic[label] = index_dic[label][0], index
        index_dic[label] = index_dic[label][0], index
        fu.log('Index_dic: '+str(index_dic), out_log, self.global_log)

        self.ref_rest_chain_triplet_list = [tuple(elem.strip(' ()').replace(' ', '').split(',')) for elem in self.ref_rest_chain_triplet_list.split('),')]
        for reference_group, restrain_group, chain in self.ref_rest_chain_triplet_list:
            fu.log('Reference group: '+reference_group, out_log, self.global_log)
            fu.log('Restrain group: '+restrain_group, out_log, self.global_log)
            fu.log('Chain: '+chain, out_log, self.global_log)
            self.output_itp_path = fu.create_name(path=os.path.dirname(top_file), prefix=self.prefix, step=self.step, name=restrain_group+'.itp')

            # Mapping atoms from absolute enumeration to Chain relative enumeration
            fu.log('reference_group_index: start_closed:'+str(index_dic['[ '+reference_group+' ]'][0]+1)+' stop_open: '+str(index_dic['[ '+reference_group+' ]'][1]), out_log, self.global_log)
            reference_group_list = [ int(elem) for line in lines[index_dic['[ '+reference_group+' ]'][0]+1: index_dic['[ '+reference_group+' ]'][1]] for elem in line.split() ]
            fu.log('restrain_group_index: start_closed:'+str(index_dic['[ '+restrain_group+' ]'][0]+1)+' stop_open: '+str(index_dic['[ '+restrain_group+' ]'][1]), out_log, self.global_log)
            restrain_group_list = [ int(elem) for line in lines[index_dic['[ '+restrain_group+' ]'][0]+1: index_dic['[ '+restrain_group+' ]'][1]] for elem in line.split() ]
            selected_list = [reference_group_list.index(atom)+1 for atom in restrain_group_list]

            # Creating new ITP with restrictions
            with open(self.output_itp_path, 'w') as f:
                fu.log('Creating: '+str(f)+' and adding the selected atoms force constants', out_log, self.global_log)
                f.write('[ position_restraints ]\n')
                f.write('; atom  type      fx      fy      fz\n')
                for atom in selected_list:
                    f.write(str(atom)+'     1  '+self.force_constants+'\n')

            # Including new ITP in the corresponding ITP-chain file
            for file_name in os.listdir(os.path.dirname(top_file)):
                if not file_name.startswith("posre") and not file_name.endswith("_pr.itp"):
                    if fnmatch.fnmatch(file_name, "*_chain_"+chain+".itp"):
                        with open(file_name, 'a') as f:
                            fu.log('Opening: '+str(f)+' and adding the ifdef include statement', out_log, self.global_log)
                            f.write('\n')
                            f.write('; Include Position restraint file\n')
                            f.write('#ifdef CUSTOM_POSRES\n')
                            f.write('#include "'+self.output_itp_path+'"\n')
                            f.write('#endif\n')

        # zip topology
        fu.zip_top(zip_file=self.output_top_zip_path, top_file=top_file, out_log=out_log)
        return 0

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS extra ndx2resttop module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_ndx_path', required=True)
    required_args.add_argument('--input_top_zip_path', required=True)
    required_args.add_argument('--output_top_zip_path', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Ndx2resttop(input_ndx_path=args.input_ndx_path, input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()

if __name__ == '__main__':
    main()
