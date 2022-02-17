from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.grompp import grompp
from biobb_md.gromacs.common import gmx_check


class TestGromppDocker():
    def setUp(self):
        fx.test_setup(self, 'grompp_docker')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_grompp(self):
        returncode = grompp(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_tpr_path'])
        assert gmx_check(self.paths['output_tpr_path'], self.paths['ref_output_tpr_path'], gmx=self.properties.get('gmx_path','gmx'))
        assert fx.exe_success(returncode)
