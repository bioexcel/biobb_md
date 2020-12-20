from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs_extra.append_ligand import append_ligand


class TestAppendLigand:
    def setUp(self):
        fx.test_setup(self, 'append_ligand')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_append_ligand(self):
        returncode = append_ligand(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])
        assert fx.exe_success(returncode)
