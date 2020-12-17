from biobb_common.tools import test_fixtures as fx
from biobb_md.gromacs.editconf import editconf

class TestEditconfDocker():
    def setUp(self):
        fx.test_setup(self, 'editconf_docker')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_editconf_docker(self):
        editconf(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.equal(self.paths['output_gro_path'], self.paths['ref_output_gro_path'])
