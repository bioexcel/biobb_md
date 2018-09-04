from pycompss.api.task import task
from biobb_common.tools import file_utils as fu
from gromacs import editconf

@task(input_gro_path=FILE_IN, output_gro_path=FILE_OUT)
def editconf_pc(input_gro_path, output_gro_path, properties, **kwargs):
    try:
        editconf.Editconf(input_gro_path=input_gro_path, output_gro_path=output_gro_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_gro_path)
