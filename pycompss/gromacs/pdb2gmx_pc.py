from pycompss.api.task import task
from biobb_common.tools import file_utils as fu
from gromacs import pdb2gmx

@task(input_pdb_path=FILE_IN, output_gro_path=FILE_OUT, output_top_zip_path=FILE_OUT)
def pdb2gmx_pc(input_pdb_path, output_gro_path, output_top_zip_path, properties, **kwargs):
    try:
        pdb2gmx.Pdb2gmx(input_pdb_path=input_pdb_path, output_gro_path=output_gro_path, output_top_zip_path=output_top_zip_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_gro_path)
        fu.write_failed_output(output_top_zip_path)
