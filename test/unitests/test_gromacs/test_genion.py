from biobb_common.tools import test_fixtures as fx
from gromacs.genion import Genion


class TestGenion(object):
    def setUp(self):
        fx.test_setup(self,'genion')

    def tearDown(self):
        fx.test_teardown(self)

    def test_genion(self):
        returncode= Genion(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.exe_success(returncode)
