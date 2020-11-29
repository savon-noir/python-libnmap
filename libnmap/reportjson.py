#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from libnmap.objects import NmapHost, NmapReport, NmapService
from libnmap.objects.os import (
    CPE,
    NmapOSClass,
    NmapOSFingerprint,
    NmapOSMatch,
    OSFPPortUsed,
)
from libnmap.parser import NmapParser


class ReportEncoder(json.JSONEncoder):
    """
    ReportEncoder is a internal class used mostly by plugins to convert
    NmapReport objects in json format.
    e.g.:
        nmapreport_obj = NmapParser.parse_fromfile(
            "libnmap/test/files/1_hosts.xml"
        )
        nmapreport_json = json.dumps(nmapreport_obj, cls=ReportEncoder)
    """

    def default(self, obj):
        otype = {
            "NmapHost": NmapHost,
            "NmapOSFingerprint": NmapOSFingerprint,
            "NmapOSMatch": NmapOSMatch,
            "NmapOSClass": NmapOSClass,
            "CPE": CPE,
            "OSFPPortUsed": OSFPPortUsed,
            "NmapService": NmapService,
            "NmapReport": NmapReport,
        }
        if isinstance(obj, tuple(otype.values())):
            key = ("__{0}__").format(obj.__class__.__name__)
            return {key: obj.__dict__}
        return json.JSONEncoder.default(self, obj)


class ReportDecoder(json.JSONDecoder):
    """
    ReportDecoder is a internal class used mostly by plugins to convert
    json nmap report in to NmapReport objects.
    e.g.:
        nmap_report_obj = json.loads(nmap_report_json, cls=ReportDecoder)
    """

    def decode(self, json_str):
        r = NmapParser.parse_fromdict(json.loads(json_str))
        return r
