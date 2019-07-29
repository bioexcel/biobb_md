from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.grompp import Grompp
from biobb_md.gromacs.common import gmx_check


class TestGrompp():
    def setUp(self):
        fx.test_setup(self,'grompp')

    def tearDown(self):
        #fx.test_teardown(self)
        pass

    def test_grompp(self):
        returncode = Grompp(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_tpr_path'])
        assert gmx_check(self.paths['output_tpr_path'], self.paths['ref_output_tpr_path'], gmx=self.properties.get('gmx_path','gmx'))
        assert fx.exe_success(returncode)
