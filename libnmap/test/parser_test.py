#!/usr/bin/env python

import unittest
import os, sys

#sys.path.append("".join([os.path.dirname(__file__), "/../"]))
from libnmap import NmapParser

class TestNmapParser(unittest.TestCase):
    def setUp(self):
        self.flist_full = [{'file': 'test/2_hosts.xml', 'hosts': 2}, {'file': 'test/1_hosts.xml', 'hosts': 1},
                   {'file': 'test/1_hosts_banner_ports_notsyn.xml', 'hosts': 1},
                  # {'file': 'test/1_hosts_banner_ports_xmas.xml', 'hosts': 1},
                   {'file': 'test/1_hosts_banner_ports.xml', 'hosts': 1},
                   {'file': 'test/1_hosts_banner.xml', 'hosts': 1},
                   {'file': 'test/2_hosts_version.xml', 'hosts': 2},
                  # {'file': 'test/2_null_hosts.xml', 'hosts': 2},
                   {'file': 'test/2_tcp_hosts.xml', 'hosts': 2},
                   {'file': 'test/1_hosts_nohostname.xml', 'hosts': 1},
        ]
        self.flist = self.flist_full

        self.ports_string = """<ports><extraports state="closed" count="996">
<extrareasons reason="resets" count="996"/>
</extraports>
<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="53"/><service name="ssh" method="table" conf="3"/></port>
<port protocol="tcp" portid="25"><state state="filtered" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="smtp" method="table" conf="3"/></port>
<port protocol="tcp" portid="80"><state state="open" reason="syn-ack" reason_ttl="51"/><service name="http" method="table" conf="3"/></port>
<port protocol="tcp" portid="9929"><state state="open" reason="syn-ack" reason_ttl="53"/><service name="nping-echo" method="table" conf="3"/></port>
</ports>
                       """

        self.port_string = '<port protocol="tcp" portid="25"><state state="filtered" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="smtp" method="table" conf="3"/></port>'

    def test_class_parser(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()
            r = NmapParser.parse(s)
            print r
            #self.assertEqual(len(nr.get_hosts()), testfile['hosts'])

    def test_class_ports_parser(self):
            print NmapParser.parse_ports(self.ports_string)

    def test_class_port_parser(self):
            print NmapParser.parse_port(self.port_string)
if __name__ == '__main__':
    test_suite = [ 'test_class_parser', 'test_class_ports_parser' , 'test_class_port_parser']
#    io_file = StringIO()
    suite = unittest.TestSuite(map(TestNmapParser, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite) ## for more verbosity uncomment this line and comment next line
#    test_result = unittest.TextTestRunner(stream=io_file).run(suite)
#    if len(test_result.failures) or len(test_result.errors):
#  # uncomment for debugging info
#        print_errs = raw_input("Errors detected. Do you want to print the errors (y/N)?")
#        if print_errs == "y":
#            print io_file.getvalue()
#    io_file.close()
