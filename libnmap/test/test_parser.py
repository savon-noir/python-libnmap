#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from libnmap.parser import NmapParser, NmapParserException


class TestNmapParser(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [
            {'file': "%s/%s" % (fdir,
                                'files/2_hosts.xml'), 'hosts': 2},
            {'file': "%s/%s" % (fdir,
                                'files/1_hosts.xml'), 'hosts': 1},
            {'file': "%s/%s" % (fdir,
                                'files/1_hosts_banner_ports_notsyn.xml'),
             'hosts': 1},
            # {'file': "%s/%s" % (fdir,
            #                      'files/1_hosts_banner_ports_xmas.xml'),
            #                      'hosts': 1},
            {'file': "%s/%s" % (fdir,
                                'files/1_hosts_banner_ports.xml'), 'hosts': 1},
            {'file': "%s/%s" % (fdir,
                                'files/1_hosts_banner.xml'), 'hosts': 1},
            {'file': "%s/%s" % (fdir,
                                'files/2_hosts_version.xml'), 'hosts': 2},
            # {'file': "%s/%s" % (fdir,
            #                      'files/2_null_hosts.xml'), 'hosts': 2},
            {'file': "%s/%s" % (fdir,
                                'files/2_tcp_hosts.xml'), 'hosts': 2},
            {'file': "%s/%s" % (fdir,
                                'files/1_hosts_nohostname.xml'), 'hosts': 1},
        ]
        self.flist = self.flist_full

        self.ports_string = """<ports><extraports state="closed" count="996">
        <extrareasons reason="resets" count="996"/>
        </extraports>
        <port protocol="tcp" portid="22">
            <state state="open" reason="syn-ack" reason_ttl="53"/>
            <service name="ssh" method="table" conf="3"/>
        </port>
        <port protocol="tcp" portid="25">
            <state state="filtered" reason="admin-prohibited" \
                    reason_ttl="253" reason_ip="109.133.192.1"/>
        <service name="smtp" method="table" conf="3"/>
        </port>
        <port protocol="tcp" portid="80">
            <state state="open" reason="syn-ack" reason_ttl="51"/>
            <service name="http" method="table" conf="3"/>
        </port>
        <port protocol="tcp" portid="9929">
            <state state="open" reason="syn-ack" reason_ttl="53"/>
            <service name="nping-echo" method="table" conf="3"/>
        </port>
        </ports>"""

        self.ports_string2 = """<ports><extraports state="closed" count="996">
        <extrareasons reason="resets" count="996"/>
        </extraports>
        <port protocol="tcp" portid="A2">
            <state state="open" reason="syn-ack" reason_ttl="53"/>
            <service name="ssh" method="table" conf="3"/>
        </port>
        <port protocol="tcp" portid="25">
            <state state="filtered" reason="admin-prohibited" \
                    reason_ttl="253" reason_ip="109.133.192.1"/>
            <service name="smtp" method="table" conf="3"/>
        </port>
        <port protocol="tcp" portid="80">
            <state state="open" reason="syn-ack" reason_ttl="51"/>i
            <service name="http" method="table" conf="3"/></port>
        <port protocol="tcp" portid="9929">
            <state state="open" reason="syn-ack" reason_ttl="53"/>
            <service name="nping-echo" method="table" conf="3"/>
        </port>
        </ports>"""

        self.port_string = """
        <port protocol="tcp" portid="25">
        <state state="filtered" reason="admin-prohibited"
                reason_ttl="253" reason_ip="109.133.192.1"/>
        <service name="smtp" method="table" conf="3"/>
        </port>"""

        self.port_string2 = """
        <port protocol="tcp" portid="">
            <state state="filtered" reason="admin-prohibited"
                    reason_ttl="253" reason_ip="109.133.192.1"/>
            <service name="smtp" method="table" conf="3"/>
        </port>"""

        self.port_string3 = '<port></port>'
        self.port_string4 = ''
        self.port_string5 = 'GINGERBREADMAN'
        self.port_string6 = """
        <port protocol="tcp" portid="FOOL">
        <state state="filtered" reason="admin-prohibited"
                reason_ttl="253" reason_ip="109.133.192.1"/>
        <service name="smtp" method="table" conf="3"/>
        </port>"""

        self.port_string7 = """
        <port protocol="tcp" portid="22">
        <stAAte state="filtered" reason="admin-prohibited"
                reason_ttl="253" reason_ip="109.133.192.1"/>
        <service name="smtp" method="table" conf="3"/></port>"""

        self.port_string8 = """
        <port protocol="tcp" portid="22">
        <service name="smtp" method="table" conf="3"/>
        </port>"""
        self.port_string9 = """
        <port protocol="tcp" portid="22">
        <state/>
        <service name="smtp" method="table" conf="3"/>
        </port>"""

    def test_class_parser(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()
            NmapParser.parse(s)

    def test_class_ports_parser(self):
        pdict = NmapParser.parse(self.ports_string)
        plist = pdict['ports']
        self.assertEqual(len(plist), 4)
        self.assertEqual(sorted([p.port for p in plist]),
                         sorted([22, 25, 9929, 80]))
        self.assertRaises(ValueError,
                              NmapParser.parse,
                              self.ports_string2)

    def test_class_port_parser(self):
            p = NmapParser.parse(self.port_string)
            self.assertEqual(p.port, 25)
            self.assertNotEqual(p.state, "open")
            self.assertEqual(p.state, "filtered")
            self.assertEqual(p.service, "smtp")
            self.assertEqual(p.reason, "admin-prohibited")
            self.assertEqual(p.reason_ttl, "253")
            self.assertEqual(p.reason_ip, "109.133.192.1")

    def test_port_except(self):
        self.assertRaises(ValueError,
                          NmapParser.parse,
                          self.port_string2)
        self.assertRaises(NmapParserException,
                          NmapParser.parse,
                          self.port_string3)
        self.assertRaises(NmapParserException,
                          NmapParser.parse,
                          self.port_string4)
        self.assertRaises(NmapParserException,
                          NmapParser.parse,
                          self.port_string5)
        self.assertRaises(ValueError,
                          NmapParser.parse,
                          self.port_string6)
        self.assertRaises(NmapParserException,
                          NmapParser.parse,
                          self.port_string7)
        self.assertRaises(NmapParserException,
                          NmapParser.parse,
                          self.port_string8)
        serv = NmapParser.parse(self.port_string9)
        self.assertEqual(serv.state, None)

    def test_parser_generic(self):
        plist = NmapParser.parse_fromstring(self.ports_string)
        for p in plist:
            print(p)

if __name__ == '__main__':
    test_suite = ['test_class_parser', 'test_class_ports_parser',
                  'test_class_port_parser', 'test_port_except',
                  'test_parser_generic']
    suite = unittest.TestSuite(map(TestNmapParser, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
