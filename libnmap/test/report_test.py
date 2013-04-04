#!/usr/bin/env python

import unittest
import os, sys

#sys.path.append("".join([os.path.dirname(__file__), "/../"]))
from libnmap import NmapParser, NmapReport

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
        self.flist_one = [{'file': 'test/1_hosts_nohostname.xml', 'hosts': 1}]
        self.flist_two = [{'file': 'test/2_hosts.xml', 'hosts': 2, 
                           'elapsed': '134.36', 'endtime': "1361738040", 
                           'summary': "Nmap done at Sun Feb 24 21:34:00 2013; 2 IP addresses (2 hosts up) scanned in 134.36 seconds"}]

        self.hlist = [ {'hostname': 'localhost', 'ports': 5, 'open': 5}, 
                          {'hostname': 'localhost2', 'ports': 4, 'open': 2},
                          {'hostname': 'scanme.nmap.org', 'ports': 4, 'open': 3},
                          {'hostname': '1.1.1.1', 'ports': 2, 'open': 0},
        ]
        self.flist_banner = [ {'file': 'test/1_hosts_banner.xml', 
                               'banner': { '631': 'product: CUPS version: 1.4',
                                           '3306': 'product: MySQL version: 5.1.61',
                                           '22': 'product: OpenSSH extrainfo: protocol 2.0 version: 5.3',
                                           '25': 'product: Postfix smtpd hostname:  jambon.localdomain',
                                           '111': '',
                               }
        } ]

        self.flist = self.flist_full
        self.port_string = '<port protocol="tcp" portid="25"><state state="filtered" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="smtp" method="table" conf="3"/></port>'
        self.port_string_other2 = '<port protocol="tcp" portid="25"><state state="open" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="smtp" method="table" conf="3"/></port>'
        self.port_string_other3 = '<port protocol="tcp" portid="22"><state state="open" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="ssh" method="table" conf="3"/></port>'
        self.port_string_other4 = '<port protocol="tcp" portid="22"><state state="willy_woncka" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="willywoncka" method="table" conf="3"/></port>'

        self.port_string_other5 = '<port protocol="tcp" portid="22"><state state="willy_woncka" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="ssh" method="table" conf="3"/></port>'
        self.port_string_other6 = '<port protocol="tcp" portid="25"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="smtp" product="Postfix smtpd" hostname=" jambon.localdomain" method="probed" conf="10"/></port>'
        self.port_string_other7 = '<port protocol="tcp" portid="111"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="rpcbind" method="probed" conf="10"/></port>'
        self.port_string_other8 = '<port protocol="tcp" portid="631"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="ipp" product="CUPS" version="1.4" method="probed" conf="10"/></port>'
        self.port_string_other9 = '<port protocol="tcp" portid="631"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="ipp" product="COPS" version="1.4" method="probed" conf="10"/></port>'

    def test_report_constructor(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()
            raw_data = NmapParser.parse(s)

            nr = NmapReport(raw_data=raw_data)
            self.assertEqual(len(nr.scanned_hosts), testfile['hosts'])

            nr2 = NmapReport('test_report')
            nr2.set_raw_data(raw_data)
            self.assertEqual(len(nr2.scanned_hosts), testfile['hosts'])
            self.assertEqual(nr2.name, 'test_report')
            self.assertEqual(sorted(nr2.get_raw_data()), sorted(raw_data))

    def test_get_ports(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()

            nr = NmapReport(NmapParser.parse(s))
            for h in nr.scanned_hosts:
                for th in self.hlist:
                    if th['hostname'] == h.get_hostname():
                        self.assertEqual(th['ports'], len(h.get_ports()))
                        self.assertEqual(th['open'], len(h.get_open_ports()))

                for np in h.get_open_ports():
                    sport = h.get_port(np)
                    self.assertEqual(sport.port, np)

    def test_runstats(self):
        for testfile in self.flist_two:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()
            rdata = NmapParser.parse(s)
            nr = NmapReport(raw_data=rdata)
            for attr in ('endtime', 'summary', 'elapsed'):
                self.assertEqual(getattr(nr, attr), testfile[attr])

    def test_banner(self):
        for testfile in self.flist_banner:
            fd = open(testfile['file'], 'r')
            nr = NmapReport('testreport', NmapParser.parse(fd.read()))
            fd.close()

            for h in nr.scanned_hosts:
                for service in h.services:
                    b = service.banner
                    self.assertEqual(b, testfile['banner'][str(service.port)]) 
    
    def test_service_equal(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            np1 = NmapReport('np1', raw_data=NmapParser.parse(fd.read()))
            fd.close()
            fd = open(testfile['file'], 'r')
            np2 = NmapReport('np2', raw_data=NmapParser.parse(fd.read()))
            fd.close()

            host1 = np1.scanned_hosts.pop()
            host2 = np2.scanned_hosts.pop()
            'All the service of the host must be compare + the hash should be also the same'
            for i in range(len(host1.services)):
                self.assertEqual(hash(host1.services[i]),hash(host2.services[i]))
                self.assertEqual(host1.services[i] , host2.services[i])

            #print host1.serviceChanged(host2)


    def test_service_not_equal(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            np1 = NmapReport('np1', NmapParser.parse(fd.read()))
            fd.close()
            fd = open(testfile['file'], 'r')
            np2 = NmapReport('np2', NmapParser.parse(fd.read()))
            fd.close()

            host1 = np1.scanned_hosts.pop()
            host2 = np2.scanned_hosts.pop()
            for i in range(len(host1.services)): 
                host1.services[i]._state['state'] = 'changed'
                self.assertNotEqual(host1.services[i] , host2.services[i])
            #print "-----------" 
            #print host1.serviceChanged(host2)
            #print "-----------"

    def test_host_not_equal(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            np1 = NmapReport(raw_data=NmapParser.parse(fd.read()))
            fd.close()
            fd = open(testfile['file'], 'r')
            np2 = NmapReport(raw_data=NmapParser.parse(fd.read()))
            fd.close()

            host1 = np1.scanned_hosts.pop()
            host2 = np2.scanned_hosts.pop()
            
            host1._address['addr'] = 'xxxxxx'
            self.assertNotEqual(host1 , host2)

    def test_host_equal(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            np1 = NmapReport(raw_data=NmapParser.parse(fd.read()))
            fd.close()
            fd = open(testfile['file'], 'r')
            np2 = NmapReport(raw_data=NmapParser.parse(fd.read()))
            fd.close()

            host1 = np1.scanned_hosts.pop()
            host2 = np2.scanned_hosts.pop()
            
            host1.services[0]._portid ='23'
            self.assertEqual(host1 , host2)

    def test_port_state_changed(self):
        nservice1 = NmapParser.parse_port(self.port_string)
        nservice2 = NmapParser.parse_port(self.port_string_other2)
        nservice3 = NmapParser.parse_port(self.port_string_other3)
        nservice4 = NmapParser.parse_port(self.port_string_other4)

        self.assertEqual(nservice1.get_state_changed(nservice2).pop(), 'state')
        self.assertEqual(nservice1.get_state_changed(nservice3), set())
        self.assertEqual(nservice1.get_state_changed(nservice4), set())

        self.assertEqual(nservice2.get_state_changed(nservice3), set())

        self.assertEqual(nservice3.get_state_changed(nservice4).pop(), 'state')
### FIXME: <open question>
#          - the whole _state dict is evaluate for diff. Is this what we really want? 
#            Shouldn't we create a new dict to diff based on some keys ?
#"""
#1 = '<port protocol="tcp" portid="25"><state state="filtered" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/>
#    <service name="smtp" method="table" conf="3"/></port>'
#2 = '<port protocol="tcp" portid="25"><state state="open" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/>
#     <service name="smtp" method="table" conf="3"/></port>'
#3 = '<port protocol="tcp" portid="22"><state state="open" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/>
#     <service name="smtp" method="table" conf="3"/></port>'
#4 = '<port protocol="tcp" portid="22"><state state="willy_woncka" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/>
#     <service name="smtp" method="table" conf="3"/></port>'
#"""

    def test_port_state_unchanged(self):
        nservice1 = NmapParser.parse_port(self.port_string)
        nservice2 = NmapParser.parse_port(self.port_string_other2)
        nservice3 = NmapParser.parse_port(self.port_string_other3)
        nservice4 = NmapParser.parse_port(self.port_string_other4)

        self.assertEqual(nservice1.get_state_unchanged(nservice2), set(['reason', 'reason_ttl', 'reason_ip']))
        self.assertEqual(nservice1.get_state_unchanged(nservice3), set())
        self.assertEqual(nservice1.get_state_unchanged(nservice4), set())

        self.assertEqual(nservice1.get_state_unchanged(nservice2), set(['reason', 'reason_ttl', 'reason_ip']))
#
#1 '<port protocol="tcp" portid="25"><state state="filtered" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="smtp" method="table" conf="3"/></port>'
#2 = '<port protocol="tcp" portid="25"><state state="open" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="smtp" method="table" conf="3"/></port>'
#3 = '<port protocol="tcp" portid="22"><state state="open" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="ssh" method="table" conf="3"/></port>'
#4 = '<port protocol="tcp" portid="22"><state state="willy_woncka" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="willywoncka" method="table" conf="3"/></port>'
#
#5 = '<port protocol="tcp" portid="22"><state state="willy_woncka" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="ssh" method="table" conf="3"/></port>'
#6 = '<port protocol="tcp" portid="25"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="smtp" product="Postfix smtpd" hostname=" jambon.localdomain" method="probed" conf="10"/></port>'
#7 = '<port protocol="tcp" portid="111"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="rpcbind" method="probed" conf="10"/></port>'
#8 = '<port protocol="tcp" portid="631"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="ipp" product="CUPS" version="1.4" method="probed" conf="10"/></port>'
    def test_port_service_changed(self):
        nservice1 = NmapParser.parse_port(self.port_string)
        nservice2 = NmapParser.parse_port(self.port_string_other2)
        nservice4 = NmapParser.parse_port(self.port_string_other4)
        nservice5 = NmapParser.parse_port(self.port_string_other5)
        nservice8 = NmapParser.parse_port(self.port_string_other8)
        nservice9 = NmapParser.parse_port(self.port_string_other9)

        self.assertEqual(nservice1.get_service_changed(nservice2), set())
        self.assertEqual(nservice5.get_service_changed(nservice4).pop(), 'name')
        # banner changed
        self.assertEqual(nservice8.get_service_changed(nservice9).pop(), 'product')
#

if __name__ == '__main__':
#    test_suite = ['test_get_hosts' , 'test_get_ports', 'test_runstats', 'test_banner', 'test_serviceEqual', 'test_serviceNotEqual', 'test_HostNotEqual', 'test_HostEqual']
    test_suite = ['test_report_constructor', 'test_get_ports', 'test_runstats',
                  'test_banner' , 'test_service_equal', 'test_service_not_equal', 
                  'test_host_not_equal' , 'test_host_equal', 'test_port_state_changed',
                  'test_port_state_unchanged', 'test_port_service_changed' ] 
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
