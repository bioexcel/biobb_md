""" Common functions for package biobb_md.gromacs """
import re
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from typing import List, Dict, Tuple, Mapping, Union, Set, Sequence


def get_gromacs_version(gmx: str = "gmx") -> int:
    """ Gets the GROMACS installed version and returns it as an int(3) for
    versions older than 5.1.5 and an int(5) for 20XX versions filling the gaps
    with '0' digits.

    Args:
        gmx (str): ('gmx') Path to the GROMACS binary.

    Returns:
        int: GROMACS version.
    """
    unique_dir = fu.create_unique_dir()
    out_log, err_log = fu.get_logs(path=unique_dir, can_write_console=False)
    cmd = [gmx, "-version"]
    try:
        cmd_wrapper.CmdWrapper(cmd, out_log, err_log).launch()
        pattern = re.compile(r"GROMACS version:\s+(.+)")
        with open(Path(unique_dir).joinpath('log.out')) as log_file:
            for line in log_file:
                version_str = pattern.match(line.strip())
                if version_str:
                    break
        version = version_str.group(1).replace(".", "").replace("VERSION", "").strip()
        version = "".join([c for c in version if c.isdigit()])
    except:
        return 0
    if version.startswith("2"):
        while len(version) < 5:
            version += '0'
    else:
        while len(version) < 3:
            version += '0'

    fu.rm(unique_dir)
    return int(version)


class GromacsVersionError(Exception):
    """ Exception Raised when the installed version of GROMACS is not
        compatible with the current function.
    """
    # pass


def gmx_check(file_a: str, file_b: str, gmx: str = 'gmx') -> bool:
    print("Comparing GROMACS files:")
    print("FILE_A: %s" % str(Path(file_a).resolve()))
    print("FILE_B: %s" % str(Path(file_b).resolve()))
    check_result = 'check_result.out'
    cmd = [gmx, 'check']
    if file_a.endswith(".tpr"):
        cmd.append('-s1')
    else:
        cmd.append('-f')
    cmd.append(file_a)
    if file_b.endswith(".tpr"):
        cmd.append('-s2')
    else:
        cmd.append('-f2')
    cmd.append(file_b)
    cmd.append('> check_result.out')
    cmd_wrapper.CmdWrapper(cmd).launch()
    print("Result file: %s" % str(Path(check_result).resolve()))
    with open(check_result) as check_file:
        for line_num, line in enumerate(check_file):
            if not line.startswith('comparing'):
                print('Discrepance found in line %d: %s' % (line_num, line))
                return False
    return True


def gmx_rms(file_a: str, file_b: str, file_tpr: str, gmx: str = 'gmx', tolerance: float = 0.5):
    print("Comparing GROMACS files:")
    print("FILE_A: %s" % str(Path(file_a).resolve()))
    print("FILE_B: %s" % str(Path(file_b).resolve()))
    rmsd_result = 'rmsd.xvg'
    cmd = ['echo', '\"Protein Protein\"', '|',
           gmx, 'rms', '-s', file_tpr, '-f', file_a, '-f2', file_b, '-xvg', 'none']
    cmd_wrapper.CmdWrapper(cmd).launch()
    print("Result file: %s" % str(Path(rmsd_result).resolve()))
    with open(rmsd_result) as check_file:
        for line in check_file:
            time_step, rmsd = tuple(line.strip().split())
            if float(rmsd) > tolerance:
                print('RMSD: %s bigger than tolerance %g for time step %s' % (rmsd, tolerance, time_step))
                return False
    return True


def read_mdp(input_mdp_path: str) -> Dict[str, str]:
    # Credit for these two reg exps to:
    # https://github.com/Becksteinlab/GromacsWrapper/blob/master/gromacs/fileformats/mdp.py
    parameter_re = re.compile(r"\s*(?P<parameter>[^=]+?)\s*=\s*(?P<value>[^;]*)(?P<comment>\s*;.*)?", re.VERBOSE)

    mdp_dict = {}
    with open(input_mdp_path) as mdp_file:
        for line in mdp_file:
            re_match = parameter_re.match(line.strip())
            if re_match:
                parameter = re_match.group('parameter')
                value = re_match.group('value')
                mdp_dict[parameter] = value

    return mdp_dict


def mdp_preset(sim_type: str) -> Dict[str, str]:
    mdp_dict = {}
    if not sim_type or sim_type == 'index':
        return mdp_dict
    
    minimization = (sim_type == 'minimization') or (sim_type == 'ions')
    nvt = (sim_type == 'nvt')
    npt = (sim_type == 'npt')
    free = (sim_type == 'free')
    md = (nvt or npt or free)

    # Position restrain
    if not free:
        mdp_dict['Define'] = '-DPOSRES'

    # Run parameters
    mdp_dict['nsteps'] = '5000'
    if minimization:
        mdp_dict['integrator'] = 'steep'
        mdp_dict['emtol'] = '1000.0'
        mdp_dict['emstep'] = '0.01'
    if md:
        mdp_dict['integrator'] = 'md'
        mdp_dict['dt'] = '0.002'

    # Output control
    if md:
        if nvt or npt:
            mdp_dict['nstxout'] = '500'
            mdp_dict['nstvout'] = '500'
            mdp_dict['nstenergy'] = '500'
            mdp_dict['nstlog'] = '500'
            mdp_dict['nstcalcenergy'] = '100'
            mdp_dict['nstcomm'] = '100'
            mdp_dict['nstxout-compressed'] = '1000'
            mdp_dict['compressed-x-precision'] = '1000'
            mdp_dict['compressed-x-grps'] = 'System'
        if free:
            mdp_dict['nstcomm'] = '100'
            mdp_dict['nstxout'] = '5000'
            mdp_dict['nstvout'] = '5000'
            mdp_dict['nstenergy'] = '5000'
            mdp_dict['nstlog'] = '5000'
            mdp_dict['nstcalcenergy'] = '100'
            mdp_dict['nstxout-compressed'] = '1000'
            mdp_dict['compressed-x-grps'] = 'System'
            mdp_dict['compressed-x-precision'] = '1000'

    # Bond parameters
    if md:
        mdp_dict['constraint-algorithm'] = 'lincs'
        mdp_dict['constraints'] = 'h-bonds'
        mdp_dict['lincs-iter'] = '1'
        mdp_dict['lincs-order'] = '4'
        if nvt:
            mdp_dict['continuation'] = 'no'
        if npt or free:
            mdp_dict['continuation'] = 'yes'

    # Neighbour searching
    mdp_dict['cutoff-scheme'] = 'Verlet'
    mdp_dict['ns-type'] = 'grid'
    mdp_dict['rcoulomb'] = '1.0'
    mdp_dict['vdwtype'] = 'cut-off'
    mdp_dict['rvdw'] = '1.0'
    mdp_dict['nstlist'] = '10'
    mdp_dict['rlist'] = '1'

    # Electrostatics
    mdp_dict['coulombtype'] = 'PME'
    if md:
        mdp_dict['pme-order'] = '4'
        mdp_dict['fourierspacing'] = '0.12'
        mdp_dict['fourier-nx'] = '0'
        mdp_dict['fourier-ny'] = '0'
        mdp_dict['fourier-nz'] = '0'
        mdp_dict['ewald-rtol'] = '1e-5'

    # Temperature coupling
    if md:
        mdp_dict['tcoupl'] = 'V-rescale'
        mdp_dict['tc-grps'] = 'Protein Non-Protein'
        mdp_dict['tau-t'] = '0.1	  0.1'
        mdp_dict['ref-t'] = '300 	  300'

    # Pressure coupling
    if md:
        if nvt:
            mdp_dict['pcoupl'] = 'no'
        if npt or free:
            mdp_dict['pcoupl'] = 'Parrinello-Rahman'
            mdp_dict['pcoupltype'] = 'isotropic'
            mdp_dict['tau-p'] = '1.0'
            mdp_dict['ref-p'] = '1.0'
            mdp_dict['compressibility'] = '4.5e-5'
            mdp_dict['refcoord-scaling'] = 'com'

    # Dispersion correction
    if md:
        mdp_dict['DispCorr'] = 'EnerPres'

    # Velocity generation
    if md:
        if nvt:
            mdp_dict['gen-vel'] = 'yes'
            mdp_dict['gen-temp'] = '300'
            mdp_dict['gen-seed'] = '-1'
        if npt or free:
            mdp_dict['gen-vel'] = 'no'

    # Periodic boundary conditions
    mdp_dict['pbc'] = 'xyz'

    return mdp_dict


def write_mdp(output_mdp_path: str, mdp_dict: Mapping[str, str]):
    mdp_list = []
    for k, v in mdp_dict.items():
        config_parameter_key = str(k).strip().replace('_','-')
        if config_parameter_key != 'type':
            mdp_list.append(config_parameter_key + ' = ' + str(v))

    with open(output_mdp_path, 'w') as mdp_file:
        for line in mdp_list:
            mdp_file.write(line + '\n')

    return output_mdp_path
            
            
def create_mdp(output_mdp_path: str, input_mdp_path: str = None,
               preset_dict: Mapping[str, str] = None,
               mdp_properties_dict: Mapping[str, str] = None) -> str:
    """Creates an MDP file using the following hierarchy  mdp_properties_dict > input_mdp_path > preset_dict"""
    mdp_dict = {}

    if preset_dict:
        for k, v in preset_dict.items():
            mdp_dict[k] = v
    if input_mdp_path:
        input_mdp_dict = read_mdp(input_mdp_path)
        for k, v in input_mdp_dict.items():
            mdp_dict[k] = v
    if mdp_properties_dict:
        for k, v in mdp_properties_dict.items():
            mdp_dict[k] = v

    return write_mdp(output_mdp_path, mdp_dict)