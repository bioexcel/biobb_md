from pycompss.api.task import task
from biobb_common.tools import file_utils as fu
from gromacs_extra import ndx2resttop

@task(input_ndx_path=FILE_IN, input_top_zip_path=FILE_IN, output_top_zip_path=FILE_OUT)
def ndx2resttop_pc(input_ndx_path, input_top_zip_path, output_top_zip_path, properties, **kwargs):
    try:
        ndx2resttop.Ndx2resttop(input_ndx_path=input_ndx_path, input_top_zip_path=input_top_zip_path, output_top_zip_path=output_top_zip_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_top_zip_path)
