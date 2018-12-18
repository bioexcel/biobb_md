from biobb_common.tools import test_fixtures as fx
from gromacs.editconf import Editconf

class TestEditconf(object):
    def setUp(self):
        fx.test_setup(self,'editconf')

    def tearDown(self):
        fx.test_teardown(self)


    def test_editconf(self):
        returncode= Editconf(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['input_gro_path'])
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.exe_success(returncode)
