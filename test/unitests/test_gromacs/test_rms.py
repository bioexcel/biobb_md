from biobb_common.tools import test_fixtures as fx
from gromacs.rms import Rms


class TestRms(object):
    def setUp(self):
        fx.test_setup(self,'rms')

    def tearDown(self):
        fx.test_teardown(self)

    def test_rms(self):
        returncode= Rms(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_xvg_path'])
        assert fx.exe_success(returncode)
