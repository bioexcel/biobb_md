from biobb_common.tools import test_fixtures as fx
from gromacs.cluster import Cluster


class TestCluster(object):
    def setUp(self):
        fx.test_setup(self,'cluster')

    def tearDown(self):
        fx.test_teardown(self)

    def test_cluster(self):
        returncode= Cluster(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.exe_success(returncode)
