#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.parser import NmapParser
from libnmap.reportjson import ReportDecoder, ReportEncoder
import json

nmap_report_obj = NmapParser.parse_fromfile('libnmap/test/files/1_hosts.xml')

# create a json object from an NmapReport instance
nmap_report_json = json.dumps(nmap_report_obj, cls=ReportEncoder)
print(nmap_report_json)
# create a NmapReport instance from a json object
nmap_report_obj = json.loads(nmap_report_json, cls=ReportDecoder)
print(nmap_report_obj)
