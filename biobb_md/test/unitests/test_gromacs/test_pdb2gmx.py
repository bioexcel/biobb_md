from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.pdb2gmx import pdb2gmx


class TestPdb2gmx:
    def setUp(self):
        fx.test_setup(self, 'pdb2gmx')

    def tearDown(self):
        fx.test_teardown(self)

    def test_pdb2gmx(self):
        returncode = pdb2gmx(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.equal(self.paths['output_gro_path'], self.paths['ref_output_gro_path'])
        assert fx.exe_success(returncode)
