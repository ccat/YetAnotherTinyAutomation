

import sys
sys.path.append("../")

import settings
from modules  import manager

def main():
    #sudo python ./examples/postgresql_install.py <version>
    
    manage=manager.init(settings=settings)
    postgresql=settings.Postgresql("postgresql",manage.dataStore.get("localhost"))

    argvs = sys.argv
    if(len(argvs)==2):
        postgresql.configure(version=argvs[1])
    
    print "Running diagnosis"
    result=manage.dataStore.get("localhost").diagnosis()
    print result
    print "Running install"
    postgresql.install()

        #self.assertEqual(self.postgres.bin_path,"/usr/lib/postgresql/9.1/bin") #for ubuntu
        #self.assertEqual(self.postgres.dbClusters["default"],{"dir":"","encoding":"UTF8","locale":None,"superuser":"postgres"}) #for ubuntu
        #self.postgres.addDBcluster(clusterName="default",dir="/tmp/testDB",encoding="UTF8",locale=None,username="postgres")
        #self.assertEqual(self.postgres.dbClusters["default"]["dir"],"/tmp/testDB")

    #def test_install(self):
    #    self.manager.dataStore.get("localhost").diagnosis()
    #    self.postgres.install
    
if __name__ == '__main__':
    main()
