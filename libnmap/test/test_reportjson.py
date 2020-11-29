#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import unittest

from libnmap.parser import NmapParser
from libnmap.reportjson import ReportDecoder, ReportEncoder


class TestReportJson(unittest.TestCase):
    def setUp(self):
        self.fdir = os.path.dirname(os.path.realpath(__file__))
        self.xml_ref_file = "{0}/files/2_hosts.xml".format(self.fdir)
        self.json_ref_file = "{0}/files/2_hosts.json".format(self.fdir)

    def test_reportencode(self):
        nmap_report_obj = NmapParser.parse_fromfile(self.xml_ref_file)
        nmap_report_json = json.loads(
            json.dumps(nmap_report_obj, cls=ReportEncoder)
        )
        with open(self.json_ref_file, "r") as fd:
            nmap_report_json_ref = json.load(fd)
            self.assertEqual(nmap_report_json_ref, nmap_report_json)

    def test_reportdecode(self):
        nmap_report_obj_ref = NmapParser.parse_fromfile(self.xml_ref_file)

        with open(self.json_ref_file, "r") as fd:
            nmap_report_json_ref = json.dumps(json.load(fd))
            nmap_report_obj = json.loads(
                nmap_report_json_ref, cls=ReportDecoder
            )
            self.assertEqual(nmap_report_obj_ref, nmap_report_obj)


if __name__ == "__main__":
    test_suite = ["test_reportencode", "test_reportdecode"]
    suite = unittest.TestSuite(map(TestReportJson, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
