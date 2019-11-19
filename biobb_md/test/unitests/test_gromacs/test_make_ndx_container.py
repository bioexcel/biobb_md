from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.make_ndx import MakeNdx

class TestMakeNdx():
    def setUp(self):
        fx.test_setup(self, 'make_ndx_container')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_make_ndx(self):
        returncode = MakeNdx(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_ndx_path'])
        assert fx.equal(self.paths['output_ndx_path'], self.paths['ref_output_ndx_path'])
        assert fx.exe_success(returncode)
