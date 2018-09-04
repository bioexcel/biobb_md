#!/usr/bin/env bash

BIOBB_MD=$HOME/projects/biobb_md
cwltool $BIOBB_MD/cwl/gromacs/pdb2gmx.cwl $BIOBB_MD/cwl/test/gromacs/pdb2gmx.yml
cwltool $BIOBB_MD/cwl/gromacs/editconf.cwl $BIOBB_MD/cwl/test/gromacs/editconf.yml
cwltool $BIOBB_MD/cwl/gromacs/genion.cwl $BIOBB_MD/cwl/test/gromacs/genion.yml
cwltool $BIOBB_MD/cwl/gromacs/cluster.cwl $BIOBB_MD/cwl/test/gromacs/cluster.yml
cwltool $BIOBB_MD/cwl/gromacs/genrestr.cwl $BIOBB_MD/cwl/test/gromacs/genrestr.yml
cwltool $BIOBB_MD/cwl/gromacs/grompp.cwl $BIOBB_MD/cwl/test/gromacs/grompp.yml
cwltool $BIOBB_MD/cwl/gromacs/mdrun.cwl $BIOBB_MD/cwl/test/gromacs/mdrun.yml
cwltool $BIOBB_MD/cwl/gromacs/solvate.cwl $BIOBB_MD/cwl/test/gromacs/solvate.yml
cwltool $BIOBB_MD/cwl/gromacs/make_ndx.cwl $BIOBB_MD/cwl/test/gromacs/make_ndx.yml
cwltool $BIOBB_MD/cwl/gromacs/rms.cwl $BIOBB_MD/cwl/test/gromacs/rms.yml
cwltool $BIOBB_MD/cwl/gromacs_extra/ndx2resttop.cwl $BIOBB_MD/cwl/test/gromacs_extra/ndx2resttop.yml
