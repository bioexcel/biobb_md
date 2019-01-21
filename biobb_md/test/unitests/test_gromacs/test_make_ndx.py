from biobb_common.tools import test_fixtures as fx
from gromacs.make_ndx import MakeNdx

class TestMakeNdx(object):
    def setUp(self):
        fx.test_setup(self,'make_ndx')

    def tearDown(self):
        #fx.test_teardown(self)
        pass

    def test_make_ndx(self):
        returncode = MakeNdx(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_ndx_path'])
        assert fx.equal(self.paths['output_ndx_path'], self.paths['ref_output_ndx_path'])
        assert fx.exe_success(returncode)
