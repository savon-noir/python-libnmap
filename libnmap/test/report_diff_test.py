#!/usr/bin/env python

import unittest
import os, sys

from libnmap import NmapParser, NmapParserException, NmapReport

class TestNmapReportDiff(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [{'file': "%s/%s" % (fdir, 'files/2_hosts.xml'), 'hosts': 2}, {'file': "%s/%s" % (fdir,'files/1_hosts.xml'), 'hosts': 1},]
        self.flist = self.flist_full

    def test_diff_host_list(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        d1 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/1_hosts.xml'))
        d2 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/2_hosts.xml'))
        d3 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/2_hosts_achange.xml'))

        r1 = NmapReport("r1", d1)
        r2 = NmapReport("r2", d2)
        r3 = NmapReport("r3", d1)
        r4 = NmapReport("r4", d3)

        d1 = r1.diff(r2)
        self.assertEqual(d1.changed(), set(['hosts_total', 'hosts_up']))
        self.assertEqual(d1.unchanged(), set(['hosts_down', 'NmapHost.127.0.0.1']))
        self.assertEqual(d1.removed(), set(['NmapHost.74.207.244.221']))

        d2 = r1.diff(r3)
        self.assertEqual(d2.changed(), set([]))
        self.assertEqual(d2.unchanged(), set(['hosts_total', 'hosts_down', 'hosts_up', 'NmapHost.127.0.0.1']))
        self.assertEqual(d2.added(), set([]))
        self.assertEqual(d2.removed(), set([]))

        d3 = r2.diff(r4)
        self.assertEqual(d3.changed(), set(['NmapHost.127.0.0.1']))
        self.assertEqual(d3.unchanged(), set(['hosts_total', 'NmapHost.74.207.244.221', 'hosts_up', 'hosts_down']))
        self.assertEqual(d3.added(), set([]))
        self.assertEqual(d3.removed(), set([]))

if __name__ == '__main__':
    test_suite = [ 'test_diff_host_list' ]
    suite = unittest.TestSuite(map(TestNmapReportDiff, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite) ## for more verbosity uncomment this line and comment next line
