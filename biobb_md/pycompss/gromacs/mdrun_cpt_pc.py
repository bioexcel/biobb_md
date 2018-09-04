from pycompss.api.task import task
from biobb_common.tools import file_utils as fu
from gromacs import mdrun

@task(input_tpr_path=FILE_IN, output_trr_path=FILE_OUT, output_gro_path=FILE_OUT, output_edr_path=FILE_OUT, output_log_path=FILE_OUT, output_xtc_path=FILE_OUT)
def mdrun_pc(input_tpr_path, output_trr_path, output_gro_path, output_edr_path,
             output_log_path, output_xtc_path, output_cpt_path, properties, **kwargs):
    try:
        mdrun.Mdrun(input_tpr_path=input_tpr_path, output_trr_path=output_trr_path, output_gro_path=output_gro_path, output_edr_path=output_edr_path, output_log_path=output_log_path, output_xtc_path=output_xtc_path, output_cpt_path=output_cpt_path, properties=properties, **kwargs).launch()
    except Exception:
        traceback.print_exc()
        fu.write_failed_output(output_trr_path)
        fu.write_failed_output(output_gro_path)
        fu.write_failed_output(output_edr_path)
        fu.write_failed_output(output_log_path)
        fu.write_failed_output(output_xtc_path)
        fu.write_failed_output(output_cpt_path)
