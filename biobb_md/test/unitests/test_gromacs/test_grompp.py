from biobb_common.tools import test_fixtures as fx
from gromacs.grompp import Grompp


class TestGrompp(object):
    def setUp(self):
        fx.test_setup(self,'grompp')

    def tearDown(self):
        fx.test_teardown(self)

    def test_grompp(self):
        returncode= Grompp(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_tpr_path'])
        assert fx.exe_success(returncode)
