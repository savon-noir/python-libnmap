#!/usr/bin/env python

import unittest
import os, sys

sys.path.append("".join([os.path.dirname(__file__), "/../"]))
from nmapreport import NmapReport

class TestNmapReport(unittest.TestCase):
    def setUp(self):
        self.flist_full = [{'file': 'tests/2_hosts.xml', 'hosts': 2}, {'file': 'tests/1_hosts.xml', 'hosts': 1},
                   {'file': 'tests/1_hosts_banner_ports_notsyn.xml', 'hosts': 1},
                  # {'file': 'tests/1_hosts_banner_ports_xmas.xml', 'hosts': 1},
                   {'file': 'tests/1_hosts_banner_ports.xml', 'hosts': 1},
                   {'file': 'tests/1_hosts_banner.xml', 'hosts': 1},
                   {'file': 'tests/2_hosts_version.xml', 'hosts': 2},
                  # {'file': 'tests/2_null_hosts.xml', 'hosts': 2},
                   {'file': 'tests/2_tcp_hosts.xml', 'hosts': 2},
                   {'file': 'tests/1_hosts_nohostname.xml', 'hosts': 1},
        ]
        self.flist_one = [{'file': 'tests/2_hosts.xml', 'hosts': 2}]
        self.flist_two = [{'file': 'tests/1_hosts_nohostname.xml', 'hosts': 1}]

        self.hlist = [ {'hostname': 'localhost', 'ports': 5, 'open': 5}, 
                          {'hostname': 'localhost2', 'ports': 4, 'open': 2},
                          {'hostname': 'scanme.nmap.org', 'ports': 4, 'open': 3},
                          {'hostname': '1.1.1.1', 'ports': 2, 'open': 0},
        ]

        self.flist = self.flist_full

    def test_get_hosts(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            nr = NmapReport(fd.read())
            fd.close()

            nr.parse()
            self.assertEqual(len(nr.get_hosts()), testfile['hosts'])


    def test_get_ports(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            nr = NmapReport(fd.read())
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

if __name__ == '__main__':
    test_suite = ['test_get_hosts' , 'test_get_ports']
#    io_file = StringIO()
    suite = unittest.TestSuite(map(TestNmapReport, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite) ## for more verbosity uncomment this line and comment next line
#    test_result = unittest.TextTestRunner(stream=io_file).run(suite)
#    if len(test_result.failures) or len(test_result.errors):
#  # uncomment for debugging info
#        print_errs = raw_input("Errors detected. Do you want to print the errors (y/N)?")
#        if print_errs == "y":
#            print io_file.getvalue()
#    io_file.close()
