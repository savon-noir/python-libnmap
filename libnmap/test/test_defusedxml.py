#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.parser import NmapParser, NmapParserException
import unittest
import os


class TestDefusedXML(unittest.TestCase):
    def setUp(self):
        self.billionlaugh = """<?xml version="1.0"?>
<!DOCTYPE lolz [
<!ENTITY lol "lol">
<!ELEMENT lolz (#PCDATA)>
<!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
<!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
<!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
<!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
<!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
<!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
<!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
<!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
<!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<lolz>&lol9;</lolz>
        """
        self.fdir = os.path.dirname(os.path.realpath(__file__))
        self.billionlaugh_file = "{0}/files/{1}".format(self.fdir, "billion_laugh.xml")
        self.external_entities_file = "{0}/files/{1}".format(self.fdir, "defused_et_local_includer.xml")

    def test_billion_laugh(self):
        self.assertRaisesRegex(NmapParserException, ".*EntitiesForbidden", NmapParser.parse_fromstring, self.billionlaugh)

    def test_external_entities(self):
        self.assertRaisesRegex(NmapParserException, ".*EntitiesForbidden", NmapParser.parse_fromfile, self.external_entities_file)


if __name__ == "__main__":
    #test_suite = ["test_external_entities"]
    test_suite = ["test_billion_laugh", "test_external_entities" ]
    suite = unittest.TestSuite(map(TestDefusedXML, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
