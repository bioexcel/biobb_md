import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_md",
    version="3.7.1",
    author="Biobb developers",
    author_email="pau.andrio@bsc.es",
    description="Biobb_md is the Biobb module collection to perform molecular dynamics simulations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_md",
    project_urls={
        "Documentation": "http://biobb_md.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    install_requires=['biobb_common==3.7.0'],
    python_requires='==3.7.*',
    entry_points={
        "console_scripts": [
            "editconf = biobb_md.gromacs.editconf:main",
            "genion = biobb_md.gromacs.genion:main",
            "genrestr = biobb_md.gromacs.genrestr:main",
            "grompp = biobb_md.gromacs.grompp:main",
            "make_ndx = biobb_md.gromacs.make_ndx:main",
            "gmxselect = biobb_md.gromacs.gmxselect:main",
            "mdrun = biobb_md.gromacs.mdrun:main",
            "grompp_mdrun = biobb_md.gromacs.grompp_mdrun:main",
            "pdb2gmx = biobb_md.gromacs.pdb2gmx:main",
            "solvate = biobb_md.gromacs.solvate:main",
            "ndx2resttop = biobb_md.gromacs_extra.ndx2resttop:main",
            "append_ligand = biobb_md.gromacs_extra.append_ligand:main"
        ]
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
