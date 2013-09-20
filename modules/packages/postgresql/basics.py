#import subprocess

from ... import interfaces

class Postgresql(interfaces.Package):
    def __init__(self, packageName,server):
        """ Setting default parameters based on ubuntu.
        """
        interfaces.Package.__init__(self, packageName,server)
        
        self.username="postgres"
        self.bin_path=None#"/usr/lib/postgresql/9.1/bin"
        self.dbClusters={}#{"default":{"dir":"","encoding":"UTF8","locale":None,"superuser":"postgres"}}
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
        result=self.os().lowlevel.exec_command(["whereis","psql"])
        if(result["returncode"]==0):
            self.installed=True
        else:
            self.installed=False
        #"cat /etc/passwd | grep postgres"
        
    def install(self):
        if(self.os().distribution_name=="CentOS"):
            self.__install_centos__()
        elif(self.os().distribution_name=="Ubuntu"):
            self.__install_ubuntu__()
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
    
        result=self.os().lowlevel.exec_command(["apt-get", "install", "postgresql-"+self.version])
        if(result["returncode"]!=0):
            raise Exception(result)


    
    def __install_centos__(self):
        if(self.version==None):
            result=self.os().lowlevel.exec_command(["yum", "-y", "install", "postgresql-server"])
            if(result["returncode"]!=0):
                raise Exception(result)
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
        #result=self.os().lowlevel.exec_command(["rpm", "-i", "http://yum.postgresql.org/9.3/redhat/rhel-"+tempVersion+"-"+self.os().hardware_type+"/pgdg-centos93-9.3-1.noarch.rpm"])
        #if(result["returncode"]!=0):
            #raise Exception(result)#already installed
        result=self.os().lowlevel.exec_command(["yum", "-y","install", "postgresql93-server"])
        if(result["returncode"]!=0):
            raise Exception(result)

    def __install_centos_92__(self):
        tempVersion=self.os().distribution_version.split(".")[0]
        self.os().rpm_i("http://yum.postgresql.org/9.3/redhat/rhel-"+tempVersion+"-"+self.os().hardware_type+"/pgdg-centos92-9.2-6.noarch.rpm")
        #result=self.os().lowlevel.exec_command(["rpm", "-i", "http://yum.postgresql.org/9.2/redhat/rhel-"+tempVersion+"-"+self.os().hardware_type+"/pgdg-centos92-9.2-6.noarch.rpm"])
        #if(result["returncode"]!=0):
        #    raise Exception(result)
        result=self.os().lowlevel.exec_command(["yum", "-y","install", "postgresql92-server"])
        if(result["returncode"]!=0):
            raise Exception(result)

    def __install_centos_91__(self):
        tempVersion=self.os().distribution_version.split(".")[0]
        self.os().rpm_i("http://yum.postgresql.org/9.3/redhat/rhel-"+tempVersion+"-"+self.os().hardware_type+"/pgdg-centos91-9.1-4.noarch.rpm")
        #result=self.os().lowlevel.exec_command(["rpm", "-i", "http://yum.postgresql.org/9.1/redhat/rhel-"+tempVersion+"-"+self.os().hardware_type+"/pgdg-centos91-9.1-4.noarch.rpm"])
        #if(result["returncode"]!=0):
        #    raise Exception(result)
        result=self.os().lowlevel.exec_command(["yum", "-y","install", "postgresql91-server"])
        if(result["returncode"]!=0):
            raise Exception(result)
        
    def __install_centos_post_installation__(self):
        command=None
        if(self.version==None):
            command="postgresql"
        else:
            command="postgresql-"+version
            
        result=self.os().lowlevel.exec_command(["service",command,"initdb"])
        if(result["returncode"]!=0):
            raise Exception(result)
        result=self.os().lowlevel.exec_command(["chkconfig",command,"on"])
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


