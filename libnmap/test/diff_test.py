#!/usr/bin/env python

import unittest
import os, sys

from libnmap import NmapParser, NmapParserException, NmapReport

class TestNmapParser(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [{'file': "%s/%s" % (fdir, 'files/2_hosts.xml'), 'hosts': 2}, {'file': "%s/%s" % (fdir,'files/1_hosts.xml'), 'hosts': 1},]
        self.flist = self.flist_full

    def test_diff_host_list(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        d1 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/1_hosts.xml'))
        d2 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/2_hosts.xml'))

        r1 = NmapReport("r1", d1)
        r2 = NmapReport("r2", d2)
        r3 = NmapReport("r3", d1)

        d = r1.diff(r2)
        print "changed: %s" % (d.changed())
        print "unchanged: %s" % (d.unchanged())
        print "added: %s" % (d.added())
	print "removed: %s" % (d.removed())
        print "___________________________________"
        d = r1.diff(r3)
        print "changed: %s" % (d.changed())
        print "unchanged: %s" % (d.unchanged())
        print "added: %s" % (d.added())
	print "removed: %s" % (d.removed())
             
if __name__ == '__main__':
    test_suite = [ 'test_diff_host_list' ]
    suite = unittest.TestSuite(map(TestNmapParser, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite) ## for more verbosity uncomment this line and comment next line
