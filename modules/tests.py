# coding:utf-8
import unittest

#import interfaces
import manager
#import diagnosis

#import monitor

import default_settings

class UsageTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_initialize(self):
        self.manager=manager.init(settings=default_settings)
        self.assertTrue(self.manager.dataStore.get("localhost")!=None)
        self.assertTrue(self.manager.dataStore.get("notExist")==None)

    """
    def test_diagnosis(self):
        import manager
        manager.init(settings="./default_settings.py")
        self.assertTrue(manager.dataStore.get("localhost")!=None)
        result=manager.run(target="localhost",command="diagnosis")
        self.assertEqual(result,None)
    """

class InterfaceTest(unittest.TestCase):

    def setUp(self):
        self.manager=manager.init(settings=default_settings)

    def test_dataStore(self):
        """ Test for DataStore interface.
        DataStore stores server data includes time-series data.
        """
        import interfaces
        server=interfaces.Server("localhost","127.0.0.1")
        self.manager.dataStore.set(server)
        self.assertEqual(self.manager.dataStore.get("localhost"),server)
        server2=self.manager.dataStore.createServer("localhost","127.0.0.1")
        self.assertEqual(self.manager.dataStore.get("localhost"),server2)

    def test_server(self):
        import interfaces
        server=interfaces.Server("testServer","127.0.0.1")
        #self.assertEqual(datePackage.resolutions,{})
        result=server.diagnosis()
        print result
        self.assertEqual(result,
                         {"OS":{"level":"NORMAL",
                                "hostname":{"level":"NORMAL","config":None,"status":result["OS"]["hostname"]["status"]},
                                "distribution_name":{"level":"NORMAL","config":None,"status":result["OS"]["distribution_name"]["status"]},
                                "distribution_version":{"level":"NORMAL","config":None,"status":result["OS"]["distribution_version"]["status"]},
                                "hardware_type":{"level":"NORMAL","config":None,"status":result["OS"]["hardware_type"]["status"]},
                               },
                         })

    def test_package(self):
        import interfaces
        server=interfaces.Server("testServer","127.0.0.1")
        package=interfaces.Package("package",server)
        #package.diag
        #self.assertEqual(datePackage.resolutions,{})

    """
    def test_dataPackage(self):
        dataPackage=interfaces.DataPackage("testPack")
        self.assertEqual(dataPackage.name,"testPack")
        dataPackage.setConfig("configName","value")
        self.assertEqual(dataPackage.getConfig("configName"), "value")
        dataPackage.setConfig("configName","value2")
        self.assertEqual(dataPackage.getConfig("configName"), "value2")
        dataPackage.setStatus("valName","value")
        self.assertEqual(dataPackage.getStatus("valName",age="latest")["value"], "value")
        self.assertEqual(dataPackage.getStatus("valName",age=-1)["value"], "value")
        self.assertEqual(dataPackage.ages("valName"),1)

    "" "
        self.assertEqual(dataPackage.diagnosis,"")
        self.assertEqual(dataPackage.conditions,[])
    "" "
        dP=settings.dataStore.createPackage("testPack2")
        self.assertEqual(dP.name,"testPack2")
    """

    """
    def test_notify(self):
        notify=interfaces.Notifier()
        notify.notify("message")
    """



"""
class DiagnosisTest(unittest.TestCase):

    def setUp(self):
        #self.seq = range(10)
        pass

    def test_interfaces(self):
        server=interfaces.Server("localhost","127.0.0.1")
        dataStore=interfaces.DataStore("packageName")
        dataStore.set("valueName","value")
        self.assertEqual(dataStore.get("valueName",age="latest"), "value")
        self.assertEqual(len(dateStore.ages()),1)

    def test_normalUse(self):

        server=interfaces.Server(hostname="testhost")
        command=interfaces.Command(command="nop")
        result=diagnosis.diagnosis(target=server,command=command)

        # make sure the shuffled sequence does not lose any elements
        #self.assertEqual(self.seq, range(10))
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))
        #self.assertTrue(element in self.seq)
"""


if __name__ == '__main__':
    unittest.main()

