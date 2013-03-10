===========
PY-NMAP
===========

Py-Nmap is a set of librairies that enables you to easily:
* launch Nmap scans
* control event with a callback function
* parse the results of scans
* make use of the results
* import/export scans results from XML files or created via the lib
* make scan report diffs

Code sample:
#!/usr/bin/env python
import sys
from libnmap import NmapProcess
from libnmap import NmapParser, NmapHost

def main(argv):
    def mycallback(nmapscan=None, data=""):
        if nmapscan.is_running():
            print "Progress: %s %% - ETC: %s" % (nmapscan.progress, nmapscan.etc)

    nm = NmapProcess("localhost", options="-sT", event_callback=mycallback)
    rc = nm.run()

    if rc == 0:
        print "Scan started {0} {1}".format(nm.starttime, nm.nmap_version)
        print "Scan ended {0}: {1}".format(nm.endtime, nm.summary)

        np = NmapParser(nm.stdout)
        np.parse()
        for h in np.get_hosts():
            plist = h.get_ports()
            for pno in plist:
                p = h.get_port(pno)
                print "Port: {0}/{1}: {2} ({3})".format(p['port'],
                                         p['protocol'], p['state'], p['name'])
    else:
        print "Error: {stderr}".format(stderr=nm.stderr)
        print "Result: {0}".format(nm.stdout)

if __name__ == '__main__':
    main(sys.argv[1:])
