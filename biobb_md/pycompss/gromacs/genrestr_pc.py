from pycompss.api.task import task
from biobb_common.tools import file_utils as fu
from gromacs import genrestr

@task(input_structure_path=FILE_IN, input_ndx_path=FILE_IN, input_top_zip_path=FILE_IN, output_top_zip_path=FILE_OUT)
def genrestr_pc(input_structure_path, input_ndx_path, input_top_zip_path,
                output_top_zip_path, properties, **kwargs):
    try:
        genrestr.Genrestr(input_structure_path=input_structure_path, input_ndx_path=input_ndx_path,
                          input_top_zip_path=input_top_zip_path, output_top_zip_path=output_top_zip_path,
                          properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_top_zip_path)
