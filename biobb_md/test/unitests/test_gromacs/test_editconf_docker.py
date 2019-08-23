from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.editconf import Editconf

class TestEditconfDocker():
    def setUp(self):
        fx.test_setup(self,'editconf_docker')

    def tearDown(self):
        fx.test_teardown(self)

    def test_editconf_docker(self):
        Editconf(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.equal(self.paths['output_gro_path'], self.paths['ref_output_gro_path'])
