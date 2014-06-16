#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from libnmap.parser import NmapParser

host1 = """
<host starttime="1361738377" endtime="1361738377">
<status state="up" reason="localhost-response"/>
<address addr="127.0.0.1" addrtype="ipv4"/>
<hostnames>
<hostname name="localhost" type="user"/>
<hostname name="localhost" type="PTR"/>
</hostnames>
<ports><extraports state="WILLY_WONCKA" count="995">
<extrareasons reason="conn-refused" count="995"/>
</extraports>
<port protocol="tcp" portid="22">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="ssh" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="25">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="smtp" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="111">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="rpcbind" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="631">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="ipp" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="3306">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="mysql" method="table" conf="3"/>
</port>
</ports>
<times srtt="2100" rttvar="688" to="100000"/>
</host>
"""
host2 = """
<host starttime="1361738318" endtime="13617386177">
<status state="up" reason="localhost-respoe"/>
<address addr="127.0.0.1" addrtype="ipv4"/>
<hostnames>
<hostname name="localhost" type="user"/>
<hostname name="localhost" type="PTR"/>
<hostname name="localhost2" type="PTR"/>
</hostnames>
<ports><extraports state="closed" count="995">
<extrareasons reason="conn-refused" count="995"/>
</extraports>
<port protocol="tcp" portid="22">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="ssh" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="25">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="smtp" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="111">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="rpcbind" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="631">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="ipp" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="3306">
<state state="open" reason="syn-ack" reason_ttl="1"/>
<service name="mysql" method="table" conf="3"/>
</port>
</ports>
<times srtt="2100" rttvar="688" to="100000"/>
</host>
"""

host3 = """<host starttime="13617" endtime="13617">
<status state="down" reason="localhost-response"/>
<address addr="127.0.0.1" addrtype="ipv4"/>
<hostnames>
<hostname name="localhost" type="user"/>
<hostname name="localhost" type="PTR"/>
</hostnames>
<ports><extraports state="closed" count="995">
<extrareasons reason="conn-refused" count="995"/>
</extraports>
<port protocol="tcp" portid="22">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="ssh" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="111">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="rpcbind" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="631">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="ipp" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="3306">
<state state="closed" reason="syn-ack" reason_ttl="0"/>
<service name="mysql" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="3307">
<state state="closed" reason="syn-ack" reason_ttl="0"/>
<service name="mysql" method="table" conf="3"/>
</port>
</ports>
<times srtt="2100" rttvar="688" to="100000"/>
</host>
"""
host4 = """
<host starttime="77" endtime="13">
<status state="up" reason="locaonse"/>
<address addr="127.0.0.1" addrtype="ipv4"/>
<hostnames>
<hostname name="localhost" type="user"/>
<hostname name="localhost" type="PTR"/>
</hostnames>
<ports><extraports state="azeazeaze" count="995">
<extrareasons reason="conn-refused" count="995"/>
</extraports>
<port protocol="tcp" portid="22">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="ssh" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="25">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="smtp" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="111">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="rpcbind" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="631">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="ipp" method="table" conf="3"/>
</port>
<port protocol="tcp" portid="3306">
<state state="open" reason="syn-ack" reason_ttl="0"/>
<service name="mysql" method="table" conf="3"/>
</port>
</ports>
<times srtt="200" rttvar="68" to="100"/>
</host>
"""


class TestNmapHost(unittest.TestCase):
    def test_eq_host(self):
        h1 = NmapParser.parse(host1)
        h2 = NmapParser.parse(host2)
        h3 = NmapParser.parse(host3)
        h4 = NmapParser.parse(host4)

        self.assertNotEqual(h1, h2)
        self.assertEqual(h1, h1)
        self.assertNotEqual(h1, h3)
        self.assertEqual(h1, h4)
        self.assertNotEqual(h2, h3)

    def test_host_api(self):
        h = NmapParser.parse(host2)
        self.assertEqual(h.starttime, "1361738318")
        self.assertEqual(h.endtime, "13617386177")
        self.assertEqual(h.address, '127.0.0.1')
        self.assertEqual(h.status, "up")
        self.assertEqual(h.hostnames, ['localhost', 'localhost', 'localhost2'])

        h2 = NmapParser.parse(host3)
        self.assertEqual(len(h2.services), 5)
        self.assertEqual(len(h2.get_ports()), 5)
        self.assertEqual(len(h2.get_open_ports()), 3)
        self.assertEqual(h2.get_service(22, "tcp").state, "open")

    def test_extra_ports(self):
        h1 = NmapParser.parse(host1)
        h2 = NmapParser.parse(host2)

        self.assertEqual(h1.extraports_state['state'], {'count': '995', 'state': 'WILLY_WONCKA'})
        self.assertEqual(h1.extraports_reasons, [{'reason': 'conn-refused', 'count': '995'}])

        self.assertEqual(h2.extraports_state['state'], {'count': '995', 'state': 'closed'})
        self.assertEqual(h2.extraports_reasons, [{'reason': 'conn-refused', 'count': '995'}])

    def test_diff_host(self):
        h1 = NmapParser.parse(host1)
        h2 = NmapParser.parse(host2)
        h3 = NmapParser.parse(host3)

        c1 = h1.diff(h2)
        c2 = h1.diff(h3)
        c3 = h2.diff(h3)

        self.assertEqual(c1.changed(), set(['hostnames']))
        self.assertEqual(c1.added(), set([]))
        self.assertEqual(c1.removed(), set([]))

        self.assertEqual(c1.unchanged(), set(['status',
                                              "NmapService::tcp.22",
                                              "NmapService::tcp.111",
                                              "NmapService::tcp.631",
                                              "NmapService::tcp.3306",
                                              'address',
                                              "NmapService::tcp.25"]))

        self.assertEqual(c2.changed(), set(['status',
                                            "NmapService::tcp.3306"]))
        self.assertEqual(c2.added(), set(["NmapService::tcp.25"]))
        self.assertEqual(c2.removed(), set(["NmapService::tcp.3307"]))
        self.assertEqual(c2.unchanged(), set(["NmapService::tcp.631",
                                              'hostnames',
                                              "NmapService::tcp.22",
                                              "NmapService::tcp.111",
                                              'address']))

        self.assertEqual(c3.changed(), set(['status', 'hostnames',
                                            "NmapService::tcp.3306"]))
        self.assertEqual(c3.added(), set(["NmapService::tcp.25"]))
        self.assertEqual(c3.removed(), set(["NmapService::tcp.3307"]))
        self.assertEqual(c3.unchanged(), set(["NmapService::tcp.631",
                                              "NmapService::tcp.22",
                                              "NmapService::tcp.111",
                                              'address']))


if __name__ == '__main__':
    test_suite = ['test_eq_host', 'test_host_api', 'test_diff_host']
    suite = unittest.TestSuite(map(TestNmapHost, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
