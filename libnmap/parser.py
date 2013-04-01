#!/usr/bin/env python
import xml.etree.ElementTree as ET
from StringIO import StringIO
from libnmap import NmapHost, NmapService

class NmapParser(object):
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
        xelement = cls.__format_element(scaninfo_data)
        return xelement.attrib

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
                setattr(nhost, xh.tag, xh.attrib)
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
                                      protocol=xelement.get('protocol'),
                                      state=xelement.find('state').attrib,
                                      service=xelement.find('service').attrib)
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
                raise Exception('Unpexpected data structure for <runstats>')

        return rdict

    @classmethod
    def __format_element(cls, elt_data):
        if isinstance(elt_data, str):
            try:
                xelement = ET.fromstring(elt_data)
            except:
                raise Exception("Error while trying to instanciate XML Element from string")
        elif ET.iselement(elt_data):
            xelement = elt_data
        else:
            raise Exception("Error while trying to parse supplied data: unsupported format")
        return xelement
