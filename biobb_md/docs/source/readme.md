[![](https://readthedocs.org/projects/biobb-md/badge/?version=latest)](https://biobb-md.readthedocs.io/en/latest/?badge=latest)
[![](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](https://anaconda.org/bioconda/biobb_md)
[![](https://img.shields.io/badge/docker-Quay.io-blue)](https://quay.io/repository/biocontainers/biobb_md)
[![](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# biobb_md

### Introduction
Biobb_md is the Biobb module collection to perform molecular dynamics simulations.
Biobb (BioExcel building blocks) packages are Python building blocks that
create new layer of compatibility and interoperability over popular
bioinformatics tools.
The latest documentation of this package can be found in our readthedocs site:
[latest API documentation](http://biobb-md.readthedocs.io/en/latest/).

### Version
v3.7.1 2021.3

### Installation
Using PIP:

> **Important:** PIP only installs the package. All the dependencies must be installed separately. To perform a complete installation, please use ANACONDA, DOCKER or SINGULARITY.

* Installation:


        pip install "biobb_md>=3.7.1"


* Usage: [Python API documentation](https://biobb-md.readthedocs.io/en/latest/modules.html)

Using ANACONDA:

* Installation:


        conda install -c bioconda "biobb_md>=3.7.1"


* Usage: With conda installation BioBBs can be used with the [Python API documentation](https://biobb-md.readthedocs.io/en/latest/modules.html) and the [Command Line documentation](https://biobb-md.readthedocs.io/en/latest/command_line.html)

Using DOCKER:

* Installation:


        docker pull quay.io/biocontainers/biobb_md:3.7.1--pyhdfd78af_0


* Usage:


        docker run quay.io/biocontainers/biobb_md:3.7.1--pyhdfd78af_0 <command>


Using SINGULARITY:

**MacOS users**: it's strongly recommended to avoid Singularity and use **Docker** as containerization system.

* Installation:


        singularity pull --name biobb_md.sif shub://bioexcel/biobb_md


* Usage:


        singularity exec biobb_md.sif <command>


The command list and specification can be found at the [Command Line documentation](https://biobb-md.readthedocs.io/en/latest/command_line.html).


### Copyright & Licensing
This software has been developed in the [MMB group](http://mmb.irbbarcelona.org) at the [BSC](http://www.bsc.es/) & [IRB](https://www.irbbarcelona.org/) for the [European BioExcel](http://bioexcel.eu/), funded by the European Commission (EU H2020 [823830](http://cordis.europa.eu/projects/823830), EU H2020 [675728](http://cordis.europa.eu/projects/675728)).

* (c) 2015-2021 [Barcelona Supercomputing Center](https://www.bsc.es/)
* (c) 2015-2021 [Institute for Research in Biomedicine](https://www.irbbarcelona.org/)

Licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), see the file LICENSE for details.

![](https://bioexcel.eu/wp-content/uploads/2019/04/Bioexcell_logo_1080px_transp.png "Bioexcel")
