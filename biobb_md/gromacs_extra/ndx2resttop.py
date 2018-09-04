#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
import os
import fnmatch

class Ndx2resttop(object):
    """Generate a restrained topology from an index NDX file.

    Args:
        input_ndx_path (str): Path to the input NDX index file.
        input_top_zip_path (str): Path the input TOP topology in zip format.
        output_top_zip_path (str): Path the output TOP topology in zip format.
        properties (dic):
            | - **output_top_path** (*str*): ("restrain.top") Path the output TOP file.
            | - **force_constants** (*float[3]*): ("500 500 500") Array of three floats defining the force constants.
            | - **ref_rest_chain_triplet_list** (*str*): (None) Triplet list composed by (reference group, restrain group, chain) list.
    """

    def __init__(self, input_ndx_path, input_top_zip_path,
                 output_top_zip_path, properties, **kwargs):
        self.input_ndx_path = input_ndx_path
        self.input_top_zip_path = input_top_zip_path
        self.output_top_zip_path = output_top_zip_path
        # Properties specific for BB
        self.output_top_path = properties.get('output_top_path','restrain.top')
        self.force_constants = properties.get('force_constants','500 500 500')
        self.ref_rest_chain_triplet_list = properties.get('ref_rest_chain_triplet_list', None)
        # Common in all BB
        self.gmx_path = properties.get('gmx_path','gmx')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')

    def launch(self):
        """Launch the topology generation.
        """
        out_log, _ = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)
        self.output_top_path = fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name=self.output_top_path)

        fu.unzip_top(zip_file=self.input_top_zip_path, top_file=self.output_top_path, out_log=out_log)


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
        out_log.info('Index_dic: '+str(index_dic))

        self.ref_rest_chain_triplet_list = [tuple(elem.strip(' ()').replace(' ', '').split(',')) for elem in self.ref_rest_chain_triplet_list.split('),')]
        for reference_group, restrain_group, chain in self.ref_rest_chain_triplet_list:
            out_log.info('Reference group: '+reference_group)
            out_log.info('Restrain group: '+restrain_group)
            out_log.info('Chain: '+chain)
            self.output_itp_path = fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name=restrain_group+'.itp')

            # Mapping atoms from absolute enumeration to Chain relative enumeration
            out_log.info('reference_group_index: start_closed:'+str(index_dic['[ '+reference_group+' ]'][0]+1)+' stop_open: '+str(index_dic['[ '+reference_group+' ]'][1]))
            reference_group_list = [ int(elem) for line in lines[index_dic['[ '+reference_group+' ]'][0]+1: index_dic['[ '+reference_group+' ]'][1]] for elem in line.split() ]
            out_log.info('restrain_group_index: start_closed:'+str(index_dic['[ '+restrain_group+' ]'][0]+1)+' stop_open: '+str(index_dic['[ '+restrain_group+' ]'][1]))
            restrain_group_list = [ int(elem) for line in lines[index_dic['[ '+restrain_group+' ]'][0]+1: index_dic['[ '+restrain_group+' ]'][1]] for elem in line.split() ]
            selected_list = [reference_group_list.index(atom)+1 for atom in restrain_group_list]

            # Creating new ITP with restrictions
            with open(self.output_itp_path, 'w') as f:
                    out_log.info('Creating: '+str(f)+' and adding the selected atoms force constants')
                    f.write('[ position_restraints ]\n')
                    f.write('; atom  type      fx      fy      fz\n')
                    for atom in selected_list:
                        f.write(str(atom)+'     1  '+self.force_constants+'\n')

            # Including new ITP in the corresponding ITP-chain file
            for file_name in os.listdir('.'):
                if not file_name.startswith("posre") and not file_name.endswith("_pr.itp"):
                    if fnmatch.fnmatch(file_name, "*_chain_"+chain+".itp"):
                        with open(file_name, 'a') as f:
                            out_log.info('Opening: '+str(f)+' and adding the ifdef include statement')
                            f.write('\n')
                            f.write('; Include Position restraint file\n')
                            f.write('#ifdef CUSTOM_POSRES\n')
                            f.write('#include "'+self.output_itp_path+'"\n')
                            f.write('#endif\n')

        # zip topology
        fu.zip_top(zip_file=self.output_top_zip_path, out_log=out_log)
        return 0

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS extra ndx2resttop module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_ndx_path', required=True)
    parser.add_argument('--input_top_zip_path', required=True)
    parser.add_argument('--output_top_zip_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Ndx2resttop(input_ndx_path=args.input_ndx_path, input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
