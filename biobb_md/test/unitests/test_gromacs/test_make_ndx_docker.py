from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.make_ndx import make_ndx


class TestMakeNdxDocker:
    def setUp(self):
        fx.test_setup(self, 'make_ndx_docker')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_make_ndx_docker(self):
        returncode = make_ndx(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_ndx_path'])
        assert fx.equal(self.paths['output_ndx_path'], self.paths['ref_output_ndx_path'])
        assert fx.exe_success(returncode)
