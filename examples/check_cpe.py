#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.parser import NmapParser

rep = NmapParser.parse_fromfile('libnmap/test/files/full_sudo6.xml')

print("Nmap scan discovered {0}/{1} hosts up".format(rep.hosts_up,
                                                     rep.hosts_total))
for _host in rep.hosts:
    if _host.is_up():
        print("+ Host: {0} {1}".format(_host.address,
                                       " ".join(_host.hostnames)))

        # get CPE from service if available
        for s in _host.services:
            print("    Service: {0}/{1} ({2})".format(s.port,
                                                      s.protocol,
                                                      s.state))
            # NmapService.cpelist returns an array of CPE objects
            for _serv_cpe in s.cpelist:
                print("        CPE: {0}".format(_serv_cpe.cpestring))

        if _host.os_fingerprinted:
            print("  OS Fingerprints")
            for osm in _host.os.osmatches:
                print("    Found Match:{0} ({1}%)".format(osm.name,
                                                          osm.accuracy))
                # NmapOSMatch.get_cpe() method return an array of string
                # unlike NmapOSClass.cpelist which returns an array of CPE obj
                for cpe in osm.get_cpe():
                    print("\t    CPE: {0}".format(cpe))
