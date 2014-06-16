#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from libnmap.parser import NmapParser, NmapParserException

baddatalist = ["<host>aaa", None, '', 123, "ports/>>>", "<port<>",
               "<port/>", "<ports/aaaa>"]


class TestNmapParser(unittest.TestCase):
    def test_parse(self):
        for baddata in baddatalist:
            self.assertRaises(NmapParserException, NmapParser.parse,
                              baddata, "zz")
            self.assertRaises(NmapParserException, NmapParser.parse,
                              baddata, "XML")
            self.assertRaises(NmapParserException, NmapParser.parse,
                              baddata, "YAML")

if __name__ == '__main__':
    test_suite = ['test_parse']

    suite = unittest.TestSuite(map(TestNmapParser, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
