#import subprocess

from ... import interfaces

class Postgresql(interfaces.Package):
    def __init__(self, packageName,server):
        """ Setting default parameters based on ubuntu.
        """
        interfaces.Package.__init__(self, packageName,server)
        
        self.username="postgres"
        self.bin_path=None#"/usr/lib/postgresql/9.1/bin"
        self.dbClusters={}#{"default":{"maindir":"","configdir":"","encoding":"UTF8","locale":None,"superuser":"postgres"}}
        self.version=None
        self.installed=None
        
        self.lowlevel=Lowlevel(self)

    def addDBcluster(self,clusterName,dir,encoding="UTF8",locale=None,username="postgres"):
        """ Creating new DB cluster configure.  This function is not create actual DB cluster.
            When initdb will be run and actual DB cluster will be created.
            
        """
        temp={"dir":dir,"encoding":encoding,"locale":locale,"superuser":username}
        self.dbClusters[clusterName]=temp
    
    def configure(self,version=None):
        if(version!=None):
            self.version=version
            
    def diagnosis(self):
        result={}
        level="NORMAL"

        tempResult=self.os().lowlevel.exec_command(["whereis","psql"])
        if(tempResult["returncode"]==0):
            installed=True
            level,result=self.__diagnosis_installed__(result)
        else:
            installed=False

        if(self.installed==None):
            self.installed=installed

        if(self.installed==installed):
            insLevel="NORMAL"
        else:
            insLevel="ERROR"
            level="ERROR"
        result["installed"]={"level":insLevel,"config":self.installed,"status":installed}
        
        result["level"]=level
        return result

    def __diagnosis_installed__(self,result):
        level="NORMAL"
        version=self.version_check()
        if(self.version==None):
            self.version=version
        elif(self.version!=version):
            level="ERROR"
        result["version"]={"level":level,"config":self.version,"status":version}

        if(self.dbClusters=={}):
            #if(self.os().distribution_name=="CentOS"):
            #    self.dbClusters["default"]={"maindir":None,"configdir":None,"encoding":None,"locale":None,"superuser":"postgres"}
            if(self.os().distribution_name=="Ubuntu"):
                if(version.startswith("9.1")):
                    shortVersion="9.1"
                elif(version.startswith("9.2")):
                    shortVersion="9.2"
                elif(version.startswith("9.3")):
                    shortVersion="9.3"
                self.dbClusters["default"]={"maindir":"/var/lib/postgresql/"+shortVersion+"/main","configdir":"/etc/postgresql/"+shortVersion+"/main","encoding":None,"locale":None,"superuser":"postgres"}

            self.dbClusters["default"]={"maindir":None,"configdir":None,"encoding":None,"locale":None,"superuser":"postgres"}

        return level,result
        
    def version_check(self):
        result=self.os().lowlevel.exec_command(["psql","--version"],raiseOnError=True)
        versionLine=result["stdout"].split("\n")[0]
        version=versionLine.replace("psql (PostgreSQL) ","")
        return version
        #psql (PostgreSQL) 9.1.9

        
    def install(self):
        if(self.os().distribution_name=="CentOS"):
            self.__install_centos__()
        elif(self.os().distribution_name=="Ubuntu"):
            self.__install_ubuntu__()
            #self.dbClusters={}#{"default":{"dir":"","encoding":"UTF8","locale":None,"superuser":"postgres"}}

        #if(self.os()=="Debian"):
        #    return self.__install_debian__()
        #if(self.os()=="Fedora"):
        #    return self.__install_fedora__()
        
    def __install_ubuntu__(self):
        if(self.version==None):
            result=self.os().lowlevel.exec_command(["apt-get", "-y", "install", "postgresql"])
            if(result["returncode"]!=0):
                raise Exception(result)
            return

        verName=None
        if(self.os().distribution_version=="10.04"):
            varName="lucid"
        elif(self.os().distribution_version=="12.04"):
            varName="precise"
        elif(self.os().distribution_version=="12.10"):
            varName="quantal"
            raise Exception("PostgreSQL does not support 12.10")
        elif(self.os().distribution_version=="13.04"):
            varName="raring"
            raise Exception("PostgreSQL does not support 13.04")

        result=self.os().lowlevel.exec_command("echo \"deb http://apt.postgresql.org/pub/repos/apt/ "+varName+"-pgdg main\" > /etc/apt/sources.list.d/pgdg.list",shell=True)
        if(result["returncode"]!=0):
            raise Exception(result)
    
        result=self.os().lowlevel.exec_command("wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -",shell=True)
        if(result["returncode"]!=0):
            raise Exception(result)

        result=self.os().lowlevel.exec_command(["apt-get", "update"])
        if(result["returncode"]!=0):
            raise Exception(result)
    
        result=self.os().lowlevel.exec_command(["apt-get","-y", "install", "postgresql-"+self.version])
        if(result["returncode"]!=0):
            raise Exception(result)


    
    def __install_centos__(self):
        if(self.version==None):
            result=self.os().yum_install("postgresql-server")

        elif(self.version=="9.3"):
            self.__install_centos_93__()
        elif(self.version=="9.2"):
            self.__install_centos_92__()
        elif(self.version=="9.1"):
            self.__install_centos_91__()
        self.__install_centos_post_installation__()
        
    def __install_centos_93__(self):
        tempVersion=self.os().distribution_version.split(".")[0]
        self.os().rpm_i("http://yum.postgresql.org/9.3/redhat/rhel-"+tempVersion+"-"+self.os().hardware_type+"/pgdg-centos93-9.3-1.noarch.rpm")
        result=self.os().yum_install("postgresql93-server")

    def __install_centos_92__(self):
        tempVersion=self.os().distribution_version.split(".")[0]
        self.os().rpm_i("http://yum.postgresql.org/9.2/redhat/rhel-"+tempVersion+"-"+self.os().hardware_type+"/pgdg-centos92-9.2-6.noarch.rpm")
        result=self.os().yum_install("postgresql92-server")

    def __install_centos_91__(self):
        tempVersion=self.os().distribution_version.split(".")[0]
        self.os().rpm_i("http://yum.postgresql.org/9.1/redhat/rhel-"+tempVersion+"-"+self.os().hardware_type+"/pgdg-centos91-9.1-4.noarch.rpm")
        result=self.os().yum_install("postgresql93-server")
        
    def __install_centos_post_installation__(self):
        command=None
        if(self.version==None):
            command="postgresql"
        else:
            command="postgresql-"+self.version
            
        result=self.os().lowlevel.exec_command(["service",command,"initdb"])
        if(result["returncode"]!=0):
            raise Exception(result)
        result=self.os().lowlevel.exec_command(["chkconfig",command,"on"])
        if(result["returncode"]!=0):
            raise Exception(result)
        result=self.os().lowlevel.exec_command(["service",command,"start"])
        if(result["returncode"]!=0):
            raise Exception(result)

    def __install_fedora__(self):
        pass


class Lowlevel(object):
    def __init__(self,postgresql):
        self.postgresql=postgresql
        self.pg_ctl=Pg_ctl(postgresql)

    def initdb(self,dbClusterName):
        """ Creating database cluster by using initdb command.
            -D / --pgdata Set directory of database cluster.
                When the directory already exists, initdb will be failed.
                When -D is not specified and $PGDATA will be used.
            -E / --encoding Set encoding for DB cluster.
                When -E is not specified and encoding wii be decided by OS locale.
            --locale Set locale.
                When --locale is not specified and OS locale will be used.
            --no-locale Disable locale.  Same as "--locale=C"
                It is better to disable locale.
            -U / --username Specify superuser name of the DB cluster.
        """
        #sudo -u postgres 
        dbCluster=self.postgresql.dbClusters[dbClusterName]
        command=["sudo","-u",self.postgresql.username]
        command.append(self.postgresql.bin_path+"/initdb")
        if(dbCluster["dir"]!=""):
            command.append("-D")
            command.append(dbCluster["dir"])
        if(dbCluster["encoding"]!=""):
            command.append("-E")
            command.append(dbCluster["encoding"])            
        if(dbCluster["locale"]==None):
            command.append("--no-locale")
        else:
            command.append("--locale="+dbCluster["locale"])
        if(dbCluster["superuser"]!=""):
            command.append("-U")
            command.append(dbCluster["superuser"])
       
        return self.postgresql.os().lowlevel.exec_command(command)

    def pg_dumpall(self,filename,cluster="default",withClean=False,withColumnInsert=False,withCompress=False):
        """
        withClean : Output SQL includes drop commands for existing databases.
        withColumnInsert : Output SQL uses insert instead of copy.
        withCompress : Outpu SQL is compressed by gzip
        
        if filename inclueds "%num%", it will be changed as YYYYMMDD_number
        """
        if(cluster!="default"):
            raise Exception("None default cluster backup by pg_dumpall is not implemented now.")
        #dbCluster=self.postgresql.dbClusters[cluster]
        
        if(filename.find("%num%")!=-1):
            import datetime
            ymd=datetime.date.today().strftime("%Y%m%d")
            num=1
            tempfilename=filename.replace("%num%",ymd+"_"+str(num))
            import os
            while(os.path.exists(tempfilename)):
                num=num+1
                tempfilename=filename.replace("%num%",ymd+"_"+str(num))
            filename=tempfilename
        
        #command=["sudo","-u",self.postgresql.username,"pg_dumpall","--file="+filename,"-w"]
        commandTemp="pg_dumpall -w"
        if(withClean):
            commandTemp=commandTemp+" -c" 
        if(withColumnInsert):
            commandTemp=commandTemp+" --column-inserts"
        
        commandTemp=commandTemp+" > /tmp/backup.sql"
        
        command=[commandTemp]
        
        if(withCompress):
            command.append("gzip -c > /tmp/backup.sql.gz")
            command.append("mv /tmp/backup.sql.gz "+filename)
        else:
            command.append("mv /tmp/backup.sql "+filename)
        command.append("rm -f /tmp/backup.sql")
        #result=self.postgresql.os().lowlevel.exec_command(command,shell=True,raiseOnError=True)
        result=self.postgresql.os().lowlevel.exec_script(command,runuser=self.postgresql.username,raiseOnError=True)
        return result
    
    def psql_restore(self,filename,cluster="default",withCompress=False):
        if(cluster!="default"):
            raise Exception("None default cluster backup by pg_dumpall is not implemented now.")

        command="sudo -u "+self.postgresql.username +" sh -c \" cat "+filename+" | "
        if(withCompress):
            command=command+" gunzip | "
        command=command+"psql postgres \" "

        result=self.postgresql.os().lowlevel.exec_command(command,shell=True,raiseOnError=True)
        return result
    
    #(cluster="default",filename="/tmp/backup.sql")

class Pg_ctl(object):
    def __init__(self,postgresql):
        self.postgresql=postgresql

    def initdb(self,dbClusterName):
        """ Creating database cluster by using pg_ctl initdb command.
            -D / --pgdata Set directory of database cluster.
                When the directory already exists, initdb will be failed.
                When -D is not specified and $PGDATA will be used.
            -o Options for initdb
        """
        #sudo -u postgres 
        dbCluster=self.postgresql.dbClusters[dbClusterName]
        command=["sudo","-u",self.postgresql.username]
        command.append(self.postgresql.bin_path+"/pg_ctl")
        command.append("initdb") # "init" is also good
        if(dbCluster["dir"]!=""):
            command.append("-D")
            command.append(dbCluster["dir"])
        
        options=""
        if(dbCluster["encoding"]!=""):
            options=" -E "+dbCluster["encoding"]            
        if(dbCluster["locale"]==None):
            options=options+" --no-locale"
        else:
            options=options+" --locale="+dbCluster["locale"]
        if(dbCluster["superuser"]!=""):
            options=options+" -U "+dbCluster["superuser"]
        command.append("-o")
        command.append(options)
       
        return self.postgresql.os().lowlevel.exec_command(command)


