#!/usr/bin/env python
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

class Grompp(object):
    """Wrapper of the GROMACS grompp module.
    The GROMACS preprocessor module needs to be feeded with the input system
    and the dynamics parameters to create a portable binary run input file TPR.
    The dynamics parameters are specified in the mdp section of the
    configuration YAML file. The parameter names and defaults are the same as
    the ones in the official MDP specification: http://manual.gromacs.org/current/online/mdp_opt.html

    Args:
        input_gro_path (str): Path to the input GROMACS structure GRO file.
        input_top_zip_path (str): Path the input GROMACS topology TOP and ITP files in zip format.
        output_tpr_path (str): Path to the output portable binary run file TPR.
        input_cpt_path (str)[Optional]: Path to the input GROMACS checkpoint file CPT.
        properties (dic):
            | - **input_mdp_path** (*str*) - (None) Path of the input MDP file.
            | - **mdp** (*dict*) - (defaults dict) MDP options specification. (Used if *input_mdp_path* is None)
                | - **type** (*str*) - ("minimization") Default options for the mdp file. Valid values: minimization, nvt, npt, free, index
            | - **output_mdp_path** (*str*) - ("grompp.mdp") Path of the output MDP file.
            | - **output_top_path** (*str*) - ("grompp.top") Path the output topology TOP file.
            | - **maxwarn** (*int*) - (10) Maximum number of allowed warnings.
            | - **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_gro_path, input_top_zip_path,
                 output_tpr_path, input_cpt_path=None, properties=None, **kwargs):
        self.input_gro_path = input_gro_path
        self.input_top_zip_path = input_top_zip_path
        self.output_tpr_path = output_tpr_path
        self.input_cpt_path = input_cpt_path
        # Properties specific for BB
        self.input_mdp_path= properties.get('input_mdp_path', None)
        self.output_mdp_path= properties.get('output_mdp_path', 'grompp.mdp')
        self.output_top_path = properties.get('output_top_path','grompp.top')
        self.maxwarn = str(properties.get('maxwarn', 10))
        self.mdp = {k: str(v) for k, v in properties.get('mdp', dict()).items()}
        # Common in all BB
        self.gmx_path = properties.get('gmx_path','gmx')
        self.global_log= properties.get('global_log', None)
        self.prefix = properties.get('prefix',None)
        self.step = properties.get('step',None)
        self.path = properties.get('path','')
        #TODO Check this two attributes
        self.nsteps=''
        self.dt=''


    def create_mdp(self):
        """Creates an MDP file using the properties file settings
        """

        mdp_list=[]
        self.output_mdp_path=fu.create_name(path=self.path, prefix=self.prefix, step=self.step, name=self.output_mdp_path)

        sim_type = self.mdp.get('type', 'minimization')
        minimization = (sim_type == 'minimization')
        nvt = (sim_type == 'nvt')
        npt = (sim_type == 'npt')
        free = (sim_type == 'free')
        index = (sim_type == 'index')
        md = (nvt or npt or free)
        mdp_list.append(";Type of MDP: " + sim_type)

        # Position restrain
        if not free:
            mdp_list.append("\n;Position restrain")
            mdp_list.append("Define = " + self.mdp.pop('define', '-DPOSRES'))

        # Run parameters
        mdp_list.append("\n;Run parameters")
        self.nsteps= self.mdp.pop('nsteps', '5000')
        mdp_list.append("nsteps = " + self.nsteps)
        if minimization:
            mdp_list.append("integrator = " + self.mdp.pop('integrator', 'steep'))
            mdp_list.append("emtol = " + self.mdp.pop('emtol', '1000.0'))
            mdp_list.append("emstep = " + self.mdp.pop('emstep', '0.01'))
        if md:
            mdp_list.append("integrator = " + self.mdp.pop('integrator', 'md'))
            self.dt=self.mdp.pop('dt', '0.002')
            mdp_list.append("dt = " + self.dt)

        # Output control
        if md:
            mdp_list.append("\n;Output control")
            if nvt or npt:
                mdp_list.append("nstxout = " + self.mdp.pop('nstxout',   '500'))
                mdp_list.append("nstvout = " + self.mdp.pop('nstvout',   '500'))
                mdp_list.append("nstenergy = " + self.mdp.pop('nstenergy', '500'))
                mdp_list.append("nstlog = " + self.mdp.pop('nstlog',    '500'))
                mdp_list.append("nstcalcenergy = " + self.mdp.pop('nstcalcenergy', '100'))
                mdp_list.append("nstcomm = " + self.mdp.pop('nstcomm', '100'))
                mdp_list.append("nstxout-compressed = " + self.mdp.pop('nstxout-compressed', '1000'))
                mdp_list.append("compressed-x-precision = " + self.mdp.pop('compressed-x-precision', '1000'))
                mdp_list.append("compressed-x-grps = " + self.mdp.pop('compressed-x-grps', 'System'))
            if free:
                mdp_list.append("nstcomm = " + self.mdp.pop('nstcomm', '100'))
                mdp_list.append("nstxout = " + self.mdp.pop('nstxout',   '5000'))
                mdp_list.append("nstvout = " + self.mdp.pop('nstvout',   '5000'))
                mdp_list.append("nstenergy = " + self.mdp.pop('nstenergy', '5000'))
                mdp_list.append("nstlog = " + self.mdp.pop('nstlog',    '5000'))
                mdp_list.append("nstcalcenergy = " + self.mdp.pop('nstcalcenergy', '100'))
                mdp_list.append("nstxout-compressed = " + self.mdp.pop('nstxout-compressed', '1000'))
                mdp_list.append("compressed-x-grps = " + self.mdp.pop('compressed-x-grps', 'System'))
                mdp_list.append("compressed-x-precision = " + self.mdp.pop('compressed-x-precision', '1000'))

        # Bond parameters
        if md:
            mdp_list.append("\n;Bond parameters")
            mdp_list.append("constraint_algorithm = " + self.mdp.pop('constraint_algorithm', 'lincs'))
            mdp_list.append("constraints = " + self.mdp.pop('constraints', 'all-bonds'))
            mdp_list.append("lincs_iter = " + self.mdp.pop('lincs_iter', '1'))
            mdp_list.append("lincs_order = " + self.mdp.pop('lincs_order', '4'))
            if nvt:
                mdp_list.append("continuation = " + self.mdp.pop('continuation', 'no'))
            if npt or free:
                mdp_list.append("continuation = " + self.mdp.pop('continuation', 'yes'))


        # Neighbour searching
        mdp_list.append("\n;Neighbour searching")
        mdp_list.append("cutoff-scheme = " + self.mdp.pop('cutoff-scheme', 'Verlet'))
        mdp_list.append("ns_type = " + self.mdp.pop('ns_type', 'grid'))
        mdp_list.append("rcoulomb = " + self.mdp.pop('rcoulomb', '1.0'))
        mdp_list.append("vdwtype = " + self.mdp.pop('vdwtype', 'cut-off'))
        mdp_list.append("rvdw = " + self.mdp.pop('rvdw', '1.0'))
        mdp_list.append("nstlist = " + self.mdp.pop('nstlist', '10'))
        mdp_list.append("rlist = " + self.mdp.pop('rlist', '1'))

        # Eletrostatics
        mdp_list.append("\n;Eletrostatics")
        mdp_list.append("coulombtype = " + self.mdp.pop('coulombtype', 'PME'))
        if md:
            mdp_list.append("pme_order = " + self.mdp.pop('pme_order', '4'))
            mdp_list.append("fourierspacing = " + self.mdp.pop('fourierspacing', '0.12'))
            mdp_list.append("fourier_nx = " + self.mdp.pop('fourier_nx', '0'))
            mdp_list.append("fourier_ny = " + self.mdp.pop('fourier_ny', '0'))
            mdp_list.append("fourier_nz = " + self.mdp.pop('fourier_nz', '0'))
            mdp_list.append("ewald_rtol = " + self.mdp.pop('ewald_rtol', '1e-5'))

        # Temperature coupling
        if md:
            mdp_list.append("\n;Temperature coupling")
            mdp_list.append("tcoupl = " + self.mdp.pop('tcoupl', 'V-rescale'))
            mdp_list.append("tc-grps = " + self.mdp.pop('tc-grps', 'Protein Non-Protein'))
            mdp_list.append("tau_t = " + self.mdp.pop('tau_t', '0.1	  0.1'))
            mdp_list.append("ref_t = " + self.mdp.pop('ref_t', '300 	  300'))

        # Pressure coupling
        if md:
            mdp_list.append("\n;Pressure coupling")
            if nvt:
                mdp_list.append("pcoupl = " + self.mdp.pop('pcoupl', 'no'))
            if npt or free:
                mdp_list.append("pcoupl = " + self.mdp.pop('pcoupl', 'Parrinello-Rahman'))
                mdp_list.append("pcoupltype = " + self.mdp.pop('pcoupltype', 'isotropic'))
                mdp_list.append("tau_p = " + self.mdp.pop('tau_p', '1.0'))
                mdp_list.append("ref_p = " + self.mdp.pop('ref_p', '1.0'))
                mdp_list.append("compressibility = " + self.mdp.pop('compressibility', '4.5e-5'))
                mdp_list.append("refcoord_scaling = " + self.mdp.pop('refcoord_scaling', 'com'))


        # Dispersion correction
        if md:
            mdp_list.append("\n;Dispersion correction")
            mdp_list.append("DispCorr = " + self.mdp.pop('DispCorr', 'EnerPres'))

        # Velocity generation
        if md:
            mdp_list.append("\n;Velocity generation")
            if nvt:
                mdp_list.append("gen_vel = " + self.mdp.pop('gen_vel', 'yes'))
                mdp_list.append("gen_temp = " + self.mdp.pop('gen_temp', '300'))
                mdp_list.append("gen_seed = " + self.mdp.pop('gen_seed', '-1'))
            if npt or free:
                mdp_list.append("gen_vel = " + self.mdp.pop('gen_vel', 'no'))

        #Periodic boundary conditions
        mdp_list.append("\n;Periodic boundary conditions")
        mdp_list.append("pbc = " + self.mdp.pop('pbc', 'xyz'))

        if index:
            mdp_list =[";This mdp file has been created by the pymdsetup.gromacs_wrapper.grompp.create_mdp()"]

        mdp_list.insert(0, ";This mdp file has been created by the pymdsetup.gromacs_wrapper.grompp.create_mdp()")

        # Adding the rest of parameters in the config file to the MDP file
        for k, v in self.mdp.items():
            if k != 'type':
                mdp_list.append(str(k) + ' = '+str(v))

        with open(self.output_mdp_path, 'w') as mdp:
            for line in mdp_list:
                mdp.write(line + '\n')

        return self.output_mdp_path

    def launch(self):
        """Launches the execution of the GROMACS grompp module.
        """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step)
        self.output_mdp_path = self.create_mdp() if self.input_mdp_path is None else self.input_mdp_path

        if self.global_log is not None:
            md = self.mdp.get('type', 'minimization')
            if md != 'index' and md != 'free':
                out_log.info('Will run a '+md+' md of ' + str(self.nsteps) +' steps')
                self.global_log.info(fu.get_logs_prefix()+'Will run a '+md+' md of ' + str(self.nsteps) +' steps')
            elif md == 'index':
                out_log.info('Will create a TPR to be used as structure file')
                self.global_log.info(fu.get_logs_prefix()+'Will create a TPR to be used as structure file')
            else:
                out_log.info('Will run a '+md+' md of ' + fu.human_readable_time(int(self.nsteps)*float(self.dt)))
                self.global_log.info(fu.get_logs_prefix()+'Will run a '+md+' md of ' + fu.human_readable_time(int(self.nsteps)*float(self.dt)))

        fu.unzip_top(zip_file=self.input_top_zip_path, top_file=self.output_top_path, out_log=out_log)

        cmd = [self.gmx_path, 'grompp',
               '-f', self.output_mdp_path,
               '-c', self.input_gro_path,
               '-r', self.input_gro_path,
               '-p', self.output_top_path,
               '-o', self.output_tpr_path,
               '-maxwarn', self.maxwarn]

        if self.input_cpt_path:
            cmd.append('-t')
            cmd.append(self.input_cpt_path)

        return cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the GROMACS grompp module.")
    parser.add_argument('--conf_file', required=True)
    parser.add_argument('--system', required=True)
    parser.add_argument('--step', required=True)

    #Specific args of each building block
    parser.add_argument('--input_gro_path', required=True)
    parser.add_argument('--input_top_zip_path', required=True)
    parser.add_argument('--output_tpr_path', required=True)
    parser.add_argument('--input_cpt_path', required=False)
    ####

    args = parser.parse_args()
    properties = settings.YamlReader(conf_file_path=args.conf_file, system=args.system).get_prop_dic()[args.step]

    #Specific call of each building block
    Grompp(input_gro_path=args.input_gro_path, input_top_zip_path=args.input_top_zip_path, output_tpr_path=args.output_tpr_path, input_cpt_path=args.input_cpt_path, properties=properties).launch()
    ####

if __name__ == '__main__':
    main()
