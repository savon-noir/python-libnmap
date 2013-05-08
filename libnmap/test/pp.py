#!/usr/bin/env python

import unittest
import os
from libnmap.parser import NmapParser, NmapParserException

baddatalist = ["<host>aaa", None, '', 123, "ports/>>>", "<port<>", "<ports/>"]


class TestNmapParser(unittest.TestCase):
    def test_parse(self):
        for baddata in baddatalist:
            print baddata
            try:
                NmapParser.parse(baddata)
            except NmapParserException as e:
                print "{0} ({1})".format(e, baddata)
            self.assertRaises(NmapParserException, NmapParser.parse, baddata, "zz")
            self.assertRaises(NmapParserException, NmapParser.parse, baddata, "XML")

if __name__ == '__main__':
    test_suite = ['test_parse']

    suite = unittest.TestSuite(map(TestNmapParser, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
