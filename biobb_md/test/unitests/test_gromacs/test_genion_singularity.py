from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.genion import genion


class TestGenionSingularity:
    def setUp(self):
        fx.test_setup(self, 'genion_singularity')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_genion_singularity(self):
        returncode = genion(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_itp_path'])
        assert fx.equal(self.paths['output_itp_path'], self.paths['ref_output_itp_path'])
        assert fx.exe_success(returncode)
