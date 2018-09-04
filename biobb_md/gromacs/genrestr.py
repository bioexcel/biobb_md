#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
import re
import os

class Genrestr(object):
    """Wrapper class for the GROMACS genrestr module.

    Args:
        input_structure_path (str): Path to the input structure PDB, GRO or TPR format.
        input_ndx_path (str): Path to the input GROMACS index file, NDX format.
        input_top_zip_path (str): Path the input TOP topology in zip format.
        output_top_zip_path (str): Path the output TOP topology in zip format.
        properties (dic):
            | - **output_top_path** (*str*) - ("restrain.top") Path the output TOP file.
            | - **output_itp_path** (*str*) - ("restrain.itp") Path to the output include for topology ITP file.
            | - **force_constants** (*str*) - ("500 500 500") Array of three floats defining the force constants
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.

    """

    def __init__(self, input_structure_path, input_ndx_path, input_top_zip_path,
                 output_top_zip_path, properties, **kwargs):
        self.input_structure_path = input_structure_path
        self.input_ndx_path = input_ndx_path
        self.input_top_zip_path = input_top_zip_path
        self.output_top_zip_path = output_top_zip_path
        # Properties specific for BB
        self.output_itp_path = properties.get('output_itp_path','restrain.itp')
        self.output_top_path = properties.get('output_top_path','restrain.top')
        self.force_constants = str(properties.get('force_constants','500 500 500'))
        self.restricted_group = properties.get('restricted_group', 'system')
        # Common in all BB
        self.gmx_path = properties.get('gmx_path','gmx')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')

    def launch(self):
        """Launches the execution of the GROMACS genrestr module.
        """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)
        self.output_top_path = fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name=self.output_top_path)
        self.output_itp_path = fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name=self.output_itp_path)

        out_log.info('Adding restraints for atoms in group: '+self.restricted_group+' using a force constant of: '+self.force_constants)
        if self.global_log:
            self.global_log.info(fu.get_logs_prefix()+'Adding restraints for atoms in group: '+self.restricted_group+' using a force constant of: '+self.force_constants)

        cmd = ['echo', '\"'+self.restricted_group+'\"', '|',
               self.gmx_path, "genrestr",
               "-f", self.input_structure_path,
               "-n", self.input_ndx_path,
               "-o", self.output_itp_path,
               "-fc", self.force_constants]

        command = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log)
        returncode = command.launch()

        fu.unzip_top(zip_file=self.input_top_zip_path, top_file=self.output_top_path, out_log=out_log)
        # Find ITP file name in the topology
        with open(self.output_top_path, 'r') as fin:
            for line in fin:
                if line.startswith('#ifdef POSRES'):
                    itp_name = re.findall('"([^"]*)"',next(fin))[0]
                    break
        # Overwrite the content of the ITP file in the topology with the
        # content of the ITP file created with genrest.
        with open(self.output_itp_path, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(itp_name, 'w') as fout:
            fout.writelines(data)
        # Remove the ITP file created with genrest.
        os.remove(self.output_itp_path)
        # zip topology
        fu.zip_top(zip_file=self.output_top_zip_path, out_log=out_log)

        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS genion module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_structure_path', required=True)
    parser.add_argument('--input_ndx_path', required=True)
    parser.add_argument('--input_top_zip_path', required=True)
    parser.add_argument('--output_top_zip_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Genrestr(input_structure_path=args.input_structure_path, input_ndx_path=args.input_ndx_path, input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
