from biobb_common.tools import test_fixtures as fx
from gromacs.genrestr import Genrestr


class TestGenrestr(object):
    def setUp(self):
        fx.test_setup(self,'genrestr')

    def tearDown(self):
        fx.test_teardown(self)

    def test_genrestr(self):
        returncode= Genrestr(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.exe_success(returncode)
