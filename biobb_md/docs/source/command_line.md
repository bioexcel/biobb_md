# BioBB MD Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Mdrun
Wrapper of the GROMACS mdrun module.
### Get help
Command:
```python
mdrun -h
```
    /bin/sh: mdrun: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_tpr_path** (*string*): Path to the portable binary run input file TPR. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/mdrun.tpr). Accepted formats: TPR
* **output_trr_path** (*string*): Path to the GROMACS uncompressed raw trajectory file TRR. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.trr). Accepted formats: TRR
* **output_gro_path** (*string*): Path to the output GROMACS structure GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.gro). Accepted formats: GRO
* **output_edr_path** (*string*): Path to the output GROMACS portable energy file EDR. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.edr). Accepted formats: EDR
* **output_log_path** (*string*): Path to the output GROMACS trajectory log file LOG. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.log). Accepted formats: LOG
* **input_cpt_path** (*string*): Path to the input GROMACS checkpoint file CPT. File type: input. [Sample file](None). Accepted formats: CPT
* **output_xtc_path** (*string*): Path to the GROMACS compressed trajectory file XTC. File type: output. [Sample file](None). Accepted formats: XTC
* **output_cpt_path** (*string*): Path to the output GROMACS checkpoint file CPT. File type: output. [Sample file](None). Accepted formats: CPT
* **output_dhdl_path** (*string*): Path to the output dhdl.xvg file only used when free energy calculation is turned on. File type: output. [Sample file](None). Accepted formats: XVG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mpi_bin** (*string*): (None) Path to the MPI runner. Usually "mpirun" or "srun"..
* **mpi_np** (*integer*): (0) Number of MPI processes. Usually an integer bigger than 1..
* **mpi_flags** (*string*): (None) Path to the MPI hostlist file..
* **checkpoint_time** (*integer*): (15) Checkpoint writing interval in minutes. Only enabled if an output_cpt_path is provided..
* **num_threads** (*integer*): (0) Let GROMACS guess. The number of threads that are going to be used..
* **num_threads_mpi** (*integer*): (0) Let GROMACS guess. The number of GROMACS MPI threads that are going to be used..
* **num_threads_omp** (*integer*): (0) Let GROMACS guess. The number of GROMACS OPENMP threads that are going to be used..
* **num_threads_omp_pme** (*integer*): (0) Let GROMACS guess. The number of GROMACS OPENMP_PME threads that are going to be used..
* **use_gpu** (*boolean*): (False) Use settings appropriate for GPU. Adds: -nb gpu -pme gpu.
* **gpu_id** (*string*): (None) List of unique GPU device IDs available to use..
* **gpu_tasks** (*string*): (None) List of GPU device IDs, mapping each PP task on each node to a device..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
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
  container_image: longr/gromacs-docker:latest
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
#### Command line
```python
mdrun --config config_mdrun.yml --input_tpr_path mdrun.tpr --output_trr_path ref_mdrun.trr --output_gro_path ref_mdrun.gro --output_edr_path ref_mdrun.edr --output_log_path ref_mdrun.log --input_cpt_path input.cpt --output_xtc_path output.xtc --output_cpt_path output.cpt --output_dhdl_path output.xvg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_mdrun.json)
```python
{
  "properties": {
    "num_threads": 0,
    "gmx_path": "gmx"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_mdrun_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "longr/gromacs-docker:latest",
    "container_volume_path": "/inout"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_mdrun_singularity.json)
```python
{
  "properties": {
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/inout"
  }
}
```
#### Command line
```python
mdrun --config config_mdrun.json --input_tpr_path mdrun.tpr --output_trr_path ref_mdrun.trr --output_gro_path ref_mdrun.gro --output_edr_path ref_mdrun.edr --output_log_path ref_mdrun.log --input_cpt_path input.cpt --output_xtc_path output.xtc --output_cpt_path output.cpt --output_dhdl_path output.xvg
```

## Make_ndx
Wrapper of the GROMACS make_ndx module.
### Get help
Command:
```python
make_ndx -h
```
    /bin/sh: make_ndx: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Path to the input GRO/PDB/TPR file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/make_ndx.tpr). Accepted formats: GRO, PDB, TPR
* **output_ndx_path** (*string*): Path to the output index NDX file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_make_ndx.ndx). Accepted formats: NDX
* **input_ndx_path** (*string*): Path to the input index NDX file. File type: input. [Sample file](None). Accepted formats: NDX
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **selection** (*string*): (a CA C N O) Heavy atoms. Atom selection string..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_make_ndx.yml)
```python
properties:
  selection: a CA C N O

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_make_ndx_docker.yml)
```python
properties:
  container_image: longr/gromacs-docker:latest
  container_path: docker
  container_volume_path: /tmp

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_make_ndx_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /tmp

```
#### Command line
```python
make_ndx --config config_make_ndx.yml --input_structure_path make_ndx.tpr --output_ndx_path ref_make_ndx.ndx --input_ndx_path input.ndx
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_make_ndx.json)
```python
{
  "properties": {
    "selection": "a CA C N O"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_make_ndx_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "longr/gromacs-docker:latest",
    "container_volume_path": "/tmp"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_make_ndx_singularity.json)
```python
{
  "properties": {
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
make_ndx --config config_make_ndx.json --input_structure_path make_ndx.tpr --output_ndx_path ref_make_ndx.ndx --input_ndx_path input.ndx
```

## Editconf
Wrapper class for the GROMACS editconf module.
### Get help
Command:
```python
editconf -h
```
    /bin/sh: editconf: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_gro_path** (*string*): Path to the input GRO file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/editconf.gro). Accepted formats: GRO, PDB
* **output_gro_path** (*string*): Path to the output GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_editconf.gro). Accepted formats: GRO, PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **distance_to_molecule** (*number*): (1.0) Distance of the box from the outermost atom in nm. ie 1.0nm = 10 Angstroms..
* **box_type** (*string*): (cubic) Geometrical shape of the solvent box. .
* **center_molecule** (*boolean*): (True) Center molecule in the box..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_editconf.yml)
```python
properties:
  box_type: cubic
  distance_to_molecule: 1.0

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_editconf_docker.yml)
```python
properties:
  container_image: longr/gromacs-docker:latest
  container_path: docker
  container_volume_path: /tmp

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_editconf_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /tmp

```
#### Command line
```python
editconf --config config_editconf.yml --input_gro_path editconf.gro --output_gro_path ref_editconf.gro
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_editconf.json)
```python
{
  "properties": {
    "distance_to_molecule": 1.0,
    "box_type": "cubic"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_editconf_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "longr/gromacs-docker:latest",
    "container_volume_path": "/tmp"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_editconf_singularity.json)
```python
{
  "properties": {
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/tmp"
  }
}
```
#### Command line
```python
editconf --config config_editconf.json --input_gro_path editconf.gro --output_gro_path ref_editconf.gro
```

## Ndx2resttop
Generate a restrained topology from an index NDX file.
### Get help
Command:
```python
ndx2resttop -h
```
    /bin/sh: ndx2resttop: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_ndx_path** (*string*): Path to the input NDX index file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs_extra/ndx2resttop.ndx). Accepted formats: NDX
* **input_top_zip_path** (*string*): Path the input TOP topology in zip format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs_extra/ndx2resttop.zip). Accepted formats: ZIP
* **output_top_zip_path** (*string*): Path the output TOP topology in zip format. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs_extra/ref_ndx2resttop.zip). Accepted formats: ZIP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **force_constants** (*string*): (500 500 500) Array of three floats defining the force constants..
* **ref_rest_chain_triplet_list** (*string*): (None) Triplet list composed by (reference group, restrain group, chain) list..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_ndx2resttop.yml)
```python
properties:
  ref_rest_chain_triplet_list: ( Chain_A, Chain_A_noMut, A ), ( Chain_B, Chain_B_noMut,
    B ), ( Chain_C, Chain_C_noMut, C ), ( Chain_D, Chain_D_noMut, D )

```
#### Command line
```python
ndx2resttop --config config_ndx2resttop.yml --input_ndx_path ndx2resttop.ndx --input_top_zip_path ndx2resttop.zip --output_top_zip_path ref_ndx2resttop.zip
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_ndx2resttop.json)
```python
{
  "properties": {
    "ref_rest_chain_triplet_list": "( Chain_A, Chain_A_noMut, A ), ( Chain_B, Chain_B_noMut, B ), ( Chain_C, Chain_C_noMut, C ), ( Chain_D, Chain_D_noMut, D )"
  }
}
```
#### Command line
```python
ndx2resttop --config config_ndx2resttop.json --input_ndx_path ndx2resttop.ndx --input_top_zip_path ndx2resttop.zip --output_top_zip_path ref_ndx2resttop.zip
```

## Grompp
Wrapper of the GROMACS grompp module.
### Get help
Command:
```python
grompp -h
```
    /bin/sh: grompp: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_gro_path** (*string*): Path to the input GROMACS structure GRO file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.gro). Accepted formats: GRO
* **input_top_zip_path** (*string*): Path to the input GROMACS topology TOP and ITP files in zip format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.zip). Accepted formats: ZIP
* **output_tpr_path** (*string*): Path to the output portable binary run file TPR. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_grompp.tpr). Accepted formats: TPR
* **input_cpt_path** (*string*): Path to the input GROMACS checkpoint file CPT. File type: input. [Sample file](None). Accepted formats: CPT
* **input_ndx_path** (*string*): Path to the input GROMACS index files NDX. File type: input. [Sample file](None). Accepted formats: NDX
* **input_mdp_path** (*string*): Path to the input GROMACS MDP file. File type: input. [Sample file](None). Accepted formats: MDP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mdp** (*object*): ({}) MDP options specification..
* **simulation_type** (*string*): (None) Default options for the mdp file. Each one creates a different mdp file. .
* **maxwarn** (*integer*): (0) Maximum number of allowed warnings. If simulation_type is index default is 10..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp.yml)
```python
properties:
  maxwarn: 1
  mdp:
    ld-seed: '1'

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_docker.yml)
```python
properties:
  container_image: gromacs/gromacs:latest
  container_path: docker
  container_volume_path: /inout
  container_working_dir: /inout
  maxwarn: 1
  mdp:
    ld-seed: '1'

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /inout
  container_working_dir: /inout
  maxwarn: 1
  mdp:
    ld-seed: '1'

```
#### Command line
```python
grompp --config config_grompp.yml --input_gro_path grompp.gro --input_top_zip_path grompp.zip --output_tpr_path ref_grompp.tpr --input_cpt_path input.cpt --input_ndx_path input.ndx --input_mdp_path input.mdp
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp.json)
```python
{
  "properties": {
    "maxwarn": 1,
    "mdp": {
      "ld-seed": "1"
    }
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_docker.json)
```python
{
  "properties": {
    "maxwarn": 1,
    "mdp": {
      "ld-seed": "1"
    },
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/inout",
    "container_working_dir": "/inout"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_singularity.json)
```python
{
  "properties": {
    "maxwarn": 1,
    "mdp": {
      "ld-seed": "1"
    },
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/inout",
    "container_working_dir": "/inout"
  }
}
```
#### Command line
```python
grompp --config config_grompp.json --input_gro_path grompp.gro --input_top_zip_path grompp.zip --output_tpr_path ref_grompp.tpr --input_cpt_path input.cpt --input_ndx_path input.ndx --input_mdp_path input.mdp
```

## Gmxselect
Wrapper of the GROMACS select module.
### Get help
Command:
```python
gmxselect -h
```
    /bin/sh: gmxselect: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Path to the input GRO/PDB/TPR file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/make_ndx.tpr). Accepted formats: PDB, GRO, TPR
* **output_ndx_path** (*string*): Path to the output index NDX file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_select.ndx). Accepted formats: NDX
* **input_ndx_path** (*string*): Path to the input index NDX file. File type: input. [Sample file](None). Accepted formats: NDX
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **selection** (*string*): (a CA C N O) Heavy atoms. Atom selection string..
* **append** (*boolean*): (False) Append the content of the input_ndx_path to the output_ndx_path..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_gmxselect.yml)
```python
properties:
  selection: '"Mynewgroup" group "Protein-H" and not same residue as within 0.4 of
    resname ARG'

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_gmxselect_docker.yml)
```python
properties:
  container_image: gromacs/gromacs:latest
  container_path: docker
  container_volume_path: /inout
  selection: \"Mynewgroup\" group \"Protein-H\" and not same residue as within 0.4
    of resname ARG

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_gmxselect_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /inout
  selection: '"Mynewgroup" group "Protein-H" and not same residue as within 0.4 of
    resname ARG'

```
#### Command line
```python
gmxselect --config config_gmxselect.yml --input_structure_path make_ndx.tpr --output_ndx_path ref_select.ndx --input_ndx_path input.ndx
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_gmxselect.json)
```python
{
  "properties": {
    "selection": "\"Mynewgroup\" group \"Protein-H\" and not same residue as within 0.4 of resname ARG"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_gmxselect_docker.json)
```python
{
  "properties": {
    "selection": "\\\"Mynewgroup\\\" group \\\"Protein-H\\\" and not same residue as within 0.4 of resname ARG",
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/inout"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_gmxselect_singularity.json)
```python
{
  "properties": {
    "selection": "\"Mynewgroup\" group \"Protein-H\" and not same residue as within 0.4 of resname ARG",
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/inout"
  }
}
```
#### Command line
```python
gmxselect --config config_gmxselect.json --input_structure_path make_ndx.tpr --output_ndx_path ref_select.ndx --input_ndx_path input.ndx
```

## Pdb2gmx
Wrapper class for the GROMACS pdb2gmx module.
### Get help
Command:
```python
pdb2gmx -h
```
    /bin/sh: pdb2gmx: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Path to the input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/egfr.pdb). Accepted formats: PDB
* **output_gro_path** (*string*): Path to the output GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_pdb2gmx.gro). Accepted formats: GRO
* **output_top_zip_path** (*string*): Path the output TOP topology in zip format. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_pdb2gmx.zip). Accepted formats: ZIP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **water_type** (*string*): (spce) Water molecule type. .
* **force_field** (*string*): (amber99sb-ildn) Force field to be used during the conversion.  .
* **ignh** (*boolean*): (False) Should pdb2gmx ignore the hidrogens in the original structure..
* **his** (*string*): (None) Histidine protonation array..
* **merge** (*boolean*): (False) Merge all chains into a single molecule..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_pdb2gmx.yml)
```python
properties:
  his: 0 0 1 1 0 0 0

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_pdb2gmx_docker.yml)
```python
properties:
  container_image: longr/gromacs-docker:latest
  container_path: docker
  container_volume_path: /inout
  his: 0 0 1 1 0 0 0

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_pdb2gmx_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /inout
  his: 0 0 1 1 0 0 0

```
#### Command line
```python
pdb2gmx --config config_pdb2gmx.yml --input_pdb_path egfr.pdb --output_gro_path ref_pdb2gmx.gro --output_top_zip_path ref_pdb2gmx.zip
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_pdb2gmx.json)
```python
{
  "properties": {
    "his": "0 0 1 1 0 0 0"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_pdb2gmx_docker.json)
```python
{
  "properties": {
    "his": "0 0 1 1 0 0 0",
    "container_path": "docker",
    "container_image": "longr/gromacs-docker:latest",
    "container_volume_path": "/inout"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_pdb2gmx_singularity.json)
```python
{
  "properties": {
    "his": "0 0 1 1 0 0 0",
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/inout"
  }
}
```
#### Command line
```python
pdb2gmx --config config_pdb2gmx.json --input_pdb_path egfr.pdb --output_gro_path ref_pdb2gmx.gro --output_top_zip_path ref_pdb2gmx.zip
```

## Append_ligand
This class takes a ligand ITP file and inserts it in a topology.
### Get help
Command:
```python
append_ligand -h
```
    /bin/sh: append_ligand: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_top_zip_path** (*string*): Path the input topology TOP and ITP files zipball. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs_extra/ndx2resttop.zip). Accepted formats: ZIP
* **input_itp_path** (*string*): Path to the ligand ITP file to be inserted in the topology. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs_extra/pep_ligand.itp). Accepted formats: ITP
* **output_top_zip_path** (*string*): Path/Name the output topology TOP and ITP files zipball. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs_extra/ref_appendligand.zip). Accepted formats: ZIP
* **input_posres_itp_path** (*string*): Path to the position restriction ITP file. File type: input. [Sample file](None). Accepted formats: ITP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **posres_name** (*string*): (POSRES_LIGAND) String to be included in the ifdef clause..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_append_ligand.yml)
```python
properties:
  posres_name: POSRES_LIGAND

```
#### Command line
```python
append_ligand --config config_append_ligand.yml --input_top_zip_path ndx2resttop.zip --input_itp_path pep_ligand.itp --output_top_zip_path ref_appendligand.zip --input_posres_itp_path input.itp
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_append_ligand.json)
```python
{
  "properties": {
    "posres_name": "POSRES_LIGAND"
  }
}
```
#### Command line
```python
append_ligand --config config_append_ligand.json --input_top_zip_path ndx2resttop.zip --input_itp_path pep_ligand.itp --output_top_zip_path ref_appendligand.zip --input_posres_itp_path input.itp
```

## Solvate
Wrapper of the GROMACS solvate module.
### Get help
Command:
```python
solvate -h
```
    /bin/sh: solvate: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_solute_gro_path** (*string*): Path to the input GRO file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/solvate.gro). Accepted formats: GRO
* **output_gro_path** (*string*): Path to the output GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_solvate.gro). Accepted formats: GRO
* **input_top_zip_path** (*string*): Path the input TOP topology in zip format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/solvate.zip). Accepted formats: ZIP
* **output_top_zip_path** (*string*): Path the output topology in zip format. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_solvate.zip). Accepted formats: ZIP
* **input_solvent_gro_path** (*string*): (spc216.gro) Path to the GRO file containing the structure of the solvent. File type: input. [Sample file](None). Accepted formats: GRO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **shell** (*number*): (0.0) Thickness in nanometers of optional water layer around solute..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_solvate.yml)
```python
properties:
  gmx_path: gmx
  restart: 'False'

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_solvate_docker.yml)
```python
properties:
  container_image: longr/gromacs-docker:latest
  container_path: docker
  container_volume_path: /inout

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_solvate_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /inout

```
#### Command line
```python
solvate --config config_solvate.yml --input_solute_gro_path solvate.gro --output_gro_path ref_solvate.gro --input_top_zip_path solvate.zip --output_top_zip_path ref_solvate.zip --input_solvent_gro_path input.gro
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_solvate.json)
```python
{
  "properties": {
    "gmx_path": "gmx",
    "restart": "False"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_solvate_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "longr/gromacs-docker:latest",
    "container_volume_path": "/inout"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_solvate_singularity.json)
```python
{
  "properties": {
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/inout"
  }
}
```
#### Command line
```python
solvate --config config_solvate.json --input_solute_gro_path solvate.gro --output_gro_path ref_solvate.gro --input_top_zip_path solvate.zip --output_top_zip_path ref_solvate.zip --input_solvent_gro_path input.gro
```

## Genion
Wrapper class for the GROMACS genion module.
### Get help
Command:
```python
genion -h
```
    /bin/sh: genion: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_tpr_path** (*string*): Path to the input portable run input TPR file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/genion.tpr). Accepted formats: TPR
* **output_gro_path** (*string*): Path to the input structure GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_genion.gro). Accepted formats: GRO
* **input_top_zip_path** (*string*): Path the input TOP topology in zip format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/genion.zip). Accepted formats: ZIP
* **output_top_zip_path** (*string*): Path the output topology TOP and ITP files zipball. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_genion.zip). Accepted formats: ZIP
* **input_ndx_path** (*string*): Path to the input index NDX file. File type: input. [Sample file](None). Accepted formats: NDX
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **replaced_group** (*string*): (SOL) Group of molecules that will be replaced by the solvent..
* **neutral** (*boolean*): (False) Neutralize the charge of the system..
* **concentration** (*number*): (0.05) Concentration of the ions in (mol/liter)..
* **seed** (*integer*): (1993) Seed for random number generator..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genion.yml)
```python
properties:
  concentration: 0.05
  replaced_group: SOL

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genion_docker.yml)
```python
properties:
  container_image: longr/gromacs-docker:latest
  container_path: docker
  container_volume_path: /data
  container_working_dir: /data

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genion_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /data
  container_working_dir: /data

```
#### Command line
```python
genion --config config_genion.yml --input_tpr_path genion.tpr --output_gro_path ref_genion.gro --input_top_zip_path genion.zip --output_top_zip_path ref_genion.zip --input_ndx_path input.ndx
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genion.json)
```python
{
  "properties": {
    "concentration": 0.05,
    "replaced_group": "SOL"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genion_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "longr/gromacs-docker:latest",
    "container_volume_path": "/data",
    "container_working_dir": "/data"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genion_singularity.json)
```python
{
  "properties": {
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/data",
    "container_working_dir": "/data"
  }
}
```
#### Command line
```python
genion --config config_genion.json --input_tpr_path genion.tpr --output_gro_path ref_genion.gro --input_top_zip_path genion.zip --output_top_zip_path ref_genion.zip --input_ndx_path input.ndx
```

## Grompp_mdrun
Wrapper of the GROMACS grompp module and the GROMACS mdrun module.
### Get help
Command:
```python
grompp_mdrun -h
```
    /bin/sh: grompp_mdrun: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_gro_path** (*string*): Path to the input GROMACS structure GRO file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.gro). Accepted formats: GRO
* **input_top_zip_path** (*string*): Path to the input GROMACS topology TOP and ITP files in zip format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/grompp.zip). Accepted formats: ZIP
* **output_trr_path** (*string*): Path to the GROMACS uncompressed raw trajectory file TRR. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.trr). Accepted formats: TRR
* **output_gro_path** (*string*): Path to the output GROMACS structure GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.gro). Accepted formats: GRO
* **output_edr_path** (*string*): Path to the output GROMACS portable energy file EDR. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_mdrun.edr). Accepted formats: EDR
* **output_log_path** (*string*): Path to the output GROMACS trajectory log file LOG. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_gmx_mdrun.log). Accepted formats: LOG
* **input_cpt_path** (*string*): Path to the input GROMACS checkpoint file CPT. File type: input. [Sample file](None). Accepted formats: CPT
* **input_ndx_path** (*string*): Path to the input GROMACS index files NDX. File type: input. [Sample file](None). Accepted formats: NDX
* **input_mdp_path** (*string*): Path to the input GROMACS MDP file. File type: input. [Sample file](None). Accepted formats: MDP
* **output_xtc_path** (*string*): Path to the GROMACS compressed trajectory file XTC. File type: output. [Sample file](None). Accepted formats: XTC
* **output_cpt_path** (*string*): Path to the output GROMACS checkpoint file CPT. File type: output. [Sample file](None). Accepted formats: CPT
* **output_dhdl_path** (*string*): Path to the output dhdl.xvg file only used when free energy calculation is turned on. File type: output. [Sample file](None). Accepted formats: XVG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **mdp** (*object*): ({}) MDP options specification..
* **simulation_type** (*string*): (minimization) Default options for the mdp file. Each creates a different mdp file. .
* **maxwarn** (*integer*): (10) Maximum number of allowed warnings..
* **mpi_bin** (*string*): (None) Path to the MPI runner. Usually "mpirun" or "srun"..
* **mpi_np** (*string*): (None) Number of MPI processes. Usually an integer bigger than 1..
* **mpi_hostlist** (*string*): (None) Path to the MPI hostlist file..
* **checkpoint_time** (*integer*): (15) Checkpoint writing interval in minutes. Only enabled if an output_cpt_path is provided..
* **num_threads** (*integer*): (0) Let GROMACS guess. The number of threads that are going to be used..
* **num_threads_mpi** (*integer*): (0) Let GROMACS guess. The number of GROMACS MPI threads that are going to be used..
* **num_threads_omp** (*integer*): (0) Let GROMACS guess. The number of GROMACS OPENMP threads that are going to be used..
* **num_threads_omp_pme** (*integer*): (0) Let GROMACS guess. The number of GROMACS OPENMP_PME threads that are going to be used..
* **use_gpu** (*boolean*): (False) Use settings appropriate for GPU. Adds: -nb gpu -pme gpu.
* **gpu_id** (*string*): (None) List of unique GPU device IDs available to use..
* **gpu_tasks** (*string*): (None) List of GPU device IDs, mapping each PP task on each node to a device..
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_mdrun.yml)
```python
properties:
  gmx_path: gmx
  maxwarn: 1
  mdp:
    dt: 0.0001
    ld-seed: '1'
  num_threads: 0
  simulation_type: free

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_mdrun_docker.yml)
```python
properties:
  container_image: longr/gromacs-docker:latest
  container_path: docker
  container_volume_path: /inout
  gmx_path: gmx
  maxwarn: 1
  mdp:
    dt: 0.0001
    ld-seed: '1'
  num_threads: 0
  simulation_type: free

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_mdrun_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /inout
  gmx_path: gmx
  mdp:
    dt: 0.0001
    ld-seed: '1'
  num_threads: 0
  simulation_type: free

```
#### Command line
```python
grompp_mdrun --config config_grompp_mdrun.yml --input_gro_path grompp.gro --input_top_zip_path grompp.zip --output_trr_path ref_mdrun.trr --output_gro_path ref_mdrun.gro --output_edr_path ref_mdrun.edr --output_log_path ref_gmx_mdrun.log --input_cpt_path input.cpt --input_ndx_path input.ndx --input_mdp_path input.mdp --output_xtc_path output.xtc --output_cpt_path output.cpt --output_dhdl_path output.xvg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_mdrun.json)
```python
{
  "properties": {
    "simulation_type": "free",
    "maxwarn": 1,
    "mdp": {
      "ld-seed": "1",
      "dt": 0.0001
    },
    "num_threads": 0,
    "gmx_path": "gmx"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_mdrun_docker.json)
```python
{
  "properties": {
    "simulation_type": "free",
    "maxwarn": 1,
    "mdp": {
      "ld-seed": "1",
      "dt": 0.0001
    },
    "num_threads": 0,
    "gmx_path": "gmx",
    "container_path": "docker",
    "container_image": "longr/gromacs-docker:latest",
    "container_volume_path": "/inout"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_grompp_mdrun_singularity.json)
```python
{
  "properties": {
    "simulation_type": "free",
    "mdp": {
      "ld-seed": "1",
      "dt": 0.0001
    },
    "num_threads": 0,
    "gmx_path": "gmx",
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/inout"
  }
}
```
#### Command line
```python
grompp_mdrun --config config_grompp_mdrun.json --input_gro_path grompp.gro --input_top_zip_path grompp.zip --output_trr_path ref_mdrun.trr --output_gro_path ref_mdrun.gro --output_edr_path ref_mdrun.edr --output_log_path ref_gmx_mdrun.log --input_cpt_path input.cpt --input_ndx_path input.ndx --input_mdp_path input.mdp --output_xtc_path output.xtc --output_cpt_path output.cpt --output_dhdl_path output.xvg
```

## Genrestr
Wrapper of the GROMACS genrestr module.
### Get help
Command:
```python
genrestr -h
```
    /bin/sh: genrestr: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Path to the input structure PDB, GRO or TPR format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/genrestr.gro). Accepted formats: PDB, GRO, TPR
* **output_itp_path** (*string*): Path the output ITP topology file with restrains. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_genrestr.itp). Accepted formats: ITP
* **input_ndx_path** (*string*): Path to the input GROMACS index file, NDX format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/genrestr.ndx). Accepted formats: NDX
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **restrained_group** (*string*): (system) Index group that will be restrained..
* **force_constants** (*string*): (500 500 500) Array of three floats defining the force constants.
* **gmx_lib** (*string*): (None) Path set GROMACS GMXLIB environment variable..
* **gmx_path** (*string*): (gmx) Path to the GROMACS executable binary..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **container_path** (*string*): (None) Path to the binary executable of your container..
* **container_image** (*string*): (gromacs/gromacs:latest) Container Image identifier..
* **container_volume_path** (*string*): (/data) Path to an internal directory in the container..
* **container_working_dir** (*string*): (None) Path to the internal CWD in the container..
* **container_user_id** (*string*): (None) User number id to be mapped inside the container..
* **container_shell_path** (*string*): (/bin/bash) Path to the binary executable of the container shell..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genrestr.yml)
```python
properties:
  force_constants: 500 500 500
  restrained_group: system

```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genrestr_docker.yml)
```python
properties:
  container_image: longr/gromacs-docker:latest
  container_path: docker
  container_volume_path: /data
  container_working_dir: /data

```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genrestr_singularity.yml)
```python
properties:
  container_image: gromacs.simg
  container_path: singularity
  container_volume_path: /data
  container_working_dir: /data

```
#### Command line
```python
genrestr --config config_genrestr.yml --input_structure_path genrestr.gro --output_itp_path ref_genrestr.itp --input_ndx_path genrestr.ndx
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genrestr.json)
```python
{
  "properties": {
    "restrained_group": "system",
    "force_constants": "500 500 500"
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genrestr_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "longr/gromacs-docker:latest",
    "container_volume_path": "/data",
    "container_working_dir": "/data"
  }
}
```
#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_genrestr_singularity.json)
```python
{
  "properties": {
    "container_path": "singularity",
    "container_image": "gromacs.simg",
    "container_volume_path": "/data",
    "container_working_dir": "/data"
  }
}
```
#### Command line
```python
genrestr --config config_genrestr.json --input_structure_path genrestr.gro --output_itp_path ref_genrestr.itp --input_ndx_path genrestr.ndx
```
