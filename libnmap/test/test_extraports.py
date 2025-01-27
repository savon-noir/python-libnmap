#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from libnmap.parser import NmapParser, NmapParserException


class TestExtraPorts(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        _extrareasons = [
            {"reason": "filtered", "count": "3"},
            {"reason": "resets", "count": "7"},
        ]
        self.flist = [
            {
                "path": "%s/%s" % (fdir, "files/extra_ports.xml"),
                "extrareasons": _extrareasons,
            }
        ]

    def test_extraports(self):
        for fentry in self.flist:
            rep1 = NmapParser.parse_fromfile(fentry["path"])
            ep_list = rep1.hosts[0].extraports
            self.assertEqual(len(ep_list), 2)
            self.assertEqual(ep_list[0]["count"], "65509")
            self.assertEqual(ep_list[0]["state"], "closed")
            self.assertEqual(len(ep_list[0]["extrareasons"]), 1)
            self.assertEqual(ep_list[1]["count"], "10")
            self.assertEqual(len(ep_list[1]["extrareasons"]), 2)
            self.assertEqual(
                ep_list[1]["extrareasons"], fentry["extrareasons"]
            )


if __name__ == "__main__":
    test_suite = [
        "test_extraports",
    ]
    suite = unittest.TestSuite(map(TestExtraPorts, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
