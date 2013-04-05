#!/usr/bin/env python
import os
import xml.etree.ElementTree as ET
from StringIO import StringIO
from libnmap import NmapHost, NmapService

class NmapParser(object):
    @classmethod
    def parse(cls, nmap_data=None, type='XML'):
        nmap_scan = { 'nmaprun': {}, 'scaninfo': {}, 'hosts': [], 'runstats': {} }
        if not nmap_data:
            raise NmapParserException("No report data to parse: please provide a file")

        try:
            if isinstance(nmap_data, str):
                tree = ET.parse(StringIO(nmap_data))
            elif isinstance(nmap_data, file):
                tree = ET.parse(nmap_data)
        except:
            raise

        root = tree.getroot()
        if root.tag == 'nmaprun':
                nmap_scan['nmaprun'] = cls.__format_attributes(root)
        else:
            raise NmapParserException('Unpexpected data structure for XML root node')
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
    def parse_fromstring(cls, nmap_data, type="XML"):
        return cls.parse(nmap_data, type)

    @classmethod
    def parse_fromfile(cls, nmap_report_path, type="XML"):
        if os.path.exists(nmap_report_path):
            fd = open(nmap_report_path, 'r')
            r = cls.parse(fd, type)
            fd.close()
        else:
            raise NmapParserException("Nmap data file could not be found or permissions were not set correctly")
        return r

    @classmethod
    def parse_scaninfo(cls, scaninfo_data):
        xelement = cls.__format_element(scaninfo_data)
        return cls.__format_attributes(xelement)

    @classmethod
    def parse_host(cls, scanhost_data):
        xelement = cls.__format_element(scanhost_data)

        nhost = NmapHost()
        for xh in xelement:
            if xh.tag == 'hostnames':
                for hostname in cls.parse_hostnames(xh):
                        nhost.add_hostname(hostname)
            elif xh.tag == 'ports':
                for port in cls.parse_ports(xh):
                    nhost.add_service(port)
            elif xh.tag in ('status', 'address'):
                setattr(nhost, xh.tag, cls.__format_attributes(xh))
            #else: print "struct host unknown attr: %s value: %s" % (h.tag, h.get(h.tag))
        return nhost

    @classmethod
    def parse_hostnames(cls, scanhostnames_data):
        xelement = cls.__format_element(scanhostnames_data)

        hostnames = []
        for hname in xelement:
            if hname.tag == 'hostname':
                hostnames.append(hname.get('name'))
        return hostnames

    @classmethod
    def parse_ports(cls, scanports_data):
        xelement = cls.__format_element(scanports_data)

        ports = []
        for xservice in xelement:
            if xservice.tag == 'port':
                nport = cls.parse_port(xservice)
                ports.append(nport)
            #else: print "struct port unknown attr: %s value: %s" % (h.tag, h.get(h.tag))
        return ports

    @classmethod
    def parse_port(cls, scanport_data):
        xelement = cls.__format_element(scanport_data)

        nport = NmapService(portid=xelement.get('portid'),
                            protocol=xelement.get('protocol'))

        nport.add_state(cls.__format_attributes(xelement.find('state')))
        if not nport.state:
            raise NmapParserException("Service state is not known or could not be parsed")

        nport.add_service(cls.__format_attributes(xelement.find('service')))
        if not nport.service:
            raise NmapParserException("Service name is not known or could not be parsed")

        return nport

    @classmethod 
    def parse_runstats(cls, scanrunstats_data):
        xelement = cls.__format_element(scanrunstats_data)

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
            else:
                raise NmapParserException('Unpexpected data structure for <runstats>')

        return rdict

    @staticmethod
    def __format_element(elt_data):
        if isinstance(elt_data, str):
            try:
                xelement = ET.fromstring(elt_data)
            except:
                raise NmapParserException("Error while trying to instanciate XML Element from string {0}".format(elt_data))
        elif ET.iselement(elt_data):
            xelement = elt_data
        else:
            raise NmapParserException("Error while trying to parse supplied data: unsupported format")
        return xelement

    @staticmethod
    def __format_attributes(elt_data):
        r = {}
        if not ET.iselement(elt_data):
            raise NmapParserException("Error while trying to parse supplied data attributes: format is not XML")
        try:
            for k in elt_data.keys():
                r[k] = elt_data.get(k)
                if r[k] is None:
                    raise NmapParserException("Error while trying to build-up element attributes")
        except:
            raise
        return r

class NmapParserException(Exception):
    def __init__(self, msg):
        self.msg = msg
