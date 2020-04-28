from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.gmxselect import Gmxselect

class TestSelect:
    def setUp(self):
        fx.test_setup(self, 'gmxselect_singularity')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_select(self):
        returncode = Gmxselect(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_ndx_path'])
        assert fx.equal(self.paths['output_ndx_path'], self.paths['ref_output_ndx_path'])
        assert fx.exe_success(returncode)
