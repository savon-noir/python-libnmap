#!/usr/bin/env python 
import xml.etree.ElementTree as ET
from StringIO import StringIO

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

    def __struct_host(self, xelement):
        nhost = NmapHost()
        for h in xelement:
            if h.tag == 'ports': nhost.ports = self.__struct_ports(h)
            elif h.tag == 'hostnames':
                for hname in h:
                    if hname.tag == 'hostname': nhost.add_hostname(hname.get('name'))
            elif h.tag in ('status', 'address'): setattr(nhost, h.tag, h.attrib)
            #else: print "struct host unknown attr: %s value: %s" % (h.tag, h.get(h.tag))
        self._nmap_dict_report['hosts'].append(nhost)

    def __struct_ports(self, xelement):
        plist = []
        for p in xelement:
            pdict = {}
            if p.tag == 'port':
                pdict['port'] = p.get('portid')
                pdict['protocol'] = p.get('protocol')
                pdict.update(p.find('state').attrib)
                pdict.update(p.find('service').attrib)
                plist.append(pdict)
            #else: print "struct ports unknown attr: %s value: %s" % (p.tag, p.get(p.tag))
        return plist

    def __struct_stats(self, xelement):
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

    def parse(self):
        if not self._nmap_xml_report:
            raise Exception("No report to parse")
        tree = ET.parse(StringIO(self._nmap_xml_report))

        root = tree.getroot()
        self._nmap_dict_report[root.tag] = root.attrib
        for el in root:
            if el.tag == 'host': self.__struct_host(el)
            elif el.tag == 'runstats': self.__struct_stats(el)
            #else: self._nmap_dict_report[el.tag] = el.attrib
            else: print "struct pparse unknown attr: %s value: %s" % (el.tag, el.get(el.tag))

    def get_hosts(self):
        return self._nmap_dict_report['hosts'] if self._nmap_dict_report.has_key('hosts') else None

class NmapHost:
    def __init__(self):
        self.hostnames = []
        self.starttime = ''
        self.endtime = ''
        self.status = {}
        self.address = {}
        # {'22': {'method': 'table', 'state': 'open', 'name': 'ssh', 'conf': '3', 'reason': 'syn-ack', 'reason_ttl': '64'}}
        self.ports = []

    def add_hostname(self, hostname):
        self.hostnames.append(hostname)

    def get_hostname(self):
        return self.hostnames[0] if len(self.hostnames) else self.get_ip()

    def get_ip(self):
        return self.address['addr']

    # uniqu() on returned array since udp and tcp port could be twice in the array
    def get_ports(self):
        return [ p['port'] for p in self.ports ]

    def get_port(self, portno, protocol='tcp'):
        plist = filter(lambda p: p['port'] == portno and p['protocol'] == protocol, self.ports)
        return plist.pop() if len(plist) else {}

    def get_open_ports(self):
        return [ p['port'] for p in self.ports if p['state'] == 'open' ]
