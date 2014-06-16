#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.objects.os import CPE
import unittest


class TestNmapFP(unittest.TestCase):
    def setUp(self):
        self.cpelist = ['cpe:/a:apache:http_server:2.2.22',
                        'cpe:/a:heimdal:kerberos',
                        'cpe:/a:openbsd:openssh:5.9p1',
                        'cpe:/o:apple:iphone_os:5',
                        'cpe:/o:apple:mac_os_x:10.8',
                        'cpe:/o:apple:mac_os_x',
                        'cpe:/o:linux:linux_kernel:2.6.13',
                        'cpe:/o:linux:linux_kernel',
                        'cpe:/o:microsoft:windows_7',
                        'cpe:/o:microsoft:windows_7::-:professional',
                        'cpe:/o:microsoft:windows_7::sp1',
                        'cpe:/o:microsoft:windows',
                        'cpe:/o:microsoft:windows_server_2008::beta3',
                        'cpe:/o:microsoft:windows_server_2008',
                        'cpe:/o:microsoft:windows_server_2008::sp1',
                        'cpe:/o:microsoft:windows_vista::-',
                        'cpe:/o:microsoft:windows_vista::sp1',
                        'cpe:/o:microsoft:windows_vista::sp2']

    def test_cpe(self):
        apa = CPE(self.cpelist[0])

        self.assertTrue(apa.is_application())
        self.assertFalse(apa.is_hardware())
        self.assertFalse(apa.is_operating_system())
   

        win = CPE(self.cpelist[12])
        self.assertEqual(win.get_vendor(), 'microsoft')
        self.assertEqual(win.get_product(), 'windows_server_2008')
        self.assertEqual(win.get_version(), '')
        self.assertEqual(win.get_update(), 'beta3')
        self.assertEqual(win.get_edition(), '')
        self.assertEqual(win.get_language(), '')

    def test_full_cpe(self):
        cpestr = 'cpe:/a:mozilla:firefox:2.0::osx:es-es'
        resdict = { 'part':'/a', 'vendor':"mozilla", 'product':"firefox", 'version':"2.0", 'update':'', 'edition':"osx", 'language':'es-es' }
        ocpe = CPE(cpestr)
        objdict = {'part': ocpe.get_part(),
                   'vendor': ocpe.get_vendor(),
                   'product': ocpe.get_product(),
                   'version': ocpe.get_version(),
                   'update': ocpe.get_update(),
                   'language': ocpe.get_language(),
                   'edition': ocpe.get_edition()
        }
        self.assertEqual(objdict, resdict)

if __name__ == '__main__':
    test_suite = ['test_cpe', 'test_full_cpe']
    suite = unittest.TestSuite(map(TestNmapFP, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
