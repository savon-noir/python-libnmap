#!/usr/bin/env python
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

nm = NmapProcess('127.0.0.1', '-sP')
rc = nm.run()
if rc != 0:
    print "nmap scan failed: %s" % (nm.stderr)

try:
    report = NmapParser.parse(nm.stdout)
except NmapParserException as e:
    print "Exception raised while parsing scan: %s" % (e.msg)

print len(nm.stdout)
