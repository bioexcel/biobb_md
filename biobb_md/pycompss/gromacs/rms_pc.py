from pycompss.api.task import task
from biobb_common.tools import file_utils as fu
from gromacs import rms

@task(input_structure_path=FILE_IN, input_traj_path=FILE_IN, output_xvg_path=FILE_OUT)
def editconf_pc(input_structure_path, input_traj_path, output_xvg_path, properties, **kwargs):
    try:
        rms.Rms(input_structure_path=input_structure_path, input_traj_path=input_traj_path, output_xvg_path=output_xvg_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_xvg_path)
