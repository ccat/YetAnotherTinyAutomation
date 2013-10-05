

import sys
sys.path.append("../")

import settings
from modules  import manager

def main():
    """
    python postgresql_backup.py filepath <from gmail address> <to address> <gmail username> <gmail application password>
    """
    
    manage=manager.init(settings=settings)
    postgresql=settings.Postgresql("postgresql",manage.dataStore.get("localhost"))

    argvs = sys.argv
    filepath=argvs[1]
    if(len(argvs)==6):
        fromAddr=argvs[2]
        toAddr=argvs[3]
        username=argvs[4]
        password=argvs[5]
    else:
        fromAddr=None
    
    print "Running diagnosis"
    result=manage.dataStore.get("localhost").diagnosis()
    print "Running pg_backupall"
    print postgresql.lowlevel.pg_dumpall(filename=filepath,withCompress=True)

    if(fromAddr!=None):
        import datetime
        ymd=datetime.date.today().strftime("%Y%m%d")
        print "Sending mail"
        mailer=settings.mailer.Mailer("mailer",self.manager.dataStore.get("localhost"),fromAddr)
        mailer.sendByGmail(toAddr,username,password,"PostgreSQL Backup data "+ymd,"This is Backup data of PostgreSQL at "+ymd,attachFilenames=[filepath])
    
if __name__ == '__main__':
    main()
