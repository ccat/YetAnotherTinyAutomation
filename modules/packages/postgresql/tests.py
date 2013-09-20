# coding:utf-8
import unittest

#import interfaces
import basics
from ... import manager
#import monitor

from ... import default_settings

class PostgresqlTest(unittest.TestCase):

    def setUp(self):
        self.manager=manager.init(settings=default_settings)
        self.postgres=basics.Postgresql("postgresql",self.manager.dataStore.get("localhost"))
        self.postgres.configure(version="9.1")
        self.postgres.addDBcluster(clusterName="testDB",dir="/tmp/testDB",encoding="UTF8",locale=None,username="postgres")

        import os
        if(os.path.exists("/tmp/testDB")):
            command=["sudo","-u",self.postgres.username,"rm","-rf",'/tmp/testDB']
            import subprocess
            subprocess.call(command)

    def test_initialize(self):
        self.assertEqual(self.postgres.username,"postgres")
        #self.assertEqual(self.postgres.bin_path,"/usr/lib/postgresql/9.1/bin") #for ubuntu
        #self.assertEqual(self.postgres.dbClusters["default"],{"dir":"","encoding":"UTF8","locale":None,"superuser":"postgres"}) #for ubuntu
        #self.postgres.addDBcluster(clusterName="default",dir="/tmp/testDB",encoding="UTF8",locale=None,username="postgres")
        #self.assertEqual(self.postgres.dbClusters["default"]["dir"],"/tmp/testDB")

    #def test_install(self):
    #    self.manager.dataStore.get("localhost").diagnosis()
    #    self.postgres.install


    """
    def test_lowlevel_initdb(self):
        self.postgres.diagnosis()
        result=self.postgres.lowlevel.initdb("testDB")
        self.assertEqual(result["returncode"],0)
        result=self.postgres.lowlevel.initdb("testDB")
        self.assertEqual(result["returncode"],1)

    def test_lowlevel_pg_ctl(self):
        self.postgres.diagnosis()
        result=self.postgres.lowlevel.pg_ctl.initdb("testDB")
        self.assertEqual(result["returncode"],0)
        result=self.postgres.lowlevel.pg_ctl.initdb("testDB")
        self.assertEqual(result["returncode"],1)
        result=self.postgres.lowlevel.pg_ctl.start("testDB",wait=True,timeout=10)
        self.assertEqual(result["returncode"],0)

    def test_diagnosis(self):
        result=self.postgres.diagnosis()
        self.assertEqual(result,
                         {"level":"NORMAL",
                                "version":{"level":"NORMAL","config":"9.1","status":"9.1"},
                                "bin_path":{"level":"INFO","config":None,"status":"/usr/lib/postgresql/9.1/bin"},
                        })
    """

if __name__ == '__main__':
    unittest.main()

