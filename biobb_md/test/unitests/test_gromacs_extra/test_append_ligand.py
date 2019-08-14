from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs_extra.append_ligand import AppendLigand

class TestAppendLigand():
    def setUp(self):
        fx.test_setup(self,'appendligand')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_append_ligand(self):
        returncode= AppendLigand(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])
        assert fx.exe_success(returncode)
