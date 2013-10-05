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
        self.postgres.configure(version="9.1.9")
        self.postgres.addDBcluster(clusterName="testDB",dir="/tmp/testDB",encoding="UTF8",locale=None,username="postgres")

        import os
        if(os.path.exists("/tmp/testDB")):
            command=["sudo","-u",self.postgres.username,"rm","-rf",'/tmp/testDB']
            import subprocess
            subprocess.call(command)

    def test_initialize(self):
        self.assertEqual(self.postgres.username,"postgres")

    def test_diagnosis(self):
        result=self.postgres.diagnosis()
        self.assertEqual(result,
                         {"level":"NORMAL",
                                "installed":{"level":"NORMAL","config":True,"status":True},
                                "version":{"level":"NORMAL","config":"9.1.9","status":"9.1.9"},
                        })
    
    def test_backup(self):
        result=self.postgres.diagnosis()
        self.postgres.lowlevel.pg_dumpall(filename="./backup.sql")
        self.postgres.lowlevel.pg_dumpall(filename="./backup_%num%.sql")
        self.postgres.lowlevel.pg_dumpall(filename="./backup_%num%.sql")
        self.postgres.lowlevel.pg_dumpall(filename="./backup_%num%.sql.gz",withCompress=True)
        self.postgres.lowlevel.pg_dumpall(filename="./backup_%num%.sql",withClean=True,withColumnInsert=True)
        import os
        self.assertTrue(os.path.exists("./backup.sql"))
        result=self.postgres.lowlevel.psql_restore(filename="./backup.sql")


if __name__ == '__main__':
    unittest.main()

