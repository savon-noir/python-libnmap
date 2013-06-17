#!/usr/bin/env python

import unittest
import os
from libnmap.parser import NmapParser


class TestNmapFP(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [{ 'file': "%s/%s" % (fdir, 'files/1_os_banner_scripts.xml'), 'os': 1},
                { 'file': "%s/%s" % (fdir, 'files/2_hosts_version.xml'), 'os': 1},
                { 'file': "%s/%s" % (fdir, 'files/1_hosts_banner_ports_notsyn.xml'), 'os': 0},
                { 'file': "%s/%s" % (fdir, 'files/1_hosts_banner.xml'), 'os': 0},
                { 'file': "%s/%s" % (fdir, 'files/1_hosts_down.xml'), 'os': 0}]
        self.flist = self.flist_full

    def test_fp(self):
        for file_e in self.flist_full:
            rep = NmapParser.parse_fromfile(file_e['file'])
            for _host in rep.hosts:
                if file_e['os'] != 0:
                    self.assertTrue(_host.os_fingerprinted)
                elif file_e['os'] == 0:
                    self.assertFalse(_host.os_fingerprinted)
                else:
                    raise Exception

if __name__ == '__main__':
    test_suite = ['test_fp']
    suite = unittest.TestSuite(map(TestNmapFP, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
