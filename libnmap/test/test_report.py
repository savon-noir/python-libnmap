#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

#sys.path.append("".join([os.path.dirname(__file__), "/../"]))
from libnmap.parser import NmapParser
from libnmap.diff import NmapDiffException


class TestNmapParser(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [{'file': "%s/%s" % (fdir, 'files/2_hosts.xml'),
                            'hosts': 2},
                           {'file': "%s/%s" % (fdir, 'files/1_hosts.xml'),
                            'hosts': 1},
                           {'file': "%s/%s" % (fdir,
                                    'files/1_hosts_banner_ports_notsyn.xml'),
                            'hosts': 1},
                           {'file': "%s/%s" % (fdir,
                                    'files/1_hosts_banner_ports.xml'),
                            'hosts': 1},
                           {'file': "%s/%s" % (fdir,
                                    'files/1_hosts_banner.xml'),
                            'hosts': 1},
                           {'file': "%s/%s" % (fdir,
                                               'files/2_hosts_version.xml'),
                            'hosts': 2},
                           {'file': "%s/%s" % (fdir,
                                               'files/2_tcp_hosts.xml'),
                            'hosts': 2},
                           {'file': "%s/%s" % (fdir,
                                               'files/1_hosts_nohostname.xml'),
                            'hosts': 1}]

        self.flist_one = [{'file': "%s/%s" % (fdir,
                                              'files/1_hosts_nohostname.xml'),
                           'hosts': 1}]
        self.flist_two = [{'file': "%s/%s" % (fdir, 'files/2_hosts.xml'),
                           'hosts': 2,
                           'elapsed': '134.36', 'endtime': "1361738040",
                           'summary': ("Nmap done at Sun Feb 24 21:34:00 2013;"
                                       " 2 IP addresses (2 hosts up) scanned"
                                       " in 134.36 seconds")}]

        self.hlist = [{'hostname': 'localhost', 'ports': 5, 'open': 5},
                      {'hostname': 'localhost2', 'ports': 4, 'open': 2},
                      {'hostname': 'scanme.nmap.org', 'ports': 4, 'open': 3},
                      {'hostname': '1.1.1.1', 'ports': 2, 'open': 0}]
        self.flist_banner = [{'file': "%s/%s" % (fdir,
                                                 'files/1_hosts_banner.xml'),
                              'banner': {
                                  '631': 'product: CUPS version: 1.4',
                                  '3306':
                                      'product: MySQL version: 5.1.61',
                                  '22': ("product: OpenSSH version: 5.3"
                                         " extrainfo: protocol 2.0"),
                                  '25': ("product: Postfix smtpd"
                                         " hostname:  jambon.localdomain"),
                                  '111': ''}}]

        self.flist = self.flist_full

    def test_report_constructor(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()
            nr = NmapParser.parse(s)
            nr2 = NmapParser.parse(s)

            self.assertEqual(len(nr.hosts), testfile['hosts'])

            self.assertEqual(len(nr2.hosts), testfile['hosts'])
            self.assertEqual(sorted(nr2.get_raw_data()),
                             sorted(nr.get_raw_data()))

    def test_get_ports(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()

            nr = NmapParser.parse(s)
            for h in nr.hosts:
                for th in self.hlist:
                    continue
# TODO FIX THIS TEST
#                    if th['hostname'] == h.hostnames[0]:
#                    self.assertEqual(th['ports'], len(h.get_ports()))
#                   self.assertEqual(th['open'], len(h.get_open_ports()))

                for np in h.get_open_ports():
                    sport = h.get_service(np[0], np[1])
                    self.assertEqual((sport.port, sport.protocol), np)

    def test_runstats(self):
        for testfile in self.flist_two:
            fd = open(testfile['file'], 'r')
            s = fd.read()
            fd.close()
            nr = NmapParser.parse(s)
            self.assertEqual(getattr(nr, 'endtime'), int(testfile['endtime']))
            self.assertEqual(getattr(nr, 'summary'), testfile['summary'])
            self.assertEqual(getattr(nr, 'elapsed'), float(testfile['elapsed']))

    def test_banner(self):
        for testfile in self.flist_banner:
            fd = open(testfile['file'], 'r')
            nr = NmapParser.parse(fd.read())
            fd.close()

            for h in nr.hosts:
                for service in h.services:
                    b = service.banner
                    self.assertEqual(b, testfile['banner'][str(service.port)])

    def test_service_equal(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            np1 = NmapParser.parse(fd.read())
            fd.close()
            fd = open(testfile['file'], 'r')
            np2 = NmapParser.parse(fd.read())
            fd.close()

            host1 = np1.hosts.pop()
            host2 = np2.hosts.pop()
            """All the service of the host must be compared and
               the hash should be also the same"""
            for i in range(len(host1.services)):
                self.assertEqual(hash(host1.services[i]),
                                 hash(host2.services[i]))
                self.assertEqual(host1.services[i],
                                 host2.services[i])

            #print host1.serviceChanged(host2)

    def test_service_not_equal(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            np1 = NmapParser.parse(fd.read())
            fd.close()
            fd = open(testfile['file'], 'r')
            np2 = NmapParser.parse(fd.read())
            fd.close()

            host1 = np1.hosts.pop()
            host2 = np2.hosts.pop()
            for i in range(len(host1.services)):
                host1.services[i]._state['state'] = 'changed'
                self.assertNotEqual(host1.services[i], host2.services[i])
            #print "-----------"
            #print host1.serviceChanged(host2)
            #print "-----------"

    def test_host_not_equal(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            np1 = NmapParser.parse(fd.read())
            fd.close()
            fd = open(testfile['file'], 'r')
            np2 = NmapParser.parse(fd.read())
            fd.close()

            host1 = np1.hosts.pop()
            host2 = np2.hosts.pop()

            host1.address = {'addr': '1.3.3.7', 'addrtype': 'ipv4'}
            self.assertNotEqual(host1, host2)

    def test_host_equal(self):
        for testfile in self.flist:
            fd = open(testfile['file'], 'r')
            np1 = NmapParser.parse(fd.read())
            fd.close()
            fd = open(testfile['file'], 'r')
            np2 = NmapParser.parse(fd.read())
            fd.close()

            host1 = np1.hosts.pop()
            host2 = np2.hosts.pop()

            host1.services[0]._portid = '23'
            self.assertEqual(host1, host2)

    def test_host_address_changed(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        fd1 = open("%s/%s" % (fdir, 'files/1_hosts_down.xml'), 'r')
        fd2 = open("%s/%s" % (fdir, 'files/1_hosts.xml'), 'r')
        nr1 = NmapParser.parse(fd1.read())
        nr2 = NmapParser.parse(fd2.read())
        h1 = nr1.hosts[0]
        h2 = nr2.hosts[0]
        self.assertRaises(NmapDiffException, h1.diff, h2)

    def test_host_address_unchanged(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        fd1 = open("%s/%s" % (fdir, 'files/1_hosts_down.xml'), 'r')
        fd2 = open("%s/%s" % (fdir, 'files/1_hosts.xml'), 'r')
        fd3 = open("%s/%s" % (fdir, 'files/1_hosts.xml'), 'r')
        nr1 = NmapParser.parse(fd1.read())
        nr2 = NmapParser.parse(fd2.read())
        nr3 = NmapParser.parse(fd3.read())

        h1 = nr1.hosts.pop()
        h2 = nr2.hosts.pop()
        h3 = nr3.hosts.pop()

        self.assertRaises(NmapDiffException, h1.diff, h2)
        self.assertEqual(h2.diff(h3).changed(), set([]))
        self.assertEqual(h2.diff(h3).added(), set([]))
        self.assertEqual(h2.diff(h3).removed(), set([]))
        self.assertEqual(h2.diff(h3).unchanged(),
                         set(['status',
                              "NmapService::tcp.22",
                              "NmapService::tcp.111",
                              "NmapService::tcp.631",
                              'hostnames',
                              "NmapService::tcp.3306",
                              'address',
                              "NmapService::tcp.25"]))

if __name__ == '__main__':
    test_suite = ['test_report_constructor', 'test_get_ports',
                  'test_runstats', 'test_banner', 'test_service_equal',
                  'test_service_not_equal', 'test_host_not_equal',
                  'test_host_equal', 'test_host_address_changed',
                  'test_host_address_unchanged']

    suite = unittest.TestSuite(map(TestNmapParser, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
