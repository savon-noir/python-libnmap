<< WAIT

This code is under development. Object's API are likely to change. 

The below README is no more applicable. Will be updated soon.

>>

[![Build Status](https://travis-ci.org/bmx0r/python-nmap-lib.png?branch=travis-ci)](https://travis-ci.org/bmx0r/python-nmap-lib)

================
Python-Nmap-Libs
================

What
====

Python-Nmap-Libs is a set of librairies that enables you to easily:
* Launch Nmap scans
* Control events during scan run with a callback function
* Parse and manipulate Nmap scan results
* Import/Export scans results from XML files or created via the lib
* Diff scan reports

How
===

Code sample:
------------

#!/usr/bin/env python
import sys
from libnmap import NmapProcess
from libnmap import NmapParser

def main(argv):
    def mycallback(nmapscan=None, data=""):
        if nmapscan.is_running():
            print "Progress: %s %% - ETC: %s" % (nmapscan.progress, nmapscan.etc)

    nm = NmapProcess("localhost", options="-sV", event_callback=mycallback)
    rc = nm.run()

    if rc == 0:
        print "Scan started {0} - NMAP v{1}".format(nm.starttime, nm.nmap_version)

        np = NmapParser(nm.stdout)
        np.parse()
        for h in np.get_hosts():
            for service in h.services:
                print "{0}/{1}: {2} ({3})".format(service.port,
                                         service.protocol, service.state, service.get_banner())
        print "Scan ended {0}: {1}".format(nm.endtime, nm.summary)
    else:
        print "Error: {stderr}".format(stderr=nm.stderr)
        print "Result: {0}".format(nm.stdout)

if __name__ == '__main__':
    main(sys.argv[1:])
