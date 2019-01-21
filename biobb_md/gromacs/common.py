""" Common functions for package biobb_md.gromacs """
import os
import re
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper

def get_gromacs_version(gmx="gmx"):
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
    cmd_wrapper.CmdWrapper(cmd, out_log, err_log).launch()
    pattern = re.compile(r"GROMACS version:\s+(.+)")
    with open(os.path.join(unique_dir, 'log.out'), 'r') as log_file:
        for line in log_file:
            version_str = pattern.match(line.strip())
            if version_str:
                break
    version = version_str.group(1).strip().replace(".", "")
    if version.startswith("2"):
        while len(version) < 5:
            version += '0'
    else:
        while len(version) < 3:
            version += '0'

    return int(version)


class GromacsVersionError(Exception):
    """ Exception Raised when the installed version of GROMACS is not
        compatible with the current function.
    """
    pass
