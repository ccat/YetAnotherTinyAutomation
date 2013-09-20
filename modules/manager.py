

import interfaces

#SETTINGS=None

def init(settings):
    #import imp
    #import sys
    #sys.path.append("./")
    #global SETTINGS
    #SETTINGS=imp.load_source("settings",settings)
    temp=Manager(settings)

    if(Manager.dataStore.get("localhost")==None):
        Manager.dataStore.createServer("localhost","127.0.0.1")

    return temp

class Manager(object):
    settings=None
    dataStore=None
    
    def __init__(self,settings):
        Manager.settings=settings
        Manager.dataStore=settings.dataStore


