#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from libnmap.parser import NmapParser
from libnmap.diff import NmapDiffException

service1 = """
<port protocol="tcp" portid="22">
    <state state="open" reason="syn-ack" reason_ttl="0"/>
    <service name="ssh" method="table" conf="3"/>
</port>
"""

service2 = """
<port protocol="udp" portid="22">
    <state state="open" reason="syn-ack" reason_ttl="0"/>
    <service name="ssh" method="table" conf="3"/>
</port>
"""

service3 = """
<port protocol="udp" portid="53">
    <state state="open" reason="syn-ack" reason_ttl="0"/>
    <service name="ssh" method="table" conf="3"/>
</port>
"""

service4 = """
<port protocol="tcp" portid="22">
    <state state="closed" reason="syn-ack" reason_ttl="0"/>
    <service name="ssh" method="table" conf="3"/>
</port>
"""

service5 = """
<port protocol="tcp" portid="3306">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="mysql" product="MySQL" version="5.1.62"
            method="probed" conf="10"/>
</port>
"""

service6 = """
<port protocol="tcp" portid="3306">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="mysql" product="MySQL"
        version="5.1.61" method="probed" conf="10"/>
</port>
"""

service7 = """
<port protocol="tcp" portid="3306">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="mysql"
        product="MySQL" version="5.1.61" method="probed" conf="10"/>
</port>
"""

port_string = """
<port protocol="tcp" portid="25">
    <state state="filtered" reason="admin-prohibited"
        reason_ttl="253" reason_ip="109.133.192.1"/>
    <service name="smtp" method="table" conf="3"/>
</port>"""

port_string_other2 = """
<port protocol="tcp" portid="25">
    <state state="open" reason="admin-prohibited"
        reason_ttl="253" reason_ip="109.133.192.1"/>
    <service name="smtp" method="table" conf="3"/>
</port>"""

port_string_other3 = """
<port protocol="tcp" portid="22">
    <state state="open" reason="admin-prohibited"
        reason_ttl="253" reason_ip="109.133.192.1"/>
    <service name="ssh" method="table" conf="3"/>
</port>"""

port_string_other4 = """
<port protocol="tcp" portid="22">
    <state state="willy_woncka" reason="admin-prohibited"
        reason_ttl="253" reason_ip="109.133.192.1"/>
    <service name="willywoncka" method="table" conf="3"/>
</port>"""

port_string_other5 = """
<port protocol="tcp" portid="22">
    <state state="willy_woncka" reason="admin-prohibited"
        reason_ttl="253" reason_ip="109.133.192.1"/>
    <service name="ssh" method="table" conf="3"/>
</port>"""

port_string_other6 = """
<port protocol="tcp" portid="25">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="smtp" product="Postfix smtpd"
        hostname=" jambon.localdomain" method="probed" conf="10"/>
</port>"""

port_string_other7 = """
<port protocol="tcp" portid="111">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="rpcbind" method="probed" conf="10"/>
</port>"""

port_string_other8 = """
<port protocol="tcp" portid="631">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="ipp" product="CUPS" version="1.4"
        method="probed" conf="10"/>
</port>"""

port_string_other9 = """
<port protocol="tcp" portid="631">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="ipp" product="COPS" version="1.4"
        method="probed" conf="10"/>
</port>"""

port_string_other10 = """
<port protocol="tcp" portid="25">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="smtp" product="Postfix smtpd"
        hostname=" jambon.localdomain" method="probed" conf="10"/>
</port>"""

port_string_other11 = """
<port protocol="tcp" portid="25">
    <state state="open" reason="syn-ack" reason_ttl="69"/>
    <service name="smtp" product="Postfix smtpd"
        hostname=" jambon.localdomain" method="probed" conf="10"/>
</port>"""

port_string_other12 = """
<port protocol="tcp" portid="25">
    <state state="filtered" reason="admin-prohibited"
        reason_ttl="253" reason_ip="109.133.192.1"/>
    <service name="smtp" method="table" conf="3"/>
</port>"""

port_string_other13 = """
<port protocol="tcp" portid="25">
    <state state="filtered" reason="patin"
        reason_ttl="253" reason_ip="109.133.192.1"/>
    <service name="smtp" method="table" conf="3"/>
</port>"""

port_noservice = """
<port protocol="udp" portid="3306">
<state state="closed" reason="port-unreach" reason_ttl="64" />
</port>"""

port_owner = """
<port protocol="tcp" portid="25">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="smtp" product="Postfix smtpd"
        hostname=" jambon.localdomain" method="probed" conf="10"/>
    <owner name="edwige"/>
</port>"""

port_tunnel = """
<port protocol="tcp" portid="443">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="https" method="probed" tunnel="ssl" conf="10"/>
</port>"""

class TestNmapService(unittest.TestCase):
    def setUp(self):
        self.s1 = NmapParser.parse(service1)
        self.s2 = NmapParser.parse(service2)
        self.s3 = NmapParser.parse(service3)
        self.s4 = NmapParser.parse(service4)
        self.s5 = NmapParser.parse(service5)
        self.s6 = NmapParser.parse(service6)
        self.s7 = NmapParser.parse(service7)

    def test_port_state_changed(self):
        nservice1 = NmapParser.parse(port_string)
        nservice2 = NmapParser.parse(port_string_other2)
        nservice3 = NmapParser.parse(port_string_other3)
        nservice4 = NmapParser.parse(port_string_other4)

        self.assertEqual(nservice1.diff(nservice2).changed(), set(['state']))
        self.assertRaises(NmapDiffException, nservice1.diff, nservice3)
        self.assertRaises(NmapDiffException, nservice1.diff, nservice4)
#
        self.assertRaises(NmapDiffException, nservice2.diff, nservice3)
        self.assertEqual(nservice3.diff(nservice4).changed(),
                         set(['state', 'service']))

    def test_port_state_unchanged(self):
        nservice1 = NmapParser.parse(port_string)
        nservice2 = NmapParser.parse(port_string_other2)
        #nservice3 = NmapParser.parse(port_string_other3)
        #nservice4 = NmapParser.parse(port_string_other4)

        self.assertEqual(nservice1.diff(nservice2).unchanged(),
                         set(['banner', 'protocol', 'port', 'service', 'id', 'reason']))

    def test_port_service_changed(self):
        nservice1 = NmapParser.parse(port_string)
        nservice2 = NmapParser.parse(port_string_other2)
        nservice4 = NmapParser.parse(port_string_other4)
        nservice5 = NmapParser.parse(port_string_other5)
        nservice8 = NmapParser.parse(port_string_other8)
        nservice9 = NmapParser.parse(port_string_other9)

        self.assertEqual(nservice1.diff(nservice2).changed(),
                         set(['state']))
        self.assertEqual(nservice5.diff(nservice4).changed(),
                         set(['service']))
        # banner changed
        self.assertEqual(nservice8.diff(nservice9).changed(),
                         set(['banner']))

    def test_eq_service(self):
        self.assertNotEqual(NmapDiffException, self.s1, self.s2)
        self.assertNotEqual(self.s1, self.s3)
        self.assertNotEqual(self.s1, self.s4)

        self.assertNotEqual(self.s5, self.s6)
        self.assertEqual(self.s6, self.s7)

    def test_diff_service(self):
        self.assertRaises(NmapDiffException, self.s1.diff, self.s2)
        self.assertRaises(NmapDiffException, self.s1.diff, self.s3)
        self.assertEqual(self.s1.diff(self.s4).changed(), set(['state']))
        self.assertEqual(self.s1.diff(self.s4).unchanged(),
                         set(['banner', 'protocol', 'port', 'service',
                              'id', 'reason']))

        self.assertEqual(self.s5.diff(self.s6).changed(), set(['banner']))
        self.assertEqual(self.s6.diff(self.s6).changed(), set([]))

    def test_diff_reason(self):
        nservice12 = NmapParser.parse(port_string_other12)
        nservice13 = NmapParser.parse(port_string_other13)
        ddict = nservice12.diff(nservice13)
        self.assertEqual(ddict.changed(), set(['reason']))

    def test_noservice(self):
        noservice = NmapParser.parse(port_noservice)
        self.assertEqual(noservice.service, "")

    def test_owner(self):
        serviceowner = NmapParser.parse(port_owner)
        self.assertEqual(serviceowner.owner, "edwige")

    def test_tunnel(self):
        servicetunnel = NmapParser.parse(port_tunnel)
        self.assertEqual(servicetunnel.tunnel, "ssl")


if __name__ == '__main__':
    test_suite = ['test_port_state_changed', 'test_port_state_unchanged',
                  'test_port_service_changed', 'test_eq_service',
                  'test_diff_service']
    suite = unittest.TestSuite(map(TestNmapService, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
