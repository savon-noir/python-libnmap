#!/usr/bin/env python
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

nm = NmapProcess('127.0.0.1', '-sP')
rc = nm.run()
if rc != 0:
    print("nmap scan failed: {0}".format(nm.stderr))

try:
    report = NmapParser.parse(nm.stdout)
except NmapParserException as e:
    print("Exception raised while parsing scan: {0}".format(e.msg))

print(len(nm.stdout))
