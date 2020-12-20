#!/usr/bin/env python3

"""Module containing the Ndx2resttop class and the command line interface."""
import fnmatch
import argparse
from pathlib import Path
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class Ndx2resttop:
    """
    | biobb_md Ndx2resttop
    | Generate a restrained topology from an index NDX file.
    | This module automatizes the process of restrained topology generation starting from an index NDX file.

    Args:
        input_ndx_path (str): Path to the input NDX index file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs_extra/ndx2resttop.ndx>`_. Accepted formats: ndx (edam:format_2330).
        input_top_zip_path (str): Path the input TOP topology in zip format. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs_extra/ndx2resttop.zip>`_. Accepted formats: zip (edam:format_3987).
        output_top_zip_path (str): Path the output TOP topology in zip format. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs_extra/ref_ndx2resttop.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **force_constants** (*str*) - ("500 500 500") Array of three floats defining the force constants.
            * **ref_rest_chain_triplet_list** (*str*) - (None) Triplet list composed by (reference group, restrain group, chain) list.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_md.gromacs_extra.ndx2resttop import ndx2resttop
            prop = { 'ref_rest_chain_triplet_list': '( Chain_A, Chain_A_noMut, A ), ( Chain_B, Chain_B_noMut, B ), ( Chain_C, Chain_C_noMut, C ), ( Chain_D, Chain_D_noMut, D )' }
            ndx2resttop(input_ndx_path='/path/to/myIndex.ndx',
                        input_top_zip_path='/path/to/myTopology.zip',
                        output_top_zip_path='/path/to/newTopology.zip',
                        properties=prop)

    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_ndx_path: str, input_top_zip_path: str, output_top_zip_path: str,
                 properties: dict = None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {"input_ndx_path": input_ndx_path, "input_top_zip_path": input_top_zip_path},
            "out": {"output_top_zip_path": output_top_zip_path}
        }

        # Properties specific for BB
        self.force_constants = properties.get('force_constants', '500 500 500')
        self.ref_rest_chain_triplet_list = properties.get('ref_rest_chain_triplet_list')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # Check the properties
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Ndx2resttop <gromacs_extra.ndx2resttop.Ndx2resttop>` object."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Restart if needed
        if self.restart:
            output_file_list = [self.io_dict['out'].get("output_top_zip_path")]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        top_file = fu.unzip_top(zip_file=self.io_dict['in'].get("input_top_zip_path"), out_log=out_log)

        # Create index list of index file :)
        index_dic = {}
        lines = open(self.io_dict['in'].get("input_ndx_path")).read().splitlines()
        for index, line in enumerate(lines):
            if line.startswith('['):
                index_dic[line] = index,
                label = line
                if index > 0:
                    index_dic[label] = index_dic[label][0], index
        index_dic[label] = index_dic[label][0], index
        fu.log('Index_dic: '+str(index_dic), out_log, self.global_log)

        self.ref_rest_chain_triplet_list = [tuple(elem.strip(' ()').replace(' ', '').split(',')) for elem in self.ref_rest_chain_triplet_list.split('),')]
        fu.log('ref_rest_chain_triplet_list: ' + str(self.ref_rest_chain_triplet_list), out_log, self.global_log)
        for reference_group, restrain_group, chain in self.ref_rest_chain_triplet_list:
            fu.log('Reference group: '+reference_group, out_log, self.global_log)
            fu.log('Restrain group: '+restrain_group, out_log, self.global_log)
            fu.log('Chain: '+chain, out_log, self.global_log)
            self.io_dict['out']["output_itp_path"] = fu.create_name(path=str(Path(top_file).parent), prefix=self.prefix, step=self.step, name=restrain_group+'.itp')

            # Mapping atoms from absolute enumeration to Chain relative enumeration
            fu.log('reference_group_index: start_closed:'+str(index_dic['[ '+reference_group+' ]'][0]+1)+' stop_open: '+str(index_dic['[ '+reference_group+' ]'][1]), out_log, self.global_log)
            reference_group_list = [int(elem) for line in lines[index_dic['[ '+reference_group+' ]'][0]+1: index_dic['[ '+reference_group+' ]'][1]] for elem in line.split()]
            fu.log('restrain_group_index: start_closed:'+str(index_dic['[ '+restrain_group+' ]'][0]+1)+' stop_open: '+str(index_dic['[ '+restrain_group+' ]'][1]), out_log, self.global_log)
            restrain_group_list = [int(elem) for line in lines[index_dic['[ '+restrain_group+' ]'][0]+1: index_dic['[ '+restrain_group+' ]'][1]] for elem in line.split()]
            selected_list = [reference_group_list.index(atom)+1 for atom in restrain_group_list]
            # Creating new ITP with restrictions
            with open(self.io_dict['out'].get("output_itp_path"), 'w') as f:
                fu.log('Creating: '+str(f)+' and adding the selected atoms force constants', out_log, self.global_log)
                f.write('[ position_restraints ]\n')
                f.write('; atom  type      fx      fy      fz\n')
                for atom in selected_list:
                    f.write(str(atom)+'     1  '+self.force_constants+'\n')

            # Including new ITP in the corresponding ITP-chain file
            for file_dir in Path(top_file).parent.iterdir():
                if not file_dir.name.startswith("posre") and not file_dir.name.endswith("_pr.itp"):
                    if fnmatch.fnmatch(str(file_dir), "*_chain_"+chain+".itp"):
                        with open(str(file_dir), 'a') as f:
                            fu.log('Opening: '+str(f)+' and adding the ifdef include statement', out_log, self.global_log)
                            f.write('\n')
                            f.write('; Include Position restraint file\n')
                            f.write('#ifdef CUSTOM_POSRES\n')
                            f.write('#include "'+str(Path(self.io_dict['out'].get("output_itp_path")).name)+'"\n')
                            f.write('#endif\n')

        # zip topology
        fu.zip_top(zip_file=self.io_dict['out'].get("output_top_zip_path"), top_file=top_file, out_log=out_log)

        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return 0


def ndx2resttop(input_ndx_path: str, input_top_zip_path: str, output_top_zip_path: str,
                properties: dict = None, **kwargs) -> int:
    """Create :class:`Ndx2resttop <gromacs_extra.ndx2resttop.Ndx2resttop>` class and
    execute the :meth:`launch() <gromacs_extra.ndx2resttop.Ndx2resttop.launch>` method."""
    return Ndx2resttop(input_ndx_path=input_ndx_path,
                       input_top_zip_path=input_top_zip_path,
                       output_top_zip_path=output_top_zip_path,
                       properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS extra ndx2resttop module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_ndx_path', required=True)
    required_args.add_argument('--input_top_zip_path', required=True)
    required_args.add_argument('--output_top_zip_path', required=True)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    ndx2resttop(input_ndx_path=args.input_ndx_path, input_top_zip_path=args.input_top_zip_path,
                output_top_zip_path=args.output_top_zip_path, properties=properties)


if __name__ == '__main__':
    main()
