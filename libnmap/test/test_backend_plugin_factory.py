#!/usr/bin/env python

import unittest
import os
from libnmap.parser import NmapParser
from libnmap.plugins.backendplugin import NmapBackendPlugin
from libnmap.plugins.backendpluginFactory import BackendPluginFactory

#define all plugin that need test
from libnmap.plugins.mongodb import NmapMongoPlugin
from libnmap.plugins.sqlite import NmapSqlitePlugin


class TestNmapBackendPlugin(unittest.TestCase):
    """
    This testing class will create a testsuite for each plugins
    The following test need to be done :
       - test the factory
       - test all the method of the class NmapBackendPlugin:
          - Verify implmented/notImplemented
          - Verify the behaviour (ie insert must insert)
    Sample of code to implement for a new plugin:

     def %plugintest_factory(self):
        pass

    def %plugintest_insert(self):
        pass

    def %plugintest_update(self):
        pass

    def %plugintest_delete(self):
        pass

    def %plugintest_get(self):
        pass

    def %plugintest_getall(self):
        pass

    def %plugintest_find(self):
        pass
    """
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [{'file': "%s/%s" % (fdir, 'files/2_hosts.xml'),
                            'hosts': 2},
                           {'file': "%s/%s" % (fdir, 'files/1_hosts.xml'),
                            'hosts': 1},
                           {'file': "%s/%s" % (fdir,
                                    'files/1_hosts_banner_ports_notsyn.xml'),
                            'hosts': 1},
                           {'file': "%s/%s" % (fdir,
                                    'files/1_hosts_banner_ports.xml'),
                            'hosts': 1},
                           {'file': "%s/%s" % (fdir,
                                    'files/1_hosts_banner.xml'),
                            'hosts': 1},
                           {'file': "%s/%s" % (fdir,
                                               'files/2_hosts_version.xml'),
                            'hosts': 2},
                           {'file': "%s/%s" % (fdir,
                                               'files/2_tcp_hosts.xml'),
                            'hosts': 2},
                           {'file': "%s/%s" % (fdir,
                                               'files/1_hosts_nohostname.xml'),
                            'hosts': 1}]
        self.flist = self.flist_full

    def mongo_test_factory(self):
        """Invoke factory and test that the object is of the right classes"""
        #create the backend factory object
        factory = BackendPluginFactory()
        mongodb = factory.create(plugin_name="mongodb")
        self.assertEqual(isinstance(mongodb, NmapBackendPlugin), True)
        self.assertEqual(isinstance(mongodb, NmapMongoPlugin), True)
        self.assertEqual(isinstance(mongodb, NmapSqlitePlugin), False)

    def mongo_test_insert(self):
        """"best way to insert is to call save() of nmapreport"""
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()

            nr = NmapParser.parse(s)
            #create the backend factory object
            factory = BackendPluginFactory()
            mongodb = factory.create(plugin_name="mongodb")
            self.assertNotEqual(nr.save(mongodb),None)

    def mongo_test_update(self):
        pass

    def mongo_test_delete(self):
        pass

    def mongo_test_get(self):
        pass

    def mongo_test_getall(self):
        pass

    def mongo_test_find(self):
        pass

if __name__ == '__main__':
    template_test_suite = ['test_factory',
                           'test_insert',
                           'test_update',
                           'test_delete',
                           'test_get',
                           'test_getall',
                           'test_find']

    test_suite = ['mongo_test_factory', 'mongo_test_insert']
    suite = unittest.TestSuite(map(TestNmapBackendPlugin, test_suite))
    test_result = unittest.TextTestRunner(verbosity=5).run(suite)
