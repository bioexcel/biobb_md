# BioBB MD Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Mdrun
Wrapper of the [GROMACS mdrun](http://manual.gromacs.org/current/onlinehelp/gmx-mdrun.html) module.

### Get help
Command:
```python
mdrun -h
```
    usage: mdrun [-h] [-c CONFIG] --input_tpr_path INPUT_TPR_PATH --output_trr_path OUTPUT_TRR_PATH --output_gro_path OUTPUT_GRO_PATH --output_edr_path OUTPUT_EDR_PATH --output_log_path OUTPUT_LOG_PATH [--output_xtc_path OUTPUT_XTC_PATH] [--output_cpt_path OUTPUT_CPT_PATH] [--output_dhdl_path OUTPUT_DHDL_PATH]
    
    Wrapper for the GROMACS mdrun module.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
      --output_xtc_path OUTPUT_XTC_PATH
      --output_cpt_path OUTPUT_CPT_PATH
      --output_dhdl_path OUTPUT_DHDL_PATH
    
    required arguments:
      --input_tpr_path INPUT_TPR_PATH
      --output_trr_path OUTPUT_TRR_PATH
      --output_gro_path OUTPUT_GRO_PATH
      --output_edr_path OUTPUT_EDR_PATH
      --output_log_path OUTPUT_LOG_PATH

### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_tpr_path** (*string*): Path to the portable binary run input file TPR. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/mdrun.tpr). Accepted formats: TPR
* **output_trr_path** (*string*): Path to the GROMACS uncompressed raw trajectory file TRR. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.trr). Accepted formats: TRR
* **output_gro_path** (*string*): Path to the output GROMACS structure GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.gro). Accepted formats: GRO
* **output_edr_path** (*string*): Path to the output GROMACS portable energy file EDR. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.edr). Accepted formats: EDR
* **output_log_path** (*string*): Path to the output GROMACS trajectory log file LOG. File type: output. [Sample file](None). Accepted formats: LOG
* **output_xtc_path** (*string*): Path to the GROMACS compressed trajectory file XTC. File type: output. [Sample file](None). Accepted formats: XTC
* **output_cpt_path** (*string*): Path to the output GROMACS checkpoint file CPT. File type: output. [Sample file](None). Accepted formats: CPT
* **output_dhdl_path** (*string*): Path to the output dhdl. File type: output. [Sample file](None). Accepted formats: XVG

### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **num_threads** (*number*): (0) Let GROMACS guess. The number of threads that are going to be used..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **mpi_bin** (*string*): (None) Path to the MPI runner. Usually "mpirun" or "srun"..
* **mpi_np** (*string*): (None) Number of MPI processes. Usually an integer bigger than 1..
* **mpi_hostlist** (*string*): (None) Path to the MPI hostlist file..
* **remove_tmp** (*boolean*): (True) [WF property] Remove temporal files..
* **restart** (*boolean*): (False) [WF property] Do not execute if output files exist..
* **container_path** (*string*): (None)  Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..

### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_mdrun.yml)
```python
properties:
  gmx_path: gmx
  num_threads: 0

```

#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_mdrun_docker.yml)
```python
properties:
  container_image: gromacs/gromacs:latest
  container_path: docker
  container_volume_path: /inout

```

#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_mdrun_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /inout

```
