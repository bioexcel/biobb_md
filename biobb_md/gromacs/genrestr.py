#!/usr/bin/env python3

"""Module containing the Genrestr class and the command line interface."""
import re
import os
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError

class Genrestr():
    """Wrapper class for the GROMACS genrestr (http://manual.gromacs.org/current/onlinehelp/gmx-genrestr.html) module.

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
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = input_structure_path
        self.input_ndx_path = input_ndx_path
        self.input_top_zip_path = input_top_zip_path
        self.output_top_zip_path = output_top_zip_path

        # Properties specific for BB
        self.output_itp_path = properties.get('output_itp_path','restrain.itp')
        self.output_top_path = properties.get('output_top_path','restrain.top')
        self.force_constants = str(properties.get('force_constants','500 500 500'))
        self.restricted_group = properties.get('restricted_group', 'system')

        # Properties common in all GROMACS BB
        self.gmx_path = properties.get('gmx_path', 'gmx')
        self.gmx_version = get_gromacs_version(self.gmx_path)

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

        # Check the properties
        fu.check_properties(self, properties)

    def launch(self):
        """Launches the execution of the GROMACS genrestr module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)
        if self.gmx_version < 512:
            raise GromacsVersionError("Gromacs version should be 5.1.2 or newer %d detected" % self.gmx_version)
        fu.log("GROMACS %s %d version detected" % (self.__class__.__name__, self.gmx_version), out_log)

        self.output_itp_path = fu.create_name(prefix=self.prefix, step=self.step, name=self.output_itp_path)

        fu.log('Adding restraints for atoms in group: %s using a force constant of: %s' % (self.restricted_group, self.force_constants), out_log, self.global_log)

        cmd = ['echo', '\"'+self.restricted_group+'\"', '|',
               self.gmx_path, "genrestr",
               "-f", self.input_structure_path,
               "-n", self.input_ndx_path,
               "-o", self.output_itp_path,
               "-fc", self.force_constants]

        command = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log)
        returncode = command.launch()

        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=out_log)
        # Find ITP file name in the topology
        with open(top_file, 'r') as fin:
            for line in fin:
                if line.startswith('#ifdef POSRES'):
                    itp_name = re.findall('"([^"]*)"',next(fin))[0]
                    break
        # Overwrite the content of the ITP file in the topology with the
        # content of the ITP file created with genrest.
        with open(self.output_itp_path, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(os.path.join(os.path.dirname(top_file),itp_name), 'w') as fout:
            fout.writelines(data)
        # Remove the ITP file created with genrest.
        os.remove(self.output_itp_path)
        # zip topology
        fu.zip_top(zip_file=self.output_top_zip_path, top_file=top_file, out_log=out_log)

        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS genion module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure_path', required=True)
    required_args.add_argument('--input_ndx_path', required=True)
    required_args.add_argument('--input_top_zip_path', required=True)
    required_args.add_argument('--output_top_zip_path', required=True)
    ####

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Genrestr(input_structure_path=args.input_structure_path, input_ndx_path=args.input_ndx_path, input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
