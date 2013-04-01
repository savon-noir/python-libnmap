#!/usr/bin/env python
import xml.etree.ElementTree as ET
from StringIO import StringIO
from libnmap import NmapHost, NmapService

class NmapParser(object):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, nmap_xml_report=None, type='XML'):
        nmap_scan = { 'nmaprun': {}, 'scaninfo': {}, 'hosts': [], 'runstats': {} }
        if not nmap_xml_report:
            raise Exception("No report to parse")

        try:
            tree = ET.parse(StringIO(nmap_xml_report))
        except:
            raise

        root = tree.getroot()
        if root.tag == 'nmaprun':
                nmap_scan['nmaprun'] = root.attrib
        else:
            raise Exception('Unpexpected data structure for XML root node')
        for el in root:
            if el.tag == 'scaninfo':
                nmap_scan['scaninfo'] = cls.parse_scaninfo(el)
            elif el.tag == 'host':
                nmap_scan['hosts'].append(cls.parse_host(el))
            elif el.tag == 'runstats':
                nmap_scan['runstats'] = cls.parse_runstats(el)
            #else: print "struct pparse unknown attr: %s value: %s" % (el.tag, el.get(el.tag))
        return nmap_scan

    @classmethod
    def parse_scaninfo(cls, scaninfo_data):
        if isinstance(scaninfo_data, str):
            try:
                xelement = ET.fromstring(scaninfo_data)
            except:
                raise Exception("Error while trying to instanciate XML Element from string")
        elif isintance(scaninfo_data, ET.Element):
            xelement = scaninfo_data
        else:
            raise Exception("Error while trying to parse supplied data: unsupported format")

        return xelement.attrib

    @classmethod
    def parse_host(cls, scanhost_data):
        if isinstance(scanhost_data, str):
            try:
                xelement = ET.fromstring(scanhost_data)
            except:
                raise Exception("Error while trying to instanciate NmapHost XML Element from string")
        elif isintance(scanhost_data, ET.Element):
            xelement = scanhost_data
        else:
            raise Exception("Error while trying to parse supplied data: unsupported format")

        nhost = NmapHost()
        for xh in xelement:
            if xh.tag == 'hostnames':
                for hostname in cls.parse_hostnames(xh):
                        nhost.add_hostname(hostname)
            elif xh.tag == 'ports':
                for port in cls.parse_ports(xh):
                    nhost.add_service(port)
            elif xh.tag in ('status', 'address'):
                setattr(nhost, xh.tag, xh.attrib)
            #else: print "struct host unknown attr: %s value: %s" % (h.tag, h.get(h.tag))
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
            #else: print "struct port unknown attr: %s value: %s" % (h.tag, h.get(h.tag))
        return ports
         
    def parse_runstats(self, xelement):
        rdict = {'finished': {}, 'hosts': {}}
        for s in xelement:
            if s.tag == 'finished':
                rdict[s.tag]['time'] = s.get('time')
                rdict[s.tag]['elapsed'] = s.get('elapsed')
                rdict[s.tag]['summary'] = s.get('summary')
            elif s.tag == 'hosts':
                rdict[s.tag]['up'] = s.get('up')
                rdict[s.tag]['down'] = s.get('down')
                rdict[s.tag]['total'] = s.get('total')
            else: raise Exception('Unpexpected data structure for <runstats>')

        return rdict

    def get_hosts(self):
        return self._hosts

    @property
    def endtime(self):
        return self._runstats['finished']['time']

    @property
    def summary(self):
        return self._runstats['finished']['summary']

    @property
    def elapsed(self):
        return self._runstats['finished']['elapsed']

    def get_parsed_data(self):
        parsed_data = { 'nmaprun': self._nmaprun,
                        'scaninfo': self._scaninfo,
                        'hosts': self._hosts, 
                        'runstats': self._runstats,
        }
        return parsed_data
