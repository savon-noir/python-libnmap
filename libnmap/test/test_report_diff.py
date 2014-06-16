#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from libnmap.parser import NmapParser


class TestNmapReportDiff(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [{'file': "%s/%s" % (fdir, 'files/2_hosts.xml'),
                            'hosts': 2},
                           {'file': "%s/%s" % (fdir, 'files/1_hosts.xml'),
                            'hosts': 1}]
        self.flist = self.flist_full

    def test_diff_host_list(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        r1 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/1_hosts.xml'))
        r2 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/2_hosts.xml'))
        r3 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/1_hosts.xml'))
        r4 = NmapParser.parse_fromfile("%s/%s" % (fdir,
                                                  'files/2_hosts_achange.xml'))

        d1 = r1.diff(r2)
        self.assertEqual(d1.changed(), set(['hosts_total', 'commandline',
                                            'hosts_up', 'scan_type',
                                            'elapsed']))
        self.assertEqual(d1.unchanged(), set(['hosts_down', 'version',
                                              'NmapHost::127.0.0.1']))
        self.assertEqual(d1.removed(), set(['NmapHost::74.207.244.221']))

        d2 = r1.diff(r3)
        self.assertEqual(d2.changed(), set([]))
        self.assertEqual(d2.unchanged(), set(['hosts_total',
                                              'commandline',
                                              'hosts_up',
                                              'NmapHost::127.0.0.1',
                                              'elapsed',
                                              'version',
                                              'scan_type',
                                              'hosts_down']))
        self.assertEqual(d2.added(), set([]))
        self.assertEqual(d2.removed(), set([]))

        d3 = r2.diff(r4)
        self.assertEqual(d3.changed(), set(['NmapHost::127.0.0.1']))
        self.assertEqual(d3.unchanged(), set(['hosts_total',
                                              'commandline',
                                              'hosts_up',
                                              'NmapHost::74.207.244.221',
                                              'version',
                                              'elapsed',
                                              'scan_type',
                                              'hosts_down']))
        self.assertEqual(d3.added(), set([]))
        self.assertEqual(d3.removed(), set([]))


if __name__ == '__main__':
    test_suite = ['test_diff_host_list']
    suite = unittest.TestSuite(map(TestNmapReportDiff, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
