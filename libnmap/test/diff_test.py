#!/usr/bin/env python

import unittest
import os, sys

from libnmap import NmapParser, NmapParserException, NmapReport

host1 = """
<host starttime="1361738377" endtime="1361738377"><status state="up" reason="localhost-response"/>
<address addr="127.0.0.1" addrtype="ipv4"/>
<hostnames>
<hostname name="localhost" type="user"/>
<hostname name="localhost" type="PTR"/>
</hostnames>
<ports><extraports state="closed" count="995">
<extrareasons reason="conn-refused" count="995"/>
</extraports>
<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ssh" method="table" conf="3"/></port>
<port protocol="tcp" portid="25"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="smtp" method="table" conf="3"/></port>
<port protocol="tcp" portid="111"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="rpcbind" method="table" conf="3"/></port>
<port protocol="tcp" portid="631"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ipp" method="table" conf="3"/></port>
<port protocol="tcp" portid="3306"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="mysql" method="table" conf="3"/></port>
</ports>
<times srtt="2100" rttvar="688" to="100000"/>
</host>
"""
host2 = """
<host starttime="1361738318" endtime="1361738677"><status state="up" reason="localhost-response"/>
<address addr="127.0.0.1" addrtype="ipv4"/>
<hostnames>
<hostname name="localhost" type="user"/>
<hostname name="localhost" type="PTR"/>
</hostnames>
<ports><extraports state="closed" count="995">
<extrareasons reason="conn-refused" count="995"/>
</extraports>
<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ssh" method="table" conf="3"/></port>
<port protocol="tcp" portid="25"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="smtp" method="table" conf="3"/></port>
<port protocol="tcp" portid="111"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="rpcbind" method="table" conf="3"/></port>
<port protocol="tcp" portid="631"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ipp" method="table" conf="3"/></port>
<port protocol="tcp" portid="3306"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="mysql" method="table" conf="3"/></port>
</ports>
<times srtt="2100" rttvar="688" to="100000"/>
</host>
"""
host3 = """
<host starttime="1361738277" endtime="1361738477"><status state="down" reason="localhost-response"/>
<address addr="127.0.0.1" addrtype="ipv4"/>
<hostnames>
<hostname name="localhost" type="user"/>
<hostname name="localhost" type="PTR"/>
</hostnames>
<ports><extraports state="closed" count="995">
<extrareasons reason="conn-refused" count="995"/>
</extraports>
<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ssh" method="table" conf="3"/></port>
<port protocol="tcp" portid="111"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="rpcbind" method="table" conf="3"/></port>
<port protocol="tcp" portid="631"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ipp" method="table" conf="3"/></port>
<port protocol="tcp" portid="3306"><state state="closed" reason="syn-ack" reason_ttl="0"/><service name="mysql" method="table" conf="3"/></port>
<port protocol="tcp" portid="3307"><state state="closed" reason="syn-ack" reason_ttl="0"/><service name="mysql" method="table" conf="3"/></port>
</ports>
<times srtt="2100" rttvar="688" to="100000"/>
</host>
"""

service1 = """
<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ssh" method="table" conf="3"/></port>
"""
service2 = """
<port protocol="udp" portid="22"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ssh" method="table" conf="3"/></port>
"""
service3 = """
<port protocol="udp" portid="53"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ssh" method="table" conf="3"/></port>
"""
service4 = """
<port protocol="tcp" portid="22"><state state="closed" reason="syn-ack" reason_ttl="0"/><service name="ssh" method="table" conf="3"/></port>
"""
service5 = """
<port protocol="tcp" portid="3306"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="mysql" product="MySQL" version="5.1.62" method="probed" conf="10"/></port>
"""
service6 = """
<port protocol="tcp" portid="3306"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="mysql" product="MySQL" version="5.1.61" method="probed" conf="10"/></port>
"""
service7 = """
<port protocol="tcp" portid="3306"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="mysql" product="MySQL" version="5.1.61" method="probed" conf="10"/></port>
"""
class TestNmapParser(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [{'file': "%s/%s" % (fdir, 'files/2_hosts.xml'), 'hosts': 2}, {'file': "%s/%s" % (fdir,'files/1_hosts.xml'), 'hosts': 1},]
        self.flist = self.flist_full

    def test_diff_host_list(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        d1 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/1_hosts.xml'))
        d2 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/2_hosts.xml'))
        d3 = NmapParser.parse_fromfile("%s/%s" % (fdir, 'files/2_hosts_achange.xml'))

        r1 = NmapReport("r1", d1)
        r2 = NmapReport("r2", d2)
        r3 = NmapReport("r3", d1)
        r4 = NmapReport("r4", d3)

        d = r1.diff(r2)
        print "changed: %s" % (d.changed())
        print "unchanged: %s" % (d.unchanged())
        print "added: %s" % (d.added())
	print "removed: %s" % (d.removed())
        print "___________________________________"
        d = r1.diff(r3)
        print "changed: %s" % (d.changed())
        print "unchanged: %s" % (d.unchanged())
        print "added: %s" % (d.added())
	print "removed: %s" % (d.removed())
        print "___________________________________"

        d = r2.diff(r4)
        print "changed: %s" % (d.changed())
        print "unchanged: %s" % (d.unchanged())
        print "added: %s" % (d.added())
	print "removed: %s" % (d.removed())

    def test_diff_host(self):
        h1 = NmapParser.parse_host(host1)
        h2 = NmapParser.parse_host(host2)
        h3 = NmapParser.parse_host(host3)

        #self.assertEqual(d1, d2)
        #self.assertNotEqual(d2, d3)

        #print d1.g
        c1 = h1.diff(h3)
        print "changed: %s" % (c1.changed())
        print "added: %s" % (c1.added())
        print "removed: %s" % (c1.removed())
        print "unchanged: %s" % (c1.unchanged())

    def test_eq_service(self):
        s1 = NmapParser.parse_port(service1)
        s2 = NmapParser.parse_port(service2)
        s3 = NmapParser.parse_port(service3)
        s4 = NmapParser.parse_port(service4)
        s5 = NmapParser.parse_port(service5)
        s6 = NmapParser.parse_port(service6)
        s7 = NmapParser.parse_port(service7)

        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertEqual(s1, s4)

        self.assertNotEqual(s5, s6)
        self.assertEqual(s6, s7)
    
if __name__ == '__main__':
  #  test_suite = [ 'test_diff_host_list', 'test_diff_host' ]
  #  test_suite = [ 'test_diff_host' ]
    test_suite = [ 'test_eq_service' ]
    suite = unittest.TestSuite(map(TestNmapParser, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite) ## for more verbosity uncomment this line and comment next line
