from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.pdb2gmx import Pdb2gmx

class TestPdb2gmx():
    def setUp(self):
        fx.test_setup(self,'pdb2gmx')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_pdb2gmx(self):
        returncode= Pdb2gmx(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.equal(self.paths['output_gro_path'], self.paths['ref_output_gro_path'])
        assert fx.exe_success(returncode)
