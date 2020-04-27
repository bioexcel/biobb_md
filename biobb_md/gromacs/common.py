""" Common functions for package biobb_md.gromacs """
import re
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper


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
