from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.gmxselect import gmxselect


class TestSelectDocker:
    def setUp(self):
        fx.test_setup(self, 'gmxselect_docker')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_select_docker(self):
        returncode = gmxselect(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_ndx_path'])
        assert fx.equal(self.paths['output_ndx_path'], self.paths['ref_output_ndx_path'])
        assert fx.exe_success(returncode)
