#!/usr/bin/env python
import os
import xml.etree.ElementTree as ET
from StringIO import StringIO
from libnmap.common import NmapHost, NmapService
from libnmap.report import NmapReport


class NmapParser(object):
    @classmethod
    def parse(cls, nmap_data=None, data_type='XML'):
        nmapobj = None
        if data_type == "XML":
            nmapobj = cls.parse_xml(nmap_data)
        return nmapobj

    @classmethod
    def parse_xml(cls, nmap_data=None, data_type='XML'):
        nmapobj = None
        if not nmap_data:
            raise NmapParserException("No report data to parse: \
                                       please provide a file")

        try:
            if isinstance(nmap_data, str):
                tree = ET.parse(StringIO(nmap_data))
            elif isinstance(nmap_data, file):
                tree = ET.parse(nmap_data)
        except:
            raise NmapParserException("Wrong XML structure: cannot parse data")

        root = tree.getroot()
        if root.tag == 'nmaprun':
            nmapobj = cls._parse_xml_report(root)
        elif root.tag == 'host':
            nmapobj = cls._parse_xml_host(root)
        elif root.tag == 'ports':
            nmapobj = cls._parse_xml_ports(root)
        elif root.tag == 'port':
            nmapobj = cls._parse_xml_port(root)
        else:
            raise NmapParserException("Unpexpected data structure for XML \
                                       root node")
        return nmapobj

    # return NmapReport()
    @classmethod
    def _parse_xml_report(cls, root=None):
        nmap_scan = {'_nmaprun': {}, '_scaninfo': {},
                     '_hosts': [], '_runstats': {}}

        if root is None:
            raise NmapParserException("No root node provided to parse XML \
                                       report")

        nmap_scan['_nmaprun'] = cls.__format_attributes(root)
        for el in root:
            if el.tag == 'scaninfo':
                nmap_scan['_scaninfo'] = cls._parse_scaninfo(el)
            elif el.tag == 'host':
                nmap_scan['_hosts'].append(cls._parse_xml_host(el))
            elif el.tag == 'runstats':
                nmap_scan['_runstats'] = cls._parse_runstats(el)
            #else:
            #    print "struct pparse unknown attr: {0} value: {1}".format(
            #        el.tag,
            #        el.get(el.tag))
        return NmapReport('dummy', nmap_scan)

    @classmethod
    def parse_fromstring(cls, nmap_data, data_type="XML"):
        return cls.parse(nmap_data, data_type)

    @classmethod
    def parse_fromfile(cls, nmap_report_path, data_type="XML"):
        if os.path.exists(nmap_report_path):
            fd = open(nmap_report_path, 'r')
            r = cls.parse(fd, data_type)
            fd.close()
        else:
            raise NmapParserException("Nmap data file could not be found \
                                       or permissions were not set correctly")
        return r

    @classmethod
    def parse_fromdict(cls, rdict):
        nreport = {}
        if rdict.keys()[0] == '__NmapReport__':
            r = rdict['__NmapReport__']
            nreport['_name'] = r['_name']
            nreport['_runstats'] = r['_runstats']
            nreport['_scaninfo'] = r['_scaninfo']
            nreport['_nmaprun'] = r['_nmaprun']
            hlist = []
            for h in r['_hosts']:
                slist = []
                for s in h['__NmapHost__']['_services']:
                    cname = '__NmapService__'
                    slist.append(NmapService(portid=s[cname]['_portid'],
                                             protocol=s[cname]['_protocol'],
                                             state=s[cname]['_state'],
                                             service=s[cname]['_service']))

                nh = NmapHost(starttime=h['__NmapHost__']['_starttime'],
                              endtime=h['__NmapHost__']['_endtime'],
                              address=h['__NmapHost__']['_address'],
                              status=h['__NmapHost__']['_status'],
                              hostnames=h['__NmapHost__']['_hostnames'],
                              services=slist)
                hlist.append(nh)
            nreport['_hosts'] = hlist
        return nreport

    @classmethod
    def _parse_scaninfo(cls, scaninfo_data):
        xelement = cls.__format_element(scaninfo_data)
        return cls.__format_attributes(xelement)

    @classmethod
    def _parse_xml_host(cls, scanhost_data):
        xelement = cls.__format_element(scanhost_data)

        nhost = NmapHost()
        for xh in xelement:
            if xh.tag == 'hostnames':
                for hostname in cls._parse_hostnames(xh):
                    nhost.add_hostname(hostname)
            elif xh.tag == 'ports':
                for port in cls._parse_xml_ports(xh):
                    nhost.add_service(port)
            elif xh.tag in ('status', 'address'):
                setattr(nhost, xh.tag, cls.__format_attributes(xh))
            #else:
            #    print "struct host unknown attr: %s value: %s" %
            #           (h.tag, h.get(h.tag))
        return nhost

    @classmethod
    def _parse_hostnames(cls, scanhostnames_data):
        xelement = cls.__format_element(scanhostnames_data)
        hostnames = []
        for hname in xelement:
            if hname.tag == 'hostname':
                hostnames.append(hname.get('name'))
        return hostnames

    @classmethod
    def _parse_xml_ports(cls, scanports_data):
        xelement = cls.__format_element(scanports_data)

        ports = []
        for xservice in xelement:
            if xservice.tag == 'port':
                nport = cls._parse_xml_port(xservice)
                ports.append(nport)
            #else:
            #    print "struct port unknown attr: %s value: %s" %
            #           (h.tag, h.get(h.tag))
        return ports

    @classmethod
    def _parse_xml_port(cls, scanport_data):
        xelement = cls.__format_element(scanport_data)

        nport = NmapService(portid=xelement.get('portid'),
                            protocol=xelement.get('protocol'))

        nport.add_state(cls.__format_attributes(xelement.find('state')))
        if not nport.state:
            raise NmapParserException("Service state is not known \
                                       or could not be parsed")

        nport.add_service(cls.__format_attributes(xelement.find('service')))
        if not nport.service:
            raise NmapParserException("Service name is not known \
                                       or could not be parsed")

        return nport

    @classmethod
    def _parse_runstats(cls, scanrunstats_data):
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
                raise NmapParserException('Unpexpected data structure \
                                           for <runstats>')

        return rdict

    @staticmethod
    def __format_element(elt_data):
        if isinstance(elt_data, str):
            try:
                xelement = ET.fromstring(elt_data)
            except:
                raise NmapParserException("Error while trying \
                                           to instanciate XML Element from \
                                           string {0}".format(elt_data))
        elif ET.iselement(elt_data):
            xelement = elt_data
        else:
            raise NmapParserException("Error while trying to parse supplied \
                                       data: unsupported format")
        return xelement

    @staticmethod
    def __format_attributes(elt_data):
        r = {}
        if not ET.iselement(elt_data):
            raise NmapParserException("Error while trying to parse supplied \
                                       data attributes: format is not XML")
        try:
            for k in elt_data.keys():
                r[k] = elt_data.get(k)
                if r[k] is None:
                    raise NmapParserException("Error while trying to build-up \
                                               element attributes")
        except:
            raise
        return r


class NmapParserException(Exception):
    def __init__(self, msg):
        self.msg = msg
