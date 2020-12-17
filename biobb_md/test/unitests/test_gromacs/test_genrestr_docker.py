from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.genrestr import genrestr


class TestGenrestrDocker:
    def setUp(self):
        fx.test_setup(self, 'genrestr_docker')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_genrestr_docker(self):
        returncode = genrestr(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_itp_path'])
        assert fx.equal(self.paths['output_itp_path'], self.paths['ref_output_itp_path'])
        assert fx.exe_success(returncode)
