from pycompss.api.task import task
from biobb_common.tools import file_utils as fu
from gromacs import grompp

@task(input_gro_path=FILE_IN, input_top_zip_path=FILE_IN, input_cpt_path=FILE_IN, output_tpr_path=FILE_OUT)
def grompp_pc(input_gro_path, input_top_zip_path, input_cpt_path=input_cpt_path,
             output_tpr_path, properties, **kwargs):
    try:
        grompp.Grompp(input_gro_path=input_gro_path, input_top_zip_path=input_top_zip_path, input_cpt_path=input_cpt_path, output_tpr_path=output_tpr_path properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_tpr_path)
