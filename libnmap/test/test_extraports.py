#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from libnmap.parser import NmapParser, NmapParserException


class TestExtraPorts(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        _extrareason = [{'reason': 'filtered', 'count': '3'}, {'reason': 'resets', 'count': '7'}]
        self.flist = [
            {"path": "%s/%s" % (fdir, "files/extra_ports.xml"), "extrareason": _extrareason}
        ]

    def test_extraports(self):
        for fentry in self.flist:
            rep1 = NmapParser.parse_fromfile(fentry["path"])
            ep_list = rep1.hosts[0].extraports
            self.assertEqual(len(ep_list), 2)
            self.assertEqual(ep_list[0].extra_count, 65509)
            self.assertEqual(ep_list[0].extra_state, 'closed')
            self.assertEqual(len(ep_list[0].extra_reasons), 1)
            self.assertEqual(ep_list[1].extra_count, 10)
            self.assertEqual(len(ep_list[1].extra_reasons), 2)
            self.assertEqual(ep_list[1].extra_reasons, fentry["extrareason"])


if __name__ == "__main__":
    test_suite = [
        "test_extraports",
    ]
    suite = unittest.TestSuite(map(TestExtraPorts, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
