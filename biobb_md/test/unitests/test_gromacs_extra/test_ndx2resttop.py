from biobb_common.tools import test_fixtures as fx
from gromacs_extra.ndx2resttop import Ndx2resttop

class TestNdx2resttop(object):
    def setUp(self):
        fx.test_setup(self,'ndx2resttop')

    def tearDown(self):
        fx.test_teardown(self)

    def test_ndx2resttop(self):
        returncode= Ndx2resttop(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['input_ndx_path'])
        assert fx.not_empty(self.paths['input_top_zip_path'])
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.exe_success(returncode)
