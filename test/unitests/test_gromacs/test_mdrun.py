from biobb_common.tools import test_fixtures as fx
from gromacs.mdrun import Mdrun


class TestMdrun(object):
    def setUp(self):
        fx.test_setup(self,'mdrun')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_mdrun(self):
        returncode= Mdrun(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_trr_path'])
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.not_empty(self.paths['output_edr_path'])
        assert fx.not_empty(self.paths['output_log_path'])
        assert fx.exe_success(returncode)
