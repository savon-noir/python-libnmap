#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from libnmap.parser import NmapParser


class TestNmapFP(unittest.TestCase):
    def setUp(self):
        fdir = os.path.dirname(os.path.realpath(__file__))
        self.flist_full = [{ 'file': "%s/%s" % (fdir, 'files/1_os_banner_scripts.xml'), 'os': 1},
                { 'file': "%s/%s" % (fdir, 'files/2_hosts_version.xml'), 'os': 1},
                { 'file': "%s/%s" % (fdir, 'files/1_hosts_banner_ports_notsyn.xml'), 'os': 0},
                { 'file': "%s/%s" % (fdir, 'files/1_hosts_banner.xml'), 'os': 0},
                { 'file': "%s/%s" % (fdir, 'files/1_hosts_down.xml'), 'os': 0}]
        self.flist = self.flist_full
        self.flist_os =  {'nv6': {'file': "%s/%s" % (fdir, 'files/full_sudo6.xml'), 'os': 0},
                'fullscan': { 'file': "%s/%s" % (fdir, 'files/fullscan.xml'), 'os': 0},
                'nv5': { 'file': "%s/%s" % (fdir, 'files/os_scan5.xml'), 'os': 0}
        }
        self.fos_class_probabilities = "{0}/{1}".format(fdir, "files/test_osclass.xml")

    def test_fp(self):
        for file_e in self.flist_full:
            rep = NmapParser.parse_fromfile(file_e['file'])
            for _host in rep.hosts:
                if file_e['os'] != 0:
                    self.assertTrue(_host.os_fingerprinted)
                elif file_e['os'] == 0:
                    self.assertFalse(_host.os_fingerprinted)
                else:
                    raise Exception

    def test_osclasses_new(self):
        oclines = [[[{'type': 'general purpose', 'accuracy': 100, 'vendor': 'Apple', 'osfamily': 'Mac OS X', 'osgen': '10.8.X'},
                    {'type': 'phone', 'accuracy': 100, 'vendor': 'Apple', 'osfamily': 'iOS', 'osgen': '5.X'},
                    {'type': 'media device', 'accuracy': 100, 'vendor': 'Apple', 'osfamily': 'iOS', 'osgen': '5.X'}]],
                    [
                        [{'type': 'general purpose', 'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': '2008'}],
                        [{'type': 'general purpose', 'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': '7'}],
                        [{'type': 'phone',           'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': 'Phone'}],
                        [{'type': 'general purpose', 'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': 'Vista'},
                        {'type': 'general purpose', 'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': '2008'},
                        {'type': 'general purpose', 'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': '7'}],
                        [{'type': 'general purpose', 'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': 'Vista'},
                        {'type': 'general purpose', 'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': '7'},
                        {'type': 'general purpose', 'accuracy': 100, 'vendor': 'Microsoft', 'osfamily': 'Windows', 'osgen': '2008'}]]
        ]
        rep = NmapParser.parse_fromfile(self.flist_os['nv6']['file'])
        hlist = []
        hlist.append(rep.hosts.pop())
        hlist.append(rep.hosts.pop())
        i=0
        j=0
        k=0
        for h in hlist:
            for om in h.os.osmatches:
                for oc in om.osclasses:
                    tdict = {'type': oc.type, 'accuracy': oc.accuracy, 'vendor': oc.vendor, 'osfamily': oc.osfamily, 'osgen': oc.osgen}
                    self.assertEqual(oclines[i][j][k], tdict)
                    k+=1
                j+=1
                k=0
            j=0
            i+=1

    def test_osmatches_new(self):
        rep = NmapParser.parse_fromfile(self.flist_os['nv6']['file'])
        hlist = []
        hlist.append(rep.hosts.pop())
        hlist.append(rep.hosts.pop())

        baseline = [[{'line': 6014, 'accuracy': 100, 'name': 'Apple Mac OS X 10.8 - 10.8.1 (Mountain Lion) (Darwin 12.0.0 - 12.1.0) or iOS 5.0.1'}],
                    [{'line': 52037, 'accuracy': 100, 'name': 'Microsoft Windows Server 2008 Beta 3'},
                    {'line': 52938, 'accuracy': 100, 'name': 'Microsoft Windows 7 Professional'},
                    {'line': 54362, 'accuracy': 100, 'name': 'Microsoft Windows Phone 7.5'},
                    {'line': 54897, 'accuracy': 100, 'name': 'Microsoft Windows Vista SP0 or SP1, Windows Server 2008 SP1, or Windows 7'},
                    {'line': 55210, 'accuracy': 100, 'name': 'Microsoft Windows Vista SP2, Windows 7 SP1, or Windows Server 2008'}]
                ]
        i=0
        j=0
        for h in hlist:
            for om in h.os.osmatches:
                tdict = {'line': om.line, 'accuracy': om.accuracy, 'name': om.name}
                self.assertEqual(baseline[i][j], tdict)
                j+=1
            j=0
            i+=1

    def test_osmatches_old(self):
        rep = NmapParser.parse_fromfile(self.flist_os['nv5']['file'])
        h1 = rep.hosts[4]
        h1osmatches = [{'line': -1, 'accuracy': 95, 'name': 'general purpose:Linux:Linux'},
            {'line': -1, 'accuracy': 90, 'name': 'WAP:Gemtek:embedded'},
            {'line': -1, 'accuracy': 89, 'name': 'general purpose:Nokia:Linux'},
            {'line': -1, 'accuracy': 88, 'name': 'webcam:AXIS:Linux'}]

        j=0
        for om in h1.os.osmatches:
            tdict = {'line': om.line, 'accuracy': om.accuracy, 'name': om.name}
            self.assertEqual(h1osmatches[j], tdict)
            j+=1

    def test_fpv6(self):
        fpval = "OS:SCAN(V=6.40-2%E=4%D=5/9%OT=88%CT=%CU=%PV=Y%DS=0%DC=L%G=N%TM=536BFF2F%P=x\nOS:86_64-apple-darwin10.8.0)SEQ(SP=F9%GCD=1%ISR=103%TI=RD%TS=A)OPS(O1=M3FD8\nOS:NW4NNT11SLL%O2=M3FD8NW4NNT11SLL%O3=M3FD8NW4NNT11%O4=M3FD8NW4NNT11SLL%O5=\nOS:M3FD8NW4NNT11SLL%O6=M3FD8NNT11SLL)WIN(W1=FFFF%W2=FFFF%W3=FFFF%W4=FFFF%W5\nOS:=FFFF%W6=FFFF)ECN(R=Y%DF=Y%TG=40%W=FFFF%O=M3FD8NW4SLL%CC=N%Q=)T1(R=Y%DF=\nOS:Y%TG=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%TG=40%W=0%S=A%A=\nOS:Z%F=R%O=%RD=0%Q=)U1(R=N)IE(R=N)\n"
        fparray = ['OS:SCAN(V=6.40-2%E=4%D=5/9%OT=88%CT=%CU=%PV=Y%DS=0%DC=L%G=N%TM=536BFF2F%P=x\nOS:86_64-apple-darwin10.8.0)SEQ(SP=F9%GCD=1%ISR=103%TI=RD%TS=A)OPS(O1=M3FD8\nOS:NW4NNT11SLL%O2=M3FD8NW4NNT11SLL%O3=M3FD8NW4NNT11%O4=M3FD8NW4NNT11SLL%O5=\nOS:M3FD8NW4NNT11SLL%O6=M3FD8NNT11SLL)WIN(W1=FFFF%W2=FFFF%W3=FFFF%W4=FFFF%W5\nOS:=FFFF%W6=FFFF)ECN(R=Y%DF=Y%TG=40%W=FFFF%O=M3FD8NW4SLL%CC=N%Q=)T1(R=Y%DF=\nOS:Y%TG=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%TG=40%W=0%S=A%A=\nOS:Z%F=R%O=%RD=0%Q=)U1(R=N)IE(R=N)\n']
        rep = NmapParser.parse_fromfile(self.flist_os['nv6']['file'])
        h1 = rep.hosts.pop()
        self.assertEqual(h1.os.fingerprint, fpval)
        self.assertEqual(h1.os.fingerprints, fparray)

    def test_fpv5(self):
        fpval = 'OS:SCAN(V=5.21%D=5/8%OT=22%CT=1%CU=37884%PV=Y%DS=0%DC=L%G=Y%TM=536BFE32%P=x\nOS:86_64-unknown-linux-gnu)SEQ(SP=100%GCD=1%ISR=106%TI=Z%CI=Z%II=I%TS=8)SEQ\nOS:(SP=101%GCD=1%ISR=107%TI=Z%CI=Z%II=I%TS=8)OPS(O1=M400CST11NW3%O2=M400CST\nOS:11NW3%O3=M400CNNT11NW3%O4=M400CST11NW3%O5=M400CST11NW3%O6=M400CST11)WIN(\nOS:W1=8000%W2=8000%W3=8000%W4=8000%W5=8000%W6=8000)ECN(R=Y%DF=Y%T=40%W=8018\nOS:%O=M400CNNSNW3%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(\nOS:R=Y%DF=Y%T=40%W=8000%S=O%A=S+%F=AS%O=M400CST11NW3%RD=0%Q=)T4(R=Y%DF=Y%T=\nOS:40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0\nOS:%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z\nOS:%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G\nOS:%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)\n'
        fparray = ['OS:SCAN(V=5.21%D=5/8%OT=22%CT=1%CU=37884%PV=Y%DS=0%DC=L%G=Y%TM=536BFE32%P=x\nOS:86_64-unknown-linux-gnu)SEQ(SP=100%GCD=1%ISR=106%TI=Z%CI=Z%II=I%TS=8)SEQ\nOS:(SP=101%GCD=1%ISR=107%TI=Z%CI=Z%II=I%TS=8)OPS(O1=M400CST11NW3%O2=M400CST\nOS:11NW3%O3=M400CNNT11NW3%O4=M400CST11NW3%O5=M400CST11NW3%O6=M400CST11)WIN(\nOS:W1=8000%W2=8000%W3=8000%W4=8000%W5=8000%W6=8000)ECN(R=Y%DF=Y%T=40%W=8018\nOS:%O=M400CNNSNW3%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(\nOS:R=Y%DF=Y%T=40%W=8000%S=O%A=S+%F=AS%O=M400CST11NW3%RD=0%Q=)T4(R=Y%DF=Y%T=\nOS:40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0\nOS:%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z\nOS:%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G\nOS:%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)\n']
        rep = NmapParser.parse_fromfile(self.flist_os['nv5']['file'])
        h1 = rep.hosts[4]
        self.assertEqual(h1.os.fingerprint, fpval)
        self.assertEqual(h1.os.fingerprints, fparray)

    def test_cpeservice(self):
        cpelist = ['cpe:/a:openbsd:openssh:5.9p1','cpe:/o:linux:linux_kernel']
        rep = NmapParser.parse_fromfile(self.flist_os['fullscan']['file'])
        h1 = rep.hosts.pop()
        s = h1.services[0]
        self.assertEqual(s.cpelist[0].cpestring, cpelist[0])
        self.assertEqual(s.cpelist[1].cpestring, cpelist[1])

    def test_os_class_probabilities(self):
        p = NmapParser.parse_fromfile(self.fos_class_probabilities)
        h = p.hosts.pop()
        osc = h.os_class_probabilities().pop()
        self.assertEqual(osc.type, "general purpose")
        self.assertEqual(osc.vendor, "Linux")
        self.assertEqual(osc.osfamily, "Linux")
        self.assertEqual(osc.osgen, "3.X")
        self.assertEqual(osc.accuracy, 100)

        #<osclass type="general purpose" vendor="Linux" osfamily="Linux" osgen="3.X" accuracy="100"><cpe>cpe:/o:linux:linux_kernel:3</cpe></osclass>
        

if __name__ == '__main__':
    test_suite = ['test_fp', 'test_fpv6', 'test_osmatches_new', 'test_osclasses_new',
            'test_fpv5', 'test_osmatches_old', 'test_cpeservice', 'test_os_class_probabilities']
    suite = unittest.TestSuite(map(TestNmapFP, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
