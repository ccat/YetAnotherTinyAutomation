# coding:utf-8

from .. import interfaces

class OS(interfaces.Package):
    def __init__(self,packageName,server):
        interfaces.Package.__init__(self,packageName, server)
        self.lowlevel=OS_lowlevel(self)
        self.distribution_name=None
        self.distribution_version=None
        self.kernel_version=None
        self.hardware_type=None

    def diagnosis(self):
        result={}
        level=0
        tempR=self.lowlevel.exec_command("hostname")
        if(tempR["returncode"]!=0):
            result["hostname"]={"level":"ERROR","config":None,"status":None}
            level=1
        else:
            result["hostname"]={"level":"NORMAL","config":None,"status":tempR["stdout"].rstrip("\n")}
            
        tempL,tempR=self.__diagnosis_dist_check__()
        level=level+tempL
        result["distribution_name"]=tempR["distribution_name"]
        result["distribution_version"]=tempR["distribution_version"]
        
        tempR=self.__diagnosis_hardware_type_check__()
        result["hardware_type"]={"level":"NORMAL","config":None,"status":tempR}

        if(level==0):
            level="NORMAL"
        elif(level>0):
            level="ERROR"
        else:
            level="UNKNOWN"
        result["level"]=level
        return result

    def getDistributionName(self):
        """ Return CentOS/Ubuntu/Redhat/Fedora/Debian
        """
        if(self.distribution_name!=None):
            return self.distribution_name
        raise Exception("No distribution name. NEED TO RUN DIAGNOSIS")

    def __diagnosis_hardware_type_check__(self):
        #CentOS "CentOS release 6.4 (Final)
        result=self.lowlevel.exec_command("uname -m")
        if(result["returncode"]!=0):
            return None
        tempR=result["stdout"].split("\n")
        self.hardware_type=tempR[0]
        return self.hardware_type

    def __diagnosis_dist_check__(self):
        result={}
        flag=False
        if(self.__diagnosis_dist_check_redhat__()):
            flag=True
        elif(self.__diagnosis_dist_check_fedora__()):
            flag=True
        elif(self.__diagnosis_dist_check_ubuntu__()):
            flag=True
        
        if(flag):
            result["distribution_name"]={"level":"NORMAL","config":None,"status":self.distribution_name}
            result["distribution_version"]={"level":"NORMAL","config":None,"status":self.distribution_version}
            return (0,result)
        else:
            result["distribution_name"]={"level":"ERROR","config":None,"status":None}
            result["distribution_version"]={"level":"ERROR","config":None,"status":None}
            return (1,result)

    def __diagnosis_dist_check_redhat__(self):
        #CentOS "CentOS release 6.4 (Final)
        result=self.lowlevel.exec_command("cat /etc/redhat-release")
        if(result["returncode"]!=0):
            return False
        tempR=result["stdout"].split(" ")
        self.distribution_name=tempR[0]
        self.distribution_version=tempR[2]
        return True

    def __diagnosis_dist_check_fedora__(self):
        #Fedora release 18 (Spherical Cow)
        result=self.lowlevel.exec_command("cat /etc/fedora-release")
        if(result["returncode"]!=0):
            return False
        tempR=result["stdout"].split(" ")
        self.distribution_name=tempR[0]
        self.distribution_version=tempR[2]
        return True

    def __diagnosis_dist_check_ubuntu__(self):
        result=self.lowlevel.exec_command("cat /etc/lsb-release")
        if(result["returncode"]!=0):
            return False
        tempR=result["stdout"].split("\n")
        self.distribution_name=tempR[0].split("=")[1]
        self.distribution_version=tempR[1].split("=")[1]
        return True

    #def distribution_SUSE_check(self):
    #    flag=self.distribution_template("cat /etc/SuSE-release")
    #
    #def distribution_debian_check(self):
    #    SSH.exec_command("cat /etc/debian_version",waitForEnd=False)

    def yum_install(self,commands):
        commandList=["yum", "-y","install" ]
        for item in commands:
            commandList.append(item)
        result=self.lowlevel.exec_command(commandList)
        if(result["returncode"]!=0):
            raise Exception(result)

    def rpm_i(self,url):
        result=self.lowlevel.exec_command(["rpm", "-i", url])
        if(result["returncode"]==1):
            if(result["stderr"].find("already installed")==-1):
                raise Exception(result)
        elif(result["returncode"]!=0):
            raise Exception(result)
        
class OS_lowlevel(object):
    def __init__(self,parent):
        self.parent=parent

    def exec_command(self,command,stdin=None,shell=False):
        if(self.parent.server.mainIPaddr!="127.0.0.1"):
            raise Exception("command can be executed only 127.0.0.1.  ToDo: NEED TO IMPLEMENT")
        if(shell==False and isinstance(command,list)==False):
            import shlex
            command=shlex.split(command)

        import subprocess
        p = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell)

        (stdoutdata, stderrdata) =p.communicate(stdin) 
        result={"returncode":p.returncode,"stdout":stdoutdata,"stderr":stderrdata}
        return result

