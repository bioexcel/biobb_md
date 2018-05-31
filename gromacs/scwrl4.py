#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
import os
import re
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import PDBIO

class Scwrl4(object):
    """Wrapper class for the 4.0 version of SCWRL and mutation modeling.

    Args:
        input_pdb_path (str): Path to the input PDB file.
        output_pdb_path (srt): Path to the output mutated PDB file.
        properties (dic):
            | - **mutation** (*str*) - Mutation in the format "Chain.WT_AA_ThreeLeterCode.Resnum.MUT_AA_ThreeLeterCode" If "ALL" is provided as chain code all the chains in the pdb file will be mutated. ie: "A.ALA15CYS"
    """
    def __init__(self, input_pdb_path, output_pdb_path, properties, **kwargs):
        self.input_pdb_path = os.path.abspath(input_pdb_path)
        self.output_pdb_path = output_pdb_path
        self.scwrl4_path = properties.get('scwrl4_path', 'Scwrl4')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')
        self.mutation = properties.get('mutation', None)
        if self.mutation:
            if self.mutation.strip() == '':
                self.mutation = None
            else:
                pattern = re.compile(("(?P<chain>[a-zA-Z*]+).(?P<wt>[a-zA-Z]{3})(?P<resnum>\d+)(?P<mt>[a-zA-Z]{3})"))
                self.mut_dict = pattern.match(self.mutation).groupdict()

    def launch(self):
        """Launches the execution of the SCWRL binary.
        All the missing heavy atoms are added.
        If `self.mutation` is provided the mutation is modeled.
        """

        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)
        if self.mutation:
            # Read structure with Biopython
            parser = PDBParser(PERMISSIVE=1,QUIET=True)
            st = parser.get_structure('s', self.input_pdb_path)  # s random id never used

            if self.mut_dict['chain'] != 'ALL':
                chains = [self.mut_dict['chain']]
            else:
                chains = [chain.id for chain in st[0]]

            resnum = int(self.mut_dict['resnum'])

            sequence=''
            for chain in chains:
                out_log.info('Replacing: '+self.mut_dict['wt']+' number: '+self.mut_dict['resnum']+' by: '+self.mut_dict['mt'])
                if self.global_log:
                    self.global_log.info(22*' '+'Replacing: '+self.mut_dict['wt']+' number: '+self.mut_dict['resnum']+' by: '+self.mut_dict['mut'])
                residue = st[0][chain][(' ', resnum, ' ')]
                backbone_atoms = ['N', 'CA', 'C', 'O', 'CB']
                not_backbone_atoms = []

                # The following formula does not work. Biopython bug?
                # for atom in residue:
                #     if atom.id not in backbone_atoms:
                #         residue.detach_child(atom.id)

                for atom in residue:
                    if atom.id not in backbone_atoms:
                        not_backbone_atoms.append(atom)
                for atom in not_backbone_atoms:
                    residue.detach_child(atom.id)

                # Change residue name
                residue.resname = self.mut_dict['mt'].upper()

                # Creating a sequence file where the lower case residues will
                # remain untouched and the upper case residues will be modified
                aa1c = { 'ALA':'A', 'CYS':'C', 'CYX':'C', 'ASP':'D', 'ASH':'D', 'GLU':'E', 'GLH':'E', 'PHE':'F', 'GLY':'G', 'HIS':'H', 'HID':'H', 'HIE':'H', 'HIP':'H', 'ILE':'I', 'LYS':'K', 'LYP':'K', 'LEU':'L', 'MET':'M', 'MSE':'M', 'ASN':'N', 'PRO':'P', 'HYP':'P', 'GLN':'Q', 'ARG':'R', 'SER':'S', 'THR':'T', 'VAL':'V', 'TRP':'W', 'TYR':'Y'}
                for res in st[0][chain].get_residues():
                    if res.resname not in aa1c:
                        st[0][chain].detach_child(res.id)
                    elif (res.id == (' ', resnum,' ')):
                        sequence += aa1c[res.resname].upper()
                    else:
                        sequence += aa1c[res.resname].lower()

            # Write resultant sequence
            sequence_file_path = fu.create_name(prefix=self.prefix, step=self.step, name="sequence.seq")
            with open(sequence_file_path, 'w') as sqfile:
                sqfile.write(sequence+"\n")

            out_log.info('Writting Scwrl4 sequence file '+sequence_file_path+' containing:')
            out_log.info(sequence)
            if self.global_log:
                self.global_log.info(22*' '+'Writting Scwrl4 sequence file '+sequence_file_path+' containing:')
                self.global_log.info(sequence)

            # Write resultant structure
            w = PDBIO()
            w.set_structure(st[0])
            prepared_file_path = fu.create_name(prefix=self.prefix, step=self.step, name="prepared.pdb")
            w.save(prepared_file_path)
            out_log.info('Writting modified Scwrl4 PDB input file to: '+prepared_file_path)
            if self.global_log:
                self.global_log.info(22*' '+'Writting modified Scwrl4 PDB input file to: '+prepared_file_path)

        else:
            prepared_file_path = self.input_pdb_path

        cmd = [self.scwrl4_path, '-i', prepared_file_path, '-o', self.output_pdb_path, '-h', '-t']
        if self.mutation:
            cmd.append('-s')
            cmd.append(sequence_file_path)

        command = cmd_wrapper.CmdWrapper(cmd, out_log, err_log)
        return command.launch()

def main():
    parser = argparse.ArgumentParser(description="Wrapper class for the 4.0 version of SCWRL and mutation modeling.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_pdb_path', required=True)
    parser.add_argument('--output_pdb_path', required=True)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Scwrl4(input_pdb_path=args.input_pdb_path, output_pdb_path=args.output_pdb_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
