#!/usr/bin/env python
import xml.etree.ElementTree as ET
from StringIO import StringIO
from libnmap import NmapHost, NmapService

class NmapParser:
    def __init__(self, nmap_report=None, type='XML'):
        self._nmap_xml_report = nmap_report
        self._nmap_dict_report = {'hosts': []}
        # CLASS "API":
        self.endtime = ''
        self.elapsed = ''
        self.summary = ''
        self.hosts_up = ''
        self.hosts_down = ''
        self.hosts_total = ''

    def parse(self):
        if not self._nmap_xml_report:
            raise Exception("No report to parse")
        tree = ET.parse(StringIO(self._nmap_xml_report))

        root = tree.getroot()
        self._nmap_dict_report[root.tag] = root.attrib
        for el in root:
            if el.tag == 'host': self.parse_host(el)
            elif el.tag == 'runstats': self.parse_runstats(el)
            #else: self._nmap_dict_report[el.tag] = el.attrib
            else: print "struct pparse unknown attr: %s value: %s" % (el.tag, el.get(el.tag))

    def parse_host(self, xelement):
        nhost = NmapHost()
        for xh in xelement:
            if xh.tag == 'hostnames':
                for hostname in self.parse_hostnames(xh):
                        nhost.add_hostname(hostname)
            elif xh.tag == 'ports':
                for port in self.parse_ports(xh):
                    nhost.add_service(port)
            elif xh.tag in ('status', 'address'): setattr(nhost, xh.tag, xh.attrib)
            #else: print "struct host unknown attr: %s value: %s" % (h.tag, h.get(h.tag))
        self._nmap_dict_report['hosts'].append(nhost)
        return nhost

    def parse_hostnames(self, xelement):
        hostnames = []
        for hname in xelement:
            if hname.tag == 'hostname':
                hostnames.append(hname.get('name'))
        return hostnames

    def parse_ports(self, xelement):
        ports = []
        for xservice in xelement:
            if xservice.tag == 'port':
                nport = NmapService(portid=xservice.get('portid'),
                                      protocol=xservice.get('protocol'),
                                      state=xservice.find('state').attrib,
                                      service=xservice.find('service').attrib)
                ports.append(nport)
        return ports
         
    def parse_runstats(self, xelement):
        for s in xelement:
            if s.tag == 'finished':
                self.endtime = s.get('time')
                self.elapsed = s.get('elapsed')
                self.summary = s.get('summary')
            elif s.tag == 'hosts':
                self.hosts_up = s.get('up')
                self.hosts_down = s.get('down')
                self.hosts_total = s.get('total')
            else: raise Exception('Unpexpected data structure for <runstats>')

    def get_hosts(self):
        return self._nmap_dict_report['hosts'] if self._nmap_dict_report.has_key('hosts') else None
