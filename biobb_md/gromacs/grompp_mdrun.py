#!/usr/bin/env python3

"""Module containing the GromppMDrun class and the command line interface."""
import os
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_md.gromacs.common import get_gromacs_version
from biobb_md.gromacs.common import GromacsVersionError
from biobb_md.gromacs.grompp import Grompp
from biobb_md.gromacs.mdrun import Mdrun


class GromppMdrun:
    """
        | biobb_md.gromacs.grompp_mdrun GromppMdrun
        | Wrapper of the `GROMACS grompp <http://manual.gromacs.org/current/onlinehelp/gmx-grompp.html>`_ module and the `GROMACS mdrun <http://manual.gromacs.org/current/onlinehelp/gmx-mdrun.html>`_ module.
        | Grompp The GROMACS preprocessor module needs to be fed with the input system and the dynamics parameters to create a portable binary run input file TPR. The dynamics parameters are specified in the mdp section of the configuration YAML file. The parameter names and defaults are the same as the ones in the `official MDP specification <http://manual.gromacs.org/current/user-guide/mdp-options.html>`_. MDRun is the main computational chemistry engine within GROMACS. It performs Molecular Dynamics simulations, but it can also perform Stochastic Dynamics, Energy Minimization, test particle insertion or (re)calculation of energies.

    Args:
        input_gro_path (str): Path to the input GROMACS structure GRO file. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.gro>`_. Accepted formats: gro (edam:format_2033).
        input_top_zip_path (str): Path to the input GROMACS topology TOP and ITP files in zip format. File type: input. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.zip>`_. Accepted formats: zip (edam:format_3987).
        output_tpr_path (str): Path to the output portable binary run file TPR. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_grompp.tpr>`_. Accepted formats: tpr (edam:format_2333).
        output_trr_path (str): Path to the GROMACS uncompressed raw trajectory file TRR. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.trr>`_. Accepted formats: trr (edam:format_3910).
        output_gro_path (str): Path to the output GROMACS structure GRO file. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.gro>`_. Accepted formats: gro (edam:format_2033).
        output_edr_path (str): Path to the output GROMACS portable energy file EDR. File type: output. `Sample file <https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.edr>`_. Accepted formats: edr (edam:format_2330).
        output_log_path (str): Path to the output GROMACS trajectory log file LOG. File type: output. Accepted formats: log (edam:format_2330).
        input_cpt_path (str) (Optional): Path to the input GROMACS checkpoint file CPT. File type: input. Accepted formats: cpt (edam:format_2333).
        input_ndx_path (str) (Optional): Path to the input GROMACS index files NDX. File type: input. Accepted formats: ndx (edam:format_2330).
        input_mdp_path (str) (Optional): Path to the input GROMACS `MDP file <http://manual.gromacs.org/current/user-guide/mdp-options.html>`_. File type: input. Accepted formats: mdp (edam:format_2330).
        output_xtc_path (str) (Optional): Path to the GROMACS compressed trajectory file XTC. File type: output. Accepted formats: xtc (edam:format_3875).
        output_cpt_path (str) (Optional): Path to the output GROMACS checkpoint file CPT. File type: output. Accepted formats: cpt (edam:format_2333).
        output_dhdl_path (str) (Optional): Path to the output dhdl.xvg file only used when free energy calculation is turned on. File type: output. Accepted formats: xvg (edam:format_2033).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **mdp** (*dict*) - (defaults dict) MDP options specification. (Used if *input_mdp_path* is None)
                * **type** (*str*) - ("minimization") Default options for the mdp file. Each creates a different mdp file. Values: `minimization <https://biobb-md.readthedocs.io/en/latest/_static/mdp/minimization.mdp>`_ (Creates a minimization), `nvt <https://biobb-md.readthedocs.io/en/latest/_static/mdp/nvt.mdp>`_ (Creates a nvt), `npt <https://biobb-md.readthedocs.io/en/latest/_static/mdp/npt.mdp>`_ (Creates a npt), `free <https://biobb-md.readthedocs.io/en/latest/_static/mdp/free.mdp>`_ (Creates a free MD), index (Creates an empty mdp file).
            * **maxwarn** (*int*) - (10) [0-1000|1] Maximum number of allowed warnings.
            * **num_threads** (*int*) - (0) [0-1000|1] Let GROMACS guess. The number of threads that are going to be used.
            * **use_gpu** (*bool*) - (False) Use settings appropriate for GPU. Adds: -nb gpu -pme gpu
            * **mpi_bin** (*str*) - (None) Path to the MPI runner. Usually "mpirun" or "srun".
            * **mpi_np** (*str*) - (None) Number of MPI processes. Usually an integer bigger than 1.
            * **mpi_hostlist** (*str*) - (None) Path to the MPI hostlist file.
            * **gmx_lib** (*str*) - (None) Path set GROMACS GMXLIB environment variable.
            * **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.


    Info:
        * wrapped_software:
            * name: GROMACS Grompp & MDRun
            * version: >5.1
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_gro_path: str, input_top_zip_path: str, output_tpr_path: str,
                 input_tpr_path: str, output_trr_path: str, output_gro_path: str, output_edr_path: str,
                 output_log_path: str, input_cpt_path: str = None, input_ndx_path: str = None,
                 input_mdp_path: str = None,  output_xtc_path: str = None, output_cpt_path: str = None,
                 output_dhdl_path: str = None, properties: dict = None, **kwargs) -> None:
        # Properties management
        properties = properties or {}
        grompp_properties_keys = ['mdp', 'maxwarn']
        mdrun_properties_keys = ['num_threads', 'use_gpu', 'mpi_bin', 'mpi_np', 'mpi_hostlist', 'dev']
        self.properties_grompp = {}
        self.properties_mdrun = {}
        if properties:
            self.global_log = properties.get('global_log', None)
            self.properties_grompp = properties.copy()
            for key in mdrun_properties_keys:
                self.properties_grompp.pop(key, None)
            self.properties_mdrun = properties.copy()
            for key in grompp_properties_keys:
                self.properties_mdrun.pop(key, None)

        # Grompp arguments
        self.input_gro_path = input_gro_path
        self.input_top_zip_path = input_top_zip_path
        self.output_tpr_path = output_tpr_path
        self.input_cpt_path = input_cpt_path
        self.input_ndx_path = input_ndx_path
        self.input_mdp_path = input_mdp_path

        # MDRun arguments
        self.input_tpr_path = input_tpr_path
        self.output_trr_path = output_trr_path
        self.output_gro_path = output_gro_path
        self.output_edr_path = output_edr_path
        self.output_log_path = output_log_path
        self.output_xtc_path = output_xtc_path
        self.output_cpt_path = output_cpt_path
        self.output_dhdl_path = output_dhdl_path

    @launchlogger
    def launch(self) -> int:
        """Launches the execution of the GROMACS grompp and mdrun modules."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        fu.log(f'Calling Grompp class', out_log, self.global_log)
        grompp_return_code = Grompp(input_gro_path=self.input_gro_path, input_top_zip_path=self.input_top_zip_path,
                                    output_tpr_path=self.output_tpr_path, input_cpt_path=self.input_cpt_path,
                                    input_ndx_path=self.input_ndx_path, input_mdp_path=self.input_mdp_path,
                                    properties=self.properties_grompp).launch()
        fu.log(f'Grompp return code: {grompp_return_code}', out_log, self.global_log)

        if not grompp_return_code:
            fu.log(f'Grompp return code is correct. Calling MDRun class', out_log, self.global_log)
            mdrun_return_code = Mdrun(input_tpr_path=self.output_tpr_path, output_trr_path=self.output_trr_path,
                                      output_gro_path=self.output_gro_path, output_edr_path=self.output_edr_path,
                                      output_log_path=self.output_log_path, output_xtc_path=self.output_xtc_path,
                                      output_cpt_path=self.output_cpt_path, output_dhdl_path=self.output_dhdl_path,
                                      properties=self.properties_mdrun).launch()
            fu.log(f'MDRun return code: {mdrun_return_code}', out_log, self.global_log)
        else:
            return 1

        return mdrun_return_code


def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS mdrun module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_tpr_path', required=True)
    required_args.add_argument('--output_trr_path', required=True)
    required_args.add_argument('--output_gro_path', required=True)
    required_args.add_argument('--output_edr_path', required=True)
    required_args.add_argument('--output_log_path', required=True)
    parser.add_argument('--output_xtc_path', required=False)
    parser.add_argument('--output_cpt_path', required=False)
    parser.add_argument('--output_dhdl_path', required=False)

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    Mdrun(input_tpr_path=args.input_tpr_path, output_trr_path=args.output_trr_path,
          output_gro_path=args.output_gro_path, output_edr_path=args.output_edr_path,
          output_log_path=args.output_log_path, output_xtc_path=args.output_xtc_path,
          output_cpt_path=args.output_cpt_path, output_dhdl_path=args.output_dhdl_path,
          properties=properties).launch()


if __name__ == '__main__':
    main()
