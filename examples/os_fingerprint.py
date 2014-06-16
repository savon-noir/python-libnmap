#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.parser import NmapParser

rep = NmapParser.parse_fromfile('libnmap/test/files/os_scan6.xml')

print("{0}/{1} hosts up".format(rep.hosts_up, rep.hosts_total))
for _host in rep.hosts:
    if _host.is_up():
        print("{0} {1}".format(_host.address, " ".join(_host.hostnames)))
        if _host.os_fingerprinted:
            print("OS Fingerprint:")
            msg = ''
            for osm in _host.os.osmatches:
                print("Found Match:{0} ({1}%)".format(osm.name, osm.accuracy))
                for osc in osm.osclasses:
                    print("\tOS Class: {0}".format(osc.description))
                    for cpe in osc.cpelist:
                        print("\tCPE: {0}".format(cpe.cpestring))
        else:
            print("No fingerprint available")
