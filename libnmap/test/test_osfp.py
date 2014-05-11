#!/usr/bin/env python

import unittest
from libnmap.parser import NmapParser

class TestNmapService(unittest.TestCase):
#    def setUp(self):
    def test_osmatch(self):
        myservice = NmapParser.parse_fromfile(osmatch_v2)
        myosmatch = myservice.os.osmatch[0]
        self.assetEqual(osmatch.accuracy, 100)
        sname = "Microsoft Windows 7 SP0 - SP1, Windows Server 2008 SP1, or Windows 8"
        self.assetEqual(myosmatch.name, sname)
        self.assetEqual(myosmatch.line, 53077)
        osclass_dict = {
                'type': 'general purpose'
                'vendor': 'Microsoft',
                'osfamily': 'Windows',
                'osgen': '7',
                'accuracy': '100'
        }
        self.assetEqual(myosmatch.osclasses, [osclass_dict])
        self.assertRaises(NmapParserException, NmapParser.parse, osmatch_buggy1)
