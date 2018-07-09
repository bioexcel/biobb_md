BIOBB_MD=$HOME/projects/biobb_md
cwltool $BIOBB_MD/cwl/gromacs/pdb2gmx.cwl $BIOBB_MD/cwl/test/gromacs/pdb2gmx.yml
cwltool $BIOBB_MD/cwl/gromacs/editconf.cwl $BIOBB_MD/cwl/test/gromacs/editconf.yml
cwltool $BIOBB_MD/cwl/gromacs/genion.cwl $BIOBB_MD/cwl/test/gromacs/genion.yml
cwltool $BIOBB_MD/cwl/gromacs/cluster.cwl $BIOBB_MD/cwl/test/gromacs/cluster.yml
