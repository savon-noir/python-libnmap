#!/usr/bin/env python

import unittest
import os, sys

#sys.path.append("".join([os.path.dirname(__file__), "/../"]))
from libnmap import NmapParser

class TestNmapParser(unittest.TestCase):
    def setUp(self):
        self.flist_full = [{'file': 'test/2_hosts.xml', 'hosts': 2}, {'file': 'test/1_hosts.xml', 'hosts': 1},
                   {'file': 'test/1_hosts_banner_ports_notsyn.xml', 'hosts': 1},
                  # {'file': 'test/1_hosts_banner_ports_xmas.xml', 'hosts': 1},
                   {'file': 'test/1_hosts_banner_ports.xml', 'hosts': 1},
                   {'file': 'test/1_hosts_banner.xml', 'hosts': 1},
                   {'file': 'test/2_hosts_version.xml', 'hosts': 2},
                  # {'file': 'test/2_null_hosts.xml', 'hosts': 2},
                   {'file': 'test/2_tcp_hosts.xml', 'hosts': 2},
                   {'file': 'test/1_hosts_nohostname.xml', 'hosts': 1},
        ]
        self.flist_one = [{'file': 'test/1_hosts_nohostname.xml', 'hosts': 1}]
        self.flist_two = [{'file': 'test/2_hosts.xml', 'hosts': 2, 
                           'elapsed': '134.36', 'endtime': "1361738040", 
                           'summary': "Nmap done at Sun Feb 24 21:34:00 2013; 2 IP addresses (2 hosts up) scanned in 134.36 seconds"}]

        self.hlist = [ {'hostname': 'localhost', 'ports': 5, 'open': 5}, 
                          {'hostname': 'localhost2', 'ports': 4, 'open': 2},
                          {'hostname': 'scanme.nmap.org', 'ports': 4, 'open': 3},
                          {'hostname': '1.1.1.1', 'ports': 2, 'open': 0},
        ]

        self.flist = self.flist_full

    def test_get_hosts(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            nr = NmapParser(fd.read())
            fd.close()

            nr.parse()
            self.assertEqual(len(nr.get_hosts()), testfile['hosts'])


    def test_get_ports(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            nr = NmapParser(fd.read())
            fd.close()

            nr.parse()
            for h in nr.get_hosts():
                for th in self.hlist:
                    if th['hostname'] == h.get_hostname():
                        self.assertEqual(th['ports'], len(h.get_ports()))
                        self.assertEqual(th['open'], len(h.get_open_ports()))

                for np in h.get_open_ports():
                    sport = h.get_port(np)
                    self.assertEqual(sport['port'], np)

    def test_runstats(self):
        for testfile in self.flist_two:
            fd = open(testfile['file'], 'r')
            nr = NmapParser(fd.read())
            fd.close()

            nr.parse()
            for attr in ('endtime', 'summary', 'elapsed'):
                self.assertEqual(getattr(nr, attr), testfile[attr])

if __name__ == '__main__':
    test_suite = ['test_get_hosts' , 'test_get_ports', 'test_runstats']
#    io_file = StringIO()
    suite = unittest.TestSuite(map(TestNmapParser, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite) ## for more verbosity uncomment this line and comment next line
#    test_result = unittest.TextTestRunner(stream=io_file).run(suite)
#    if len(test_result.failures) or len(test_result.errors):
#  # uncomment for debugging info
#        print_errs = raw_input("Errors detected. Do you want to print the errors (y/N)?")
#        if print_errs == "y":
#            print io_file.getvalue()
#    io_file.close()
