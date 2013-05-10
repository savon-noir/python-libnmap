# libnmap

[![Build Status](https://travis-ci.org/savon-noir/python-nmap-lib.png)](https://travis-ci.org/savon-noir/python-nmap-lib)

## Code status
A few basic stuff need to be added (check TODO, please forkme and issue pull
requests)

## What

libnmap is a python toolkit for manipulating nmap. It currently offers the following modules:
- process: enables you to launch nmap scans
- parse: enables you to parse nmap reports or scan results (only XML so far) from a file, a string,...
- report: enables you to manipulate a parsed scan result and de/serialize scan results in a json format
- diff: enables you to see what changed between two scans
- common: contains basic nmap objects like NmapHost and NmapService. It is to note that each object can be "diff()ed" with another similar object.
- plugins: enables you to support datastores for your scan results directly in the "NmapReport" object from report module
    - mongodb: only plugin implemented so far, ultra basic, for POC purpose only
    - couchdb: todo
    - sqlalchemy: todo
    - elastic search: todo
    - csv: todo

## How

### Launch a simple scan with event callback
Below a simple example on how to run a nmap scan using a callback function.
No advanced data manipulations with our parser. The callback will simply
printout the percentage done and the etc. The event callback is triggered
each time nmap outputs data. It is to note that a fixed options forces
nmap to send its progress to the lib every two seconds. Consequently, at least
every two seconds, the callback function is triggered even if nmap is not
printing out stuff.

```python
#!/usr/bin/env python
from libnmap import NmapProcess
        
def main(argv):
    def mycallback(nmapscan=None, data=""):
        if nmapscan.is_running():
            print "Progress: %s %% - ETC: %s" % (nmapscan.progress,
                                                 nmapscan.etc)

    nm = NmapProcess("scanme.nmap.org", options="-sV", event_callback=mycallback)
    rc = nm.run()

    if rc == 0:
        print "Scan started at {0} nmap version: {1}".format(nm.starttime,
                                                             nm.version)
        print "state: {0} (rc: {1})".format(nm.state, nm.rc)
        print "results size: {0}".format(len(nm.stdout))
        print "Scan ended {0}: {1}".format(nm.endtime, nm.summary)
    else:
        print "state: {0} (rc: {1})".format(nm.state, nm.rc)
        print "Error: {stderr}".format(stderr=nm.stderr)
        print "Result: {0}".format(nm.stdout)


if __name__ == '__main__':
    main(sys.argv[1:])
```

### Launch a nmap scan
Here a consequent example on how to use libnmap:
```python
#!/usr/bin/env python
from libnmap import NmapProcess, NmapParser, NmapParserException


# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    nm = NmapProcess(targets, options)
    rc = nm.run()
    if rc != 0:
        print "nmap scan failed: %s" % (nm.stderr)

    try:
        parsed = NmapParser.parse(nm.stdout)
    except NmapParserException as e:
        print "Exception raised while parsing scan: %s" % (e.msg)

    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    print "Starting Nmap {0} ( http://nmap.org ) at {1}".format(
        nmap_report._nmaprun['version'],
        nmap_report._nmaprun['startstr'])

    for host in nmap_report.hosts:
        print "Nmap scan report for {0} ({1})".format(
            host.hostname,
            host.address)
        print "Host is {0}.".format(host.status)
        print "  PORT     STATE         SERVICE"

        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print pserv
    print nmap_report.summary


if __name__ == "__main__":
    report = do_scan("127.0.0.1", "-sV")
    print_scan(report)
```

### De/Serialize NmapReport
Easy:
```python
from libnmap import NmapParser, NmapReport
from libnmap import ReportDecoder, ReportEncoder
import json
 
r = NmapParser.parse_fromfile('/root/dev/python-nmap-lib/libnmap/test/files/1_hosts.xml')
 
# create a json object from an NmapReport instance
j = json.dumps(r, cls=ReportEncoder)
  
# create a NmapReport instance from a json object
nmapreport = json.loads(j, cls=ReportDecoder)
nmapreport.name
```
