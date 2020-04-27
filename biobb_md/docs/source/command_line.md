# BioBB Analysis Command Line Help

Generic usage:


```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```

-----------------

## Editconf

Wrapper of the GROMACS gmx editconf module.

### Get help

Command:


```python
editconf -h
```

    usage: editconf [-h] [-c CONFIG] --input_gro_path INPUT_GRO_PATH --output_gro_path OUTPUT_GRO_PATH
    
    Wrapper of the GROMACS gmx editconf module.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      --input_gro_path INPUT_GRO_PATH
      --output_gro_path OUTPUT_GRO_PATH


### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_gro_path** (*str*): Path to the input GRO file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/editconf.gro). Accepted formats: gro.
* **output_gro_path** (*str*): Path to the output GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_editconf.gro). Accepted formats: gro.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **distance_to_molecule** (*float*) - (1.0) Distance of the box from the outermost atom in nm. ie 1.0nm = 10 Angstroms.
* **box_type** (*str*) - ("cubic") Geometrical shape of the solvent box. [Available box types](http://manual.gromacs.org/current/onlinehelp/gmx-editconf.html) -bt option.
* **center_molecule** (*bool*) - (True) Center molecule in the box.
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*str*) - (None)  Path to the binary executable of your container.
* **container_image** (*str*) - ("gromacs/gromacs:latest") Container Image identifier.
* **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
* **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
* **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
* **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

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
  container_image: gromacs/gromacs:latest
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
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### [Singularity config file](https://github.com/bioexcel/biobb_md/blob/master/biobb_md/test/data/config/config_editconf_singularity.json)


```python
{
    "properties": {
        "distance_to_molecule": 1.0,
        "box_type": "cubic"
        "container_path": "singularity"
        "container_image": "gromacs.simg"
        "container_volume_path": "/tmp"
    }
}
```

#### Command line


```python
editconf --config config_editconf.json --input_gro_path editconf.gro --output_gro_path ref_editconf.gro
```

## Genion

Wrapper for the GROMACS genion module.

### Get help

Command:


```python
genion -h
```

    usage: genion [-h] [-c CONFIG] --input_tpr_path INPUT_TPR_PATH --output_gro_path OUTPUT_GRO_PATH --input_top_zip_path INPUT_TOP_ZIP_PATH --output_top_zip_path OUTPUT_TOP_ZIP_PATH
    
    Wrapper for the GROMACS genion module.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      --input_tpr_path INPUT_TPR_PATH
      --output_gro_path OUTPUT_GRO_PATH
      --input_top_zip_path INPUT_TOP_ZIP_PATH
      --output_top_zip_path OUTPUT_TOP_ZIP_PATH


### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_tpr_path** (*str*): Path to the input portable run input TPR file. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/genion.tpr). Accepted formats: tpr.
* **output_gro_path** (*str*): Path to the input structure GRO file. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_genion.gro). Accepted formats: gro.
* **input_top_zip_path** (*str*): Path the input TOP topology in zip format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/genion.zip). Accepted formats: zip.
* **output_top_zip_path** (*str*): Path the output topology TOP and ITP files zipball. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_genion.zip). Accepted formats: zip.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **output_top_path** (*str*) - ("gio.top") Path the output topology TOP file.
* **replaced_group** (*str*) - ("SOL") Group of molecules that will be replaced by the solvent.
* **neutral** (*bool*) - (False) Neutralize the charge of the system.
* **concentration** (*float*) - (0.05) Concentration of the ions in (mol/liter).
* **seed** (*int*) - (1993) Seed for random number generator.
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*str*) - (None)  Path to the binary executable of your container.
* **container_image** (*str*) - ("gromacs/gromacs:latest") Container Image identifier.
* **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
* **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
* **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
* **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

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
  container_image: gromacs/gromacs:latest
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
genion --config data/conf/genion.yml --input_tpr_path data/input/genion.tpr --output_gro_path data/output/genion.gro --input_top_zip_path data/input/input_top.zip --output_top_zip_path data/output/output_top.zip
```

### JSON

#### Common file config


```python
{
    "properties": {
        "concentration": 0.05,
        "replaced_group": "SOL"
    }
}
```

#### Docker config file


```python
{
    "properties": {
        "distance_to_molecule": 1.0,
        "box_type": "cubic"
        "container_path": "docker"
        "container_image": "gromacs/gromacs:latest"
        "container_volume_path": "/tmp"
    }
}
```

#### Singularity config file


```python
{
    "properties": {
        "distance_to_molecule": 1.0,
        "box_type": "cubic"
        "container_path": "singularity"
        "container_image": "gromacs.simg"
        "container_volume_path": "/tmp"
    }
}
```

#### Command line


```python
genion --config data/conf/genion.json --input_tpr_path data/input/genion.tpr --output_gro_path data/output/genion.gro --input_top_zip_path data/input/input_top.zip --output_top_zip_path data/output/output_top.zip
```

## Genrestr convert

Converts between cpptraj compatible trajectory file formats and/or extracts a selection of atoms or frames.

### Get help

Command:


```python
genrestr -h
```

    usage: genrestr [-h] [-c CONFIG] --input_structure_path INPUT_STRUCTURE_PATH --input_ndx_path INPUT_NDX_PATH --output_itp_path OUTPUT_ITP_PATH
    
    Wrapper for the GROMACS genion module.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      --input_structure_path INPUT_STRUCTURE_PATH
      --input_ndx_path INPUT_NDX_PATH
      --output_itp_path OUTPUT_ITP_PATH


### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Path to the input structure PDB, GRO or TPR format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/genrestr.gro). Accepted formats: pdb, gro, tpr.
* **input_ndx_path** (*str*): Path to the input GROMACS index file, NDX format. File type: input. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/data/gromacs/genrestr.ndx). Accepted formats: ndx.
* **output_itp_path** (*str*): Path the output ITP topology file with restrains. File type: output. [Sample file](https://github.com/bioexcel/biobb_md/raw/master/biobb_md/test/reference/gromacs/ref_genrestr.itp). Accepted formats: itp.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **restrained_group** (*str*) - ("system") Index group that will be restrained.
* **force_constants** (*str*) - ("500 500 500") Array of three floats defining the force constants
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*str*) - (None)  Path to the binary executable of your container.
* **container_image** (*str*) - ("gromacs/gromacs:latest") Container Image identifier.
* **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
* **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
* **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
* **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

### YAML

#### Common file config


```python
properties:
  restrained_group: "system"
  force_constants: "500 500 500"
```

#### Docker file config


```python
properties:
  "container_path": "docker"
  "container_image": "gromacs/gromacs:latest"
  "container_volume_path": "/data"
  "container_working_dir": "/data"
```

#### Singularity file config


```python
properties:
  "container_path": "singularity"
  "container_image": "gromacs.simg"
  "container_volume_path": "/data"
  "container_working_dir": "/data"
```

#### Command line


```python
genrestr --config data/conf/convert.yml --input_structure_path data/input/cpptraj.parm.top --input_ndx_path data/input/cpptraj.traj.dcd --output_itp_path data/output/output.convert.netcdf
```

### JSON file

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_convert --config data/conf/convert.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.convert.netcdf
```

## Cpptraj dry

Dehydrates a given cpptraj compatible trajectory stripping out solvent molecules and ions.

### Get help

Command:


```python
cpptraj_dry -h
```


```python
usage: cpptraj_dry [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Dehydrates a given cpptraj compatible trajectory stripping out solvent molecules and ions.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output processed trajectory.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **output_cpptraj_path** (*str*): Path to the output processed trajectory.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **start** (*int*) - (1) Starting frame for slicing
    * **end** (*int*) - (-1) Ending frame for slicing
    * **step** (*int*) - (1) Step for slicing
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
* **out_parameters** (*dict*) - (None) Parameters for output trajectory.
    * **format** (*str*) - ("netcdf") Output trajectory format. Values: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
```

#### Docker file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_dry --config data/conf/dry.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.dry.netcdf
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  },
  "container_path": "docker",
  "container_image": "afandiadib/ambertools:serial",
  "container_volume_path": "/tmp"
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_dry --config data/conf/dry.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.dry.netcdf
```

## Cpptraj image

Corrects periodicity (image) from a given cpptraj trajectory file.

### Get help

Command:


```python
cpptraj_image -h
```


```python
usage: cpptraj_image [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Corrects periodicity (image) from a given cpptraj trajectory file.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output processed trajectory.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **output_cpptraj_path** (*str*): Path to the output processed trajectory.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **start** (*int*) - (1) Starting frame for slicing
    * **end** (*int*) - (-1) Ending frame for slicing
    * **step** (*int*) - (1) Step for slicing
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
* **out_parameters** (*dict*) - (None) Parameters for output trajectory.
    * **format** (*str*) - ("netcdf") Output trajectory format. Values: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
```

#### Docker file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Common file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_image --config data/conf/image.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.image.netcdf
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  },
  "container_path": "docker",
  "container_image": "afandiadib/ambertools:serial",
  "container_volume_path": "/tmp"
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  },
  "container_path": "singularity",
  "container_image": "ambertools.sif",
  "container_volume_path": "/tmp"
}
```

#### Command line


```python
cpptraj_image --config data/conf/image.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.image.netcdf
```

## Cpptraj input

Performs multiple analysis and trajectory operations of a given trajector

### Get help

Command:


```python
cpptraj_input -h
```


```python
usage: cpptraj_input [-h] [--config CONFIG] --input_instructions_path INPUT_INSTRUCTIONS_PATH

Performs multiple analysis and trajectory operations of a given trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_instructions_path INPUT_INSTRUCTIONS_PATH
                        Path of the instructions file.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_instructions_path** (*str*): Path of the instructions file.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### Instructions file

input.in:


```python
parm data/input/cpptraj.convert.pdb
trajin data/input/cpptraj.convert.dcd
trajout data/output/output.netcdf netcdf
```

### YAML

#### Common file config


```python
properties:
  cpptraj_path: cpptraj
```

#### Docker file config


```python
properties:
  cpptraj_path: cpptraj
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  cpptraj_path: cpptraj
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_input --config data/conf/input.yml --input_instructions_path data/input/input.in
```

### JSON

#### Common file config


```python
{
  "properties": {
    "cpptraj_path": "cpptraj"
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "cpptraj_path": "cpptraj",
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "cpptraj_path": "cpptraj",
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_input --config data/conf/input.json --input_instructions_path data/input/input.in
```

## Cpptraj mask

Extracts a selection of atoms from a given cpptraj compatible trajectory.

### Get help

Command:


```python
cpptraj_mask -h
```


```python
usage: cpptraj_mask [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Extracts a selection of atoms from a given cpptraj compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output processed trajectory.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **output_cpptraj_path** (*str*): Path to the output processed trajectory.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **start** (*int*) - (1) Starting frame for slicing
    * **end** (*int*) - (-1) Ending frame for slicing
    * **step** (*int*) - (1) Step for slicing
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
* **out_parameters** (*dict*) - (None) Parameters for output trajectory.
    * **format** (*str*) - ("netcdf") Output trajectory format. Values: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
```

#### Docker file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_mask --config data/conf/mask.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.mask.netcdf
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_mask --config data/conf/mask.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.image.netcdf
```

## Cpptraj rgyr

Computes the radius of gyration (Rgyr) from a given cpptraj compatible trajectory.

### Get help

Command:


```python
cpptraj_rgyr -h
```


```python
usage: cpptraj_rgyr [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Computes the radius of gyration (Rgyr) from a given cpptraj compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output analysis.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **output_cpptraj_path** (*str*): Path to the output processed analysis.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **start** (*int*) - (1) Starting frame for slicing
    * **end** (*int*) - (-1) Ending frame for slicing
    * **step** (*int*) - (1) Step for slicing
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
```

#### Docker file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_rgyr --config data/conf/rgyr.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.rgyr.dat
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_rgyr --config data/conf/rgyr.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.rgyr.dat
```

## Cpptraj rms

Calculates the Root Mean Square deviation (RMSd) of a given cpptraj compatible trajectory.s.

### Get help

Command:


```python
cpptraj_rms -h
```


```python
usage: cpptraj_rms [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH [--input_exp_path INPUT_EXP_PATH] --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Calculates the Root Mean Square deviation (RMSd) of a given cpptraj compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_exp_path INPUT_EXP_PATH
                        Path to the experimental reference file (required if reference = experimental).

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output processed analysis.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **input_exp_path** (*str*): Path to the experimental reference file (required if reference = experimental).
* **output_cpptraj_path** (*str*): Path to the output processed analysis.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **start** (*int*) - (1) Starting frame for slicing
    * **end** (*int*) - (-1) Ending frame for slicing
    * **step** (*int*) - (1) Step for slicing
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
    * **reference** (*string*) - ("first") Reference definition. Values: first, average, experimental.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
    reference: first
```

#### Docker file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
    reference: first
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
    reference: first
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_rms --config data/conf/rms.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.rms.dat
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha",
      "reference": "first"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha",
      "reference": "first"
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha",
      "reference": "first"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_rms --config data/conf/rms.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.rms.dat
```

## Cpptraj rmsf

Calculates the Root Mean Square fluctuations (RMSf) of a given cpptraj compatible trajectory.

### Get help

Command:


```python
cpptraj_rmsf -h
```


```python
usage: cpptraj_rmsf [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH [--input_exp_path INPUT_EXP_PATH] --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Calculates the Root Mean Square fluctuations (RMSf) of a given cpptraj compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_exp_path INPUT_EXP_PATH
                        Path to the experimental reference file (required if reference = experimental).

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output processed analysis.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **input_exp_path** (*str*): Path to the experimental reference file (required if reference = experimental).
* **output_cpptraj_path** (*str*): Path to the output processed analysis.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **start** (*int*) - (1) Starting frame for slicing
    * **end** (*int*) - (-1) Ending frame for slicing
    * **step** (*int*) - (1) Step for slicing
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
    * **reference** (*string*) - ("first") Reference definition. Values: first, average, experimental.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
    reference: first
```

#### Docker file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
    reference: first
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  in_parameters:
    start: 1
    end: -1
    step: 1
    mask: c-alpha
    reference: first
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_rmsf --config data/conf/rmsf.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.rmsf.dat
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha",
      "reference": "first"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha",
      "reference": "first"
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha",
      "reference": "first"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_rmsf --config data/conf/rmsf.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.rmsf.dat
```

## Cpptraj slice

Extracts a particular trajectory slice from a given cpptraj compatible trajectory.

### Get help

Command:


```python
cpptraj_slice -h
```


```python
usage: cpptraj_slice [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Extracts a particular trajectory slice from a given cpptraj compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output processed trajectory.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **output_cpptraj_path** (*str*): Path to the output processed trajectory.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **start** (*int*) - (1) Starting frame for slicing
    * **end** (*int*) - (-1) Ending frame for slicing
    * **step** (*int*) - (1) Step for slicing
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
* **out_parameters** (*dict*) - (None) Parameters for output trajectory.
    * **format** (*str*) - ("netcdf") Output trajectory format. Values: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    start: 2
    end: 20
    step: 2
    mask: c-alpha
  out_parameters:
    format: netcdf
```

#### Docker file config


```python
properties:
  in_parameters:
    start: 2
    end: 20
    step: 2
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  in_parameters:
    start: 2
    end: 20
    step: 2
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_slice --config data/conf/slice.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.slice.netcdf
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_slice --config data/conf/slice.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.slice.netcdf
```

## Cpptraj snapshot

Extracts a particular snapshot from a given cpptraj compatible trajectory.

### Get help

Command:


```python
cpptraj_snapshot -h
```


```python
usage: cpptraj_snapshot [-h] --config CONFIG --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Extracts a particular snapshot from a given cpptraj compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output processed structure.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **output_cpptraj_path** (*str*): Path to the output processed structure.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **snapshot** (*int*) - (1) Frame to be captured for snapshot
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
* **out_parameters** (*dict*) - (None) Parameters for output trajectory.
    * **format** (*str*) - ("netcdf") Output trajectory format. Values: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    snapshot: 12
    mask: c-alpha
  out_parameters:
    format: pdb
```

#### Docker file config


```python
properties:
  in_parameters:
    snapshot: 12
    mask: c-alpha
  out_parameters:
    format: pdb
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  in_parameters:
    snapshot: 12
    mask: c-alpha
  out_parameters:
    format: pdb
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_snapshot --config data/conf/snapshot.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.snapshot.pdb
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "snapshot": 12,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "pdb"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "snapshot": 12,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "pdb"
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "snapshot": 12,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "pdb"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_snapshot --config data/conf/slice.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.slice.netcdf
```

## Cpptraj strip

Strips a defined set of atoms (mask) from a given cpptraj compatible trajectory.

### Get help

Command:


```python
cpptraj_strip -h
```


```python
usage: cpptraj_strip [-h] [--config CONFIG] --input_top_path INPUT_TOP_PATH --input_traj_path INPUT_TRAJ_PATH --output_cpptraj_path OUTPUT_CPPTRAJ_PATH

Strips a defined set of atoms (mask) from a given cpptraj compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_top_path INPUT_TOP_PATH
                        Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
  --output_cpptraj_path OUTPUT_CPPTRAJ_PATH
                        Path to the output processed trajectory.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_top_path** (*str*): Path to the input structure or topology file. Accepted formats: top, pdb, prmtop, parmtop, zip.
* **input_traj_path** (*str*): Path to the input trajectory to be processed. Accepted formats: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **output_cpptraj_path** (*str*): Path to the output processed trajectory.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **in_parameters** (*dict*) - (None) Parameters for input trajectory. Accepted parameters:
    * **start** (*int*) - (1) Starting frame for slicing
    * **end** (*int*) - (-1) Ending frame for slicing
    * **step** (*int*) - (1) Step for slicing
    * **mask** (*string*) - ("all-atoms") Mask definition. Values: c-alpha, backbone, all-atoms, heavy-atoms, side-chain, solute, ions, solvent.
* **out_parameters** (*dict*) - (None) Parameters for output trajectory.
    * **format** (*str*) - ("netcdf") Output trajectory format. Values: crd, cdf, netcdf, restart, ncrestart, restartnc, dcd, charmm, cor, pdb, mol2, trr, gro, binpos, xtc, cif, arc, sqm, sdf, conflib.
* **cpptraj_path** (*str*) - ("cpptraj") Path to the cpptraj executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('afandiadib/ambertools:serial') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  in_parameters:
    start: 2
    end: 20
    step: 2
    mask: c-alpha
  out_parameters:
    format: netcdf
```

#### Docker file config


```python
properties:
  in_parameters:
    start: 2
    end: 20
    step: 2
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: docker
  container_image: afandiadib/ambertools:serial
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  in_parameters:
    start: 2
    end: 20
    step: 2
    mask: c-alpha
  out_parameters:
    format: netcdf
  container_path: singularity
  container_image: ambertools.sif
  container_volume_path: /tmp
```

#### Command line


```python
cpptraj_strip --config data/conf/strip.yml --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.strip.netcdf
```

### JSON

#### Common file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    }
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "docker",
    "container_image": "afandiadib/ambertools:serial",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "in_parameters": {
      "start": 1,
      "end": -1,
      "step": 1,
      "mask": "c-alpha"
    },
    "out_parameters": {
      "format": "netcdf"
    },
    "container_path": "singularity",
    "container_image": "ambertools.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
cpptraj_strip --config data/conf/strip.json --input_top_path data/input/cpptraj.parm.top --input_traj_path data/input/cpptraj.traj.dcd --output_cpptraj_path data/output/output.strip.netcdf
```

## GROMACS cluster

Creates cluster structures from a given GROMACS compatible trajectory.

### Get help

Command:


```python
gmx_cluster -h
```


```python
usage: gmx_cluster [-h] [--config CONFIG] --input_structure_path INPUT_STRUCTURE_PATH --input_traj_path INPUT_TRAJ_PATH [--input_index_path INPUT_INDEX_PATH] --output_pdb_path OUTPUT_PDB_PATH

Creates cluster structures from a given GROMACS compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_index_path INPUT_INDEX_PATH
                        Path to the GROMACS index file. Accepted formats: ndx.

required arguments:
  --input_structure_path INPUT_STRUCTURE_PATH
                        Path to the input structure file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
  --output_pdb_path OUTPUT_PDB_PATH
                        Path to the output cluster file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Path to the input structure file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
* **input_traj_path** (*str*): Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
* **input_index_path** (*str*): Path to the GROMACS index file. Accepted formats: ndx.
* **output_pdb_path** (*str*): Path to the output cluster file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **fit_selection** (*str*) - ("System") - Group where the fitting will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **output_selection** (*str*) - ("System") Group that is going to be written in the output trajectory. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **dista** (*bool*) - (False) Use RMSD of distances instead of RMS deviation.
* **method** (*str*) - ("linkage") Method for cluster determination. Values: linkage, jarvis-patrick, monte-carlo, diagonalization, gromos
* **cutoff** (*float*) - (0.1) RMSD cut-off (nm) for two structures to be neighbor
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('gromacs/gromacs:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  fit_selection: System
  output_selection: System
  dista: False
  method: linkage
  cutoff: 0.1
```

#### Docker file config


```python
properties:
  fit_selection: System
  output_selection: System
  dista: False
  method: linkage
  cutoff: 0.1
  container_path: docker
  container_image: gromacs/gromacs:latest
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  fit_selection: System
  output_selection: System
  dista: False
  method: linkage
  cutoff: 0.1
  container_path: singularity
  container_image: gromacs.sif
  container_volume_path: /tmp
```

#### Command line


```python
gmx_cluster --config data/conf/cluster.yml --input_structure_path data/input/cluster.gro --input_traj_path data/input/cluster.trr --output_pdb_path data/output/output.cluster.pdb
```

### JSON

#### Common file config


```python
{
  "properties": {
    "fit_selection": "System",
    "output_selection": "System",
    "dista": false,
    "method": "linkage",
    "cutoff": 0.1
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "fit_selection": "System",
    "output_selection": "System",
    "dista": false,
    "method": "linkage",
    "cutoff": 0.1,
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "fit_selection": "System",
    "output_selection": "System",
    "dista": false,
    "method": "linkage",
    "cutoff": 0.1,
    "container_path": "singularity",
    "container_image": "gromacs.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
gmx_cluster --config data/conf/cluster.json --input_structure_path data/input/cluster.gro --input_traj_path data/input/cluster.trr --output_pdb_path data/output/output.cluster.pdb
```

## GROMACS energy

Extracts energy components from a given GROMACS energy file.

### Get help

Command:


```python
gmx_energy -h
```


```python
usage: gmx_energy [-h] [--config CONFIG] --input_energy_path INPUT_ENERGY_PATH --output_xvg_path OUTPUT_XVG_PATH

Extracts energy components from a given GROMACS energy file.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file

required arguments:
  --input_energy_path INPUT_ENERGY_PATH
                        Path to the input EDR file. Accepted formats: edr.
  --output_xvg_path OUTPUT_XVG_PATH
                        Path to the XVG output file. Accepted formats: xvg.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_energy_path** (*str*): Path to the input EDR file. Accepted formats: edr.
* **output_xvg_path** (*str*): Path to the XVG output file. Accepted formats: xvg.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **xvg** (*str*) - ("none") XVG plot formatting. Values: xmgrace, xmgr, none.
* **terms** (*list*) - (["Potential"]) Energy terms. Select one or more from values: Angle, Proper-Dih., Improper-Dih., LJ-14, Coulomb-14, LJ-(SR), Coulomb-(SR), Coul.-recip., Position-Rest., Potential, Kinetic-En., Total-Energy, Temperature, Pressure,  Constr.-rmsd, Box-X, Box-Y,  Box-Z, Volume, Density, pV, Enthalpy, Vir-XX, Vir-XY, Vir-XZ, Vir-YX, Vir-YY, Vir-YZ, Vir-ZX, Vir-ZY, Vir-ZZ, Pres-XX, Pres-XY, Pres-XZ, Pres-YX, Pres-YY,  Pres-YZ, Pres-ZX, Pres-ZY, Pres-ZZ, #Surf*SurfTen, Box-Vel-XX, Box-Vel-YY, Box-Vel-ZZ, Mu-X, Mu-Y, Mu-Z, T-Protein, T-non-Protein, Lamb-Protein, Lamb-non-Protein
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('gromacs/gromacs:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  terms: [Potential, Pressure]
```

#### Docker file config


```python
properties:
  terms: [Potential, Pressure]
  container_path: docker
  container_image: gromacs/gromacs:latest
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  terms: [Potential, Pressure]
  container_path: singularity
  container_image: gromacs.sif
  container_volume_path: /tmp
```

#### Command line


```python
gmx_energy --config data/conf/energy.yml --input_energy_path data/input/energy.edr --output_xvg_path data/output/output.energy.xvg
```

### JSON

#### Common file config


```python
{
  "properties": {
    "terms": ["Potential", "Pressure"]
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "terms": ["Potential", "Pressure"],
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "terms": ["Potential", "Pressure"],
    "container_path": "singularity",
    "container_image": "gromacs.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
gmx_energy --config data/conf/energy.json --input_energy_path data/input/energy.edr --output_xvg_path data/output/output.energy.xvg
```

## GROMACS image

Corrects periodicity (image) from a given GROMACS compatible trajectory file.

### Get help

Command:


```python
gmx_image -h
```


```python
usage: gmx_image [-h] [--config CONFIG] --input_traj_path INPUT_TRAJ_PATH --input_top_path INPUT_TOP_PATH [--input_index_path INPUT_INDEX_PATH] --output_traj_path OUTPUT_TRAJ_PATH

Corrects periodicity (image) from a given GROMACS compatible trajectory file.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_index_path INPUT_INDEX_PATH
                        Path to the GROMACS index file. Accepted formats: ndx.

required arguments:
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
  --input_top_path INPUT_TOP_PATH
                        Path to the GROMACS input topology file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
  --output_traj_path OUTPUT_TRAJ_PATH
                        Path to the output file. Accepted formats: xtc, trr, gro, g96, pdb, tng.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_traj_path** (*str*): Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
* **input_top_path** (*str*): Path to the GROMACS input topology file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
* **input_index_path** (*str*): Path to the GROMACS index file. Accepted formats: ndx.
* **output_traj_path** (*str*): Path to the output file. Accepted formats: xtc, trr, gro, g96, pdb, tng.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **fit_selection** (*str*) - ("System") - Group where the fitting will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **center_selection** (*str*) - ("System") Group where the trjconv will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **output_selection** (*str*) - ("System") Group that is going to be written in the output trajectory. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **pbc** (*str*) - ("mol") PBC treatment (see help text for full description). Values: none, mol, res, atom, nojump, cluster, whole.
* **center** (*bool*) - (True) Center atoms in box.
* **ur** (*str*) - ("compact") Unit-cell representation. Values: rect, tric, compact.
* **fit** (*str*) - ("none") Fit molecule to ref structure in the structure file. Values: none, rot+trans, rotxy+transxy, translation, transxy, progressive.
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('gromacs/gromacs:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  fit_selection: System
  center_selection: System
  output_selection: System
  pbc: mol
  center: True
  fit: rot+trans
  ur: compact
```

#### Docker file config


```python
properties:
  fit_selection: System
  center_selection: System
  output_selection: System
  pbc: mol
  center: True
  fit: rot+trans
  ur: compact
  container_path: docker
  container_image: gromacs/gromacs:latest
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  fit_selection: System
  center_selection: System
  output_selection: System
  pbc: mol
  center: True
  fit: rot+trans
  ur: compact
  container_path: singularity
  container_image: gromacs.sif
  container_volume_path: /tmp
```

#### Command line


```python
gmx_image --config data/conf/gmx_image.yml --input_traj_path data/input/image.trr --input_top_path data/input/image.gro --output_traj_path data/output/output.image.xtc
```

### JSON

#### Common file config


```python
{
  "properties": {
    "fit_selection": "System",
    "center_selection": "System",
    "output_selection": "System",
    "pbc": "mol",
    "center": true,
    "fit": "rot+trans",
    "ur": "compact"
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "fit_selection": "System",
    "center_selection": "System",
    "output_selection": "System",
    "pbc": "mol",
    "center": true,
    "fit": "rot+trans",
    "ur": "compact",
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "fit_selection": "System",
    "center_selection": "System",
    "output_selection": "System",
    "pbc": "mol",
    "center": true,
    "fit": "rot+trans",
    "ur": "compact",
    "container_path": "singularity",
    "container_image": "gromacs.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
gmx_image --config data/conf/gmx_image.json --input_traj_path data/input/image.trr --input_top_path data/input/image.gro --output_traj_path data/output/output.image.xtc
```

## GROMACS rgyr

Computes the radius of gyration (Rgyr) of a molecule about the x-, y- and z-axes, as a function of time, from a given GROMACS compatible trajectory.

### Get help

Command:


```python
gmx_rgyr -h
```


```python
usage: gmx_rgyr [-h] [--config CONFIG] --input_structure_path INPUT_STRUCTURE_PATH --input_traj_path INPUT_TRAJ_PATH [--input_index_path INPUT_INDEX_PATH] --output_xvg_path OUTPUT_XVG_PATH

Computes the radius of gyration (Rgyr) of a molecule about the x-, y- and z-axes, as a function of time, from a given GROMACS compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_index_path INPUT_INDEX_PATH
                        Path to the GROMACS index file. Accepted formats: ndx.

required arguments:
  --input_structure_path INPUT_STRUCTURE_PATH
                        Path to the input structure file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
  --output_xvg_path OUTPUT_XVG_PATH
                        Path to the XVG output file. Accepted formats: xvg.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Path to the input structure file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
* **input_traj_path** (*str*): Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
* **input_index_path** (*str*): Path to the GROMACS index file. Accepted formats: ndx.
* **output_xvg_path** (*str*): Path to the XVG output file. Accepted formats: xvg.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **xvg** (*str*) - ("none") XVG plot formatting. Values: xmgrace, xmgr, none.
* **selection** (*str*) - ("System") Group where the rgyr will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('gromacs/gromacs:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  selection: System
```

#### Docker file config


```python
properties:
  selection: System
  container_path: docker
  container_image: gromacs/gromacs:latest
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  selection: System
  container_path: singularity
  container_image: gromacs.sif
  container_volume_path: /tmp
```

#### Command line


```python
gmx_rgyr --config data/conf/gmx_rgyr.yml --input_structure_path data/input/rgyr.gro --input_traj_path data/input/rgyr.trr --output_xvg_path data/output/output.rgyr.xvg
```

### JSON

#### Common file config


```python
{
  "properties": {
    "selection": "System"
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "selection": "System",
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "selection": "System",
    "container_path": "singularity",
    "container_image": "gromacs.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
gmx_rgyr --config data/conf/gmx_rgyr.json --input_structure_path data/input/rgyr.gro --input_traj_path data/input/rgyr.trr --output_xvg_path data/output/output.rgyr.xvg
```

## GROMACS rms

Performs a Root Mean Square deviation (RMSd) analysis from a given GROMACS compatible trajectory.

### Get help

Command:


```python
gmx_rms -h
```


```python
usage: gmx_rms [-h] [--config CONFIG] --input_structure_path INPUT_STRUCTURE_PATH --input_traj_path INPUT_TRAJ_PATH [--input_index_path INPUT_INDEX_PATH] --output_xvg_path OUTPUT_XVG_PATH

Performs a Root Mean Square deviation (RMSd) analysis from a given GROMACS compatible trajectory.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_index_path INPUT_INDEX_PATH
                        Path to the GROMACS index file. Accepted formats: ndx.

required arguments:
  --input_structure_path INPUT_STRUCTURE_PATH
                        Path to the input structure file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
  --output_xvg_path OUTPUT_XVG_PATH
                        Path to the XVG output file. Accepted formats: xvg.

```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Path to the input structure file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
* **input_traj_path** (*str*): Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
* **input_index_path** (*str*): Path to the GROMACS index file. Accepted formats: ndx.
* **output_xvg_path** (*str*): Path to the XVG output file. Accepted formats: xvg.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **xvg** (*str*) - ("none") XVG plot formatting. Values: xmgrace, xmgr, none.
* **selection** (*str*) - ("System") Group where the rms will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('gromacs/gromacs:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  selection: System
```

#### Docker file config


```python
properties:
  selection: System
  container_path: docker
  container_image: gromacs/gromacs:latest
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  selection: System
  container_path: singularity
  container_image: gromacs.sif
  container_volume_path: /tmp
```

#### Command line


```python
gmx_rms --config data/conf/gmx_rms.yml --input_structure_path data/input/rgyr.gro --input_traj_path data/input/rgyr.trr --output_xvg_path data/output/output.rms.xvg
```

### JSON

#### Common file config


```python
{
  "properties": {
    "selection": "System"
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "selection": "System",
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "selection": "System",
    "container_path": "singularity",
    "container_image": "gromacs.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
gmx_rms --config data/conf/gmx_rms.json --input_structure_path data/input/rgyr.gro --input_traj_path data/input/rgyr.trr --output_xvg_path data/output/output.rms.xvg
```

## GROMACS trjconv structure

Converts between GROMACS compatible structure file formats and/or extracts a selection of atoms.

### Get help

Command:


```python
gmx_trjconv_str -h
```


```python
usage: gmx_trjconv_str [-h] [--config CONFIG] --input_structure_path INPUT_STRUCTURE_PATH --input_top_path INPUT_TOP_PATH [--input_index_path INPUT_INDEX_PATH] --output_str_path OUTPUT_STR_PATH

Converts between GROMACS compatible structure file formats and/or extracts a selection of atoms.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_index_path INPUT_INDEX_PATH
                        Path to the GROMACS index file. Accepted formats: ndx.

required arguments:
  --input_structure_path INPUT_STRUCTURE_PATH
                        Path to the input structure file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
  --input_top_path INPUT_TOP_PATH
                        Path to the GROMACS input topology file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
  --output_str_path OUTPUT_STR_PATH
                        Path to the output file. Accepted formats: xtc, trr, gro, g96, pdb, tng.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Path to the input structure file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
* **input_top_path** (*str*): Path to the GROMACS input topology file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
* **input_index_path** (*str*): Path to the GROMACS index file. Accepted formats: ndx.
* **output_str_path** (*str*): Path to the output file. Accepted formats: xtc, trr, gro, g96, pdb, tng.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **selection** (*str*) - ("System") Group where the trjconv will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('gromacs/gromacs:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  selection: System
```

#### Docker file config


```python
properties:
  selection: System
  container_path: docker
  container_image: gromacs/gromacs:latest
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  selection: System
  container_path: singularity
  container_image: gromacs.sif
  container_volume_path: /tmp
```

#### Command line


```python
gmx_trjconv_str --config data/conf/gmx_trjconv_str.yml --input_structure_path data/input/trjconv.str.gro --input_top_path data/input/trjconv.str.gro --output_str_path data/output/output.trjconv.str.pdb
```

### JSON

#### Common file config


```python
{
  "properties": {
    "selection": "System"
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "selection": "System",
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "selection": "System",
    "container_path": "singularity",
    "container_image": "gromacs.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
gmx_trjconv_str --config data/conf/gmx_trjconv_str.json --input_structure_path data/input/trjconv.str.gro --input_top_path data/input/trjconv.str.gro --output_str_path data/output/output.trjconv.str.pdb
```

## GROMACS trjconv structure ensemble

Extracts an ensemble of frames containing a selection of atoms from GROMACS compatible trajectory files.

### Get help

Command:


```python
gmx_trjconv_str_ens -h
```


```python
usage: gmx_trjconv_str_ens [-h] [--config CONFIG] --input_traj_path INPUT_TRAJ_PATH --input_top_path INPUT_TOP_PATH [--input_index_path INPUT_INDEX_PATH] --output_str_ens_path OUTPUT_STR_ENS_PATH

Extracts an ensemble of frames containing a selection of atoms from GROMACS compatible trajectory files.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_index_path INPUT_INDEX_PATH
                        Path to the GROMACS index file. Accepted formats: ndx.

required arguments:
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
  --input_top_path INPUT_TOP_PATH
                        Path to the GROMACS input topology file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
  --output_str_ens_path OUTPUT_STR_ENS_PATH
                        Path to the output file. Accepted formats: zip.

```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_traj_path** (*str*): Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
* **input_top_path** (*str*): Path to the GROMACS input topology file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
* **input_index_path** (*str*): Path to the GROMACS index file. Accepted formats: ndx.
* **output_str_ens_path** (*str*): Path to the output file. Accepted formats: zip.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **selection** (*str*) - ("System") Group where the trjconv will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **start** (*int*) - (0) Time of first frame to read from trajectory (default unit ps).
* **end** (*int*) - (0) Time of last frame to read from trajectory (default unit ps).
* **dt** (*int*) - (0) Only write frame when t MOD dt = first time (ps).
* **output_name** (*str*) - ("output") File name for ensemble of output files.
* **output_type** (*str*) - ("pdb") File type for ensemble of output files. Values: gro, g96, pdb.
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('gromacs/gromacs:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  selection: System
  start: 0
  end: 10
  dt: 1
  output_name: output
  output_type: pdb
```

#### Docker file config


```python
properties:
  selection: System
  start: 0
  end: 10
  dt: 1
  output_name: output
  output_type: pdb
  container_path: docker
  container_image: gromacs/gromacs:latest
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  selection: System
  start: 0
  end: 10
  dt: 1
  output_name: output
  output_type: pdb
  container_path: singularity
  container_image: gromacs.sif
  container_volume_path: /tmp
```

#### Command line


```python
gmx_trjconv_str_ens --config data/conf/gmx_trjconv_str_ens.yml --input_traj_path data/input/trjconv.str.ens.trr --input_top_path data/input/trjconv.str.ens.gro --output_str_ens_path data/output/output.trjconv.str.ens.zip
```

### JSON

#### Common file config


```python
{
  "properties": {
    "selection": "System",
    "start": 0,
    "end": 10,
    "dt": 1,
    "output_name": "output",
    "output_type": "pdb"
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "selection": "System",
    "start": 0,
    "end": 10,
    "dt": 1,
    "output_name": "output",
    "output_type": "pdb",
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "selection": "System",
    "start": 0,
    "end": 10,
    "dt": 1,
    "output_name": "output",
    "output_type": "pdb",
    "container_path": "singularity",
    "container_image": "gromacs.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
gmx_trjconv_str_ens --config data/conf/gmx_trjconv_str_ens.json --input_traj_path data/input/trjconv.str.ens.trr --input_top_path data/input/trjconv.str.ens.gro --output_str_ens_path data/output/output.trjconv.str.ens.zip
```

## GROMACS trjconv trajectory

Converts between GROMACS compatible trajectory file formats and/or extracts a selection of atoms.

### Get help

Command:


```python
gmx_trjconv_trj -h
```


```python
usage: gmx_trjconv_trj [-h] [--config CONFIG] --input_traj_path INPUT_TRAJ_PATH [--input_index_path INPUT_INDEX_PATH] --output_traj_path OUTPUT_TRAJ_PATH

Converts between GROMACS compatible trajectory file formats and/or extracts a selection of atoms.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file
  --input_index_path INPUT_INDEX_PATH
                        Path to the GROMACS index file. Accepted formats: ndx.

required arguments:
  --input_traj_path INPUT_TRAJ_PATH
                        Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
  --output_traj_path OUTPUT_TRAJ_PATH
                        Path to the output file. Accepted formats: xtc, trr, gro, g96, pdb, tng.
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_traj_path** (*str*): Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
* **input_index_path** (*str*): Path to the GROMACS index file. Accepted formats: ndx.
* **output_traj_path** (*str*): Path to the output file. Accepted formats: xtc, trr, gro, g96, pdb, tng.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **selection** (*str*) - ("System") Group where the trjconv will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
* **start** (*int*) - (0) Time of first frame to read from trajectory (default unit ps).
* **end** (*int*) - (0) Time of last frame to read from trajectory (default unit ps).
* **dt** (*int*) - (0) Only write frame when t MOD dt = first time (ps).
* **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **container_path** (*string*) - (None) Container path definition.
* **container_image** (*string*) - ('gromacs/gromacs:latest') Container image definition.
* **container_volume_path** (*string*) - ('/tmp') Container volume path definition.
* **container_working_dir** (*string*) - (None) Container working directory definition.
* **container_user_id** (*string*) - (None) Container user_id definition.
* **container_shell_path** (*string*) - ('/bin/bash') Path to default shell inside the container.

### YAML

#### Common file config


```python
properties:
  selection: System
  start: 0
  end: 0
  dt: 0
```

#### Docker file config


```python
properties:
  selection: System
  start: 0
  end: 0
  dt: 0
  container_path: docker
  container_image: gromacs/gromacs:latest
  container_volume_path: /tmp
```

#### Singularity file config


```python
properties:
  selection: System
  start: 0
  end: 0
  dt: 0
  container_path: singularity
  container_image: gromacs.sif
  container_volume_path: /tmp
```

#### Command line


```python
gmx_trjconv_trj --config data/conf/gmx_trjconv_trj.yml --input_traj_path data/input/trjconv.trj.trr --output_traj_path data/output/output.trjconv.trj.xtc
```

### JSON

#### Common file config


```python
{
  "properties": {
    "selection": "System",
    "start": 0,
    "end": 0,
    "dt": 0
  }
}
```

#### Docker file config


```python
{
  "properties": {
    "selection": "System",
    "start": 0,
    "end": 0,
    "dt": 0,
    "container_path": "docker",
    "container_image": "gromacs/gromacs:latest",
    "container_volume_path": "/tmp"
  }
}
```

#### Singularity file config


```python
{
  "properties": {
    "selection": "System",
    "start": 0,
    "end": 0,
    "dt": 0,
    "container_path": "singularity",
    "container_image": "gromacs.sif",
    "container_volume_path": "/tmp"
  }
}
```

#### Command line


```python
gmx_trjconv_trj --config data/conf/gmx_trjconv_trj.json --input_traj_path data/input/trjconv.trj.trr --output_traj_path data/output/output.trjconv.trj.xtc
```
