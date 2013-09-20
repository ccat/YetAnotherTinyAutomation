# coding:utf-8

import datetime
import manager

class DataStore(object):
    def __init__(self):
        self.store={}

    def set(self,obj):
        self.store[obj.hostname]=obj

    def get(self,name):
        if(name not in self.store):
            return None
        return self.store[name]

    def createServer(self,hostname,mainIPaddr):
        server=Server(hostname,mainIPaddr)
        self.set(server)
        return server

class Server(object):
    """ 設定や作業を行うマシンに対するオブジェクト
    """
    #def __init__(self,settings,hostname,mainIPaddr):
    def __init__(self,hostname,mainIPaddr):
        #self.settings=settings
        self.hostname=hostname
        self.mainIPaddr=mainIPaddr
        self.packages={}
        temp=manager.Manager.settings.packages.basics.OS("OS",self)
        #self.packages["OS"]=temp

    def setPackage(self,name,obj):
        self.packages[name]=obj
        
    def diagnosis(self):
        for key,item in self.packages.items():
            item.resetDiagnosisFlag()

        result={}
        result["OS"]=self.packages["OS"].startDiagnosis()
        for key,item in self.packages.items():
            tempR=item.startDiagnosis()
            if(tempR!=None):
                result[key]=tempR
                
        return result

    """
    def createPackage(self,name):
        dP=settings.dataStore.createPackage(name)
        self.packages[name]=dP
        return dP
    """

class Package(object):

    def __init__(self,packageName,server):
        #self.status={}
        self.configs={}
        self.server=server
        self.diagnosisFlag=False
        server.setPackage(packageName,self)

    def setConfig(self,name,value):
        self.configs[name]=value

    def getConfig(self,name):
        return self.configs[name]

    def package(self,name):
        return self.server.packages[name]

    def os(self):
        return self.server.packages["OS"]
    
    def resetDiagnosisFlag(self):
        self.diagnosisFlag=False
        
    def startDiagnosis(self):
        if(self.diagnosisFlag==True):
            return
        self.diagnosisFlag=True
        return self.diagnosis()
        
    def diagnosis(self):
        pass
    