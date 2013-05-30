#!/usr/bin/env python
import xml.etree.ElementTree as ET
from libnmap.objects import NmapHost, NmapService, NmapReport


class NmapParser(object):
    @classmethod
    def parse(cls, nmap_data=None, data_type='XML'):
        """
            Generic class method of NmapParser class.
            The data to be parsed does not need to be a complete nmap
            scan report. You can possibly give <hosts>...</hosts>
            or <port> XML tags.

            :param nmap_data: any portion of nmap scan result.

            nmap_data should always be a string representing a part
            or a complete nmap scan report.

            :type nmap_data: string

            :param data_type: specifies the type of data to be parsed.
            :type data_type: string ("XML"|"JSON"|"YAML").

            As of today, only XML parsing is supported.

            :return: NmapObject (NmapHost, NmapService or NmapReport)
        """

        nmapobj = None
        if data_type == "XML":
            nmapobj = cls._parse_xml(nmap_data)
        else:
            raise NmapParserException("Unknown data type provided. "
                                      "Please check documentation for "
                                      "supported data types.")
        return nmapobj

    @classmethod
    def _parse_xml(cls, nmap_data=None):
        """
            Protected class method used to process a specific data type.
            In this case: XML. This method is called by cls.parse class
            method and receives nmap scan results data (in XML).

            :param nmap_data: any portion of nmap scan result can be given
            as argument. nmap_data should always be a string representing
            a part or a complete nmap scan report.
            :type nmap_data: string

            This method checks which portion of a nmap scan is given
            as argument.
            It could be:

                1. a full nmap scan report;
                2. a scanned host: <host> tag in a nmap scan report
                3. a scanned service: <port> tag
                4. a list of hosts: <hosts/> tag (TODO)
                5. a list of ports: <ports/> tag

            :return: NmapObject (NmapHost, NmapService or NmapReport)
                    or a list of NmapObject
        """

        if not nmap_data:
            raise NmapParserException("No report data to parse: please "
                                      "provide a valid XML nmap report")
        elif not isinstance(nmap_data, str):
            raise NmapParserException("wrong nmap_data type given as "
                                      "argument: cannot parse data")

        try:
            root = ET.fromstring(nmap_data)
        except:
            raise NmapParserException("Wrong XML structure: cannot parse data")

        nmapobj = None
        if root.tag == 'nmaprun':
            nmapobj = cls._parse_xml_report(root)
        elif root.tag == 'host':
            nmapobj = cls._parse_xml_host(root)
        elif root.tag == 'ports':
            nmapobj = cls._parse_xml_ports(root)
        elif root.tag == 'port':
            nmapobj = cls._parse_xml_port(root)
        else:
            raise NmapParserException("Unpexpected data structure for XML "
                                      "root node")
        return nmapobj

    @classmethod
    def _parse_xml_report(cls, root=None):
        """
            This method parses out a full nmap scan report from its XML root
            node: <nmaprun>.

            :param root: Element from xml.ElementTree (top of XML the document)
            :type root: Element

            :return: NmapReport object
        """

        nmap_scan = {'_nmaprun': {}, '_scaninfo': {},
                     '_hosts': [], '_runstats': {}}

        if root is None:
            raise NmapParserException("No root node provided to parse XML "
                                      "report")

        nmap_scan['_nmaprun'] = cls.__format_attributes(root)
        for el in root:
            if el.tag == 'scaninfo':
                nmap_scan['_scaninfo'] = cls.__parse_scaninfo(el)
            elif el.tag == 'host':
                nmap_scan['_hosts'].append(cls._parse_xml_host(el))
            elif el.tag == 'runstats':
                nmap_scan['_runstats'] = cls.__parse_runstats(el)
            #else:
            #    print "struct pparse unknown attr: {0} value: {1}".format(
            #        el.tag,
            #        el.get(el.tag))
        return NmapReport(nmap_scan)

    @classmethod
    def parse_fromstring(cls, nmap_data, data_type="XML"):
        """
            Call generic cls.parse() method and ensure that a string is
            passed on as argument. If not, an exception is raised.

            :param nmap_data: Same as for parse(), any portion of nmap scan.

            Reports could be passed as argument. Data type _must_ be a string.

            :type nmap_data: string

            :param data_type: Specifies the type of data passed on as argument.

            :return: NmapObject
        """

        if not isinstance(nmap_data, str):
            raise NmapParserException("bad argument type for "
                                      "xarse_fromstring(): should be a string")
        return cls.parse(nmap_data, data_type)

    @classmethod
    def parse_fromfile(cls, nmap_report_path, data_type="XML"):
        """
            Call generic cls.parse() method and ensure that a correct file
            path is given as argument. If not, an exception is raised.

            :param nmap_data: Same as for parse().

            Any portion of nmap scan reports could be passed as argument.

            Data type _must be a valid path to a file containing
            nmap scan results.

            :param data_type: Specifies the type of serialization in the file.

            :return: NmapObject
        """

        try:
            with open(nmap_report_path, 'r') as fileobj:
                fdata = fileobj.read()
                rval = cls.parse(fdata, data_type)
        except IOError:
            raise
        return rval

    @classmethod
    def parse_fromdict(cls, rdict):
        """
            Strange method which transforms a python dict
            representation of a NmapReport and turns it into an
            NmapReport object.
            Needs to be reviewed and possibly removed.

            :param rdict: python dict representation of an NmapReport
            :type rdict: dict

            :return: NmapReport
        """

        nreport = {}
        if rdict.keys()[0] == '__NmapReport__':
            r = rdict['__NmapReport__']
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
            nmapobj = NmapReport(nreport)
        return nmapobj

    @classmethod
    def __parse_scaninfo(cls, scaninfo_data):
        """
            Private method parsing a portion of a nmap scan result.
            Receives a <scaninfo> XML tag.

            :param scaninfo_data: <scaninfo> XML tag from a nmap scan
            :type scaninfo_data: xml.ElementTree.Element or a string

            :return: python dict representing the XML scaninfo tag
        """

        xelement = cls.__format_element(scaninfo_data)
        return cls.__format_attributes(xelement)

    @classmethod
    def _parse_xml_host(cls, scanhost_data):
        """
            Protected method parsing a portion of a nmap scan result.
            Receives a <host> XML tag representing a scanned host with
            its services.

            :param scaninfo_data: <host> XML tag from a nmap scan
            :type scaninfo_data: xml.ElementTree.Element or a string

            :return: NmapHost object
        """

        xelement = cls.__format_element(scanhost_data)

        _host_header = cls.__format_attributes(xelement)
        _hostnames = []
        _services = []
        _status = {}
        _address = {}
        _host_extras = {}
        extra_tags = ['uptime', 'distance', 'tcpsequence',
                      'ipidsequence', 'tcptssequence', 'times']
        for xh in xelement:
            if xh.tag == 'hostnames':
                for hostname in cls.__parse_hostnames(xh):
                    _hostnames.append(hostname)
            elif xh.tag == 'ports':
                for port in cls._parse_xml_ports(xh):
                    _services.append(port)
            elif xh.tag == 'status':
                _status = cls.__format_attributes(xh)
            elif xh.tag == 'address':
                _address = cls.__format_attributes(xh)
            elif xh.tag == 'os':
                _os_extra = cls.__parse_os_fingerprint(xh)
                _host_extras.update({'os': _os_extra})
            elif xh.tag in extra_tags:
                _host_extras[xh.tag] = cls.__format_attributes(xh)
            #else:
            #    print "struct host unknown attr: %s value: %s" %
            #           (h.tag, h.get(h.tag))
        _stime = ''
        _etime = ''
        if 'starttime' in _host_header:
            _stime = _host_header['starttime']
        if 'endime' in _host_header:
            _etime = _host_header['endtime']
        nhost = NmapHost(_stime,
                         _etime,
                         _address,
                         _status,
                         _hostnames,
                         _services,
                         _host_extras)
        return nhost

    @classmethod
    def __parse_hostnames(cls, scanhostnames_data):
        """
            Private method parsing the hostnames list within a <host> XML tag.

            :param scanhostnames_data: <hostnames> XML tag from a nmap scan
            :type scanhostnames_data: xml.ElementTree.Element or a string

            :return: list of hostnames
        """

        xelement = cls.__format_element(scanhostnames_data)
        hostnames = []
        for hname in xelement:
            if hname.tag == 'hostname':
                hostnames.append(hname.get('name'))
        return hostnames

    @classmethod
    def _parse_xml_ports(cls, scanports_data):
        """
            Protected method parsing the list of scanned services from
            a targeted host. This protected method cannot be called directly
            with a string. A <ports/> tag can be directly passed to parse()
            and the below method will be called and return a list of nmap
            scanned services.

            :param scanports_data: <ports> XML tag from a nmap scan
            :type scanports_data: xml.ElementTree.Element or a string

            :return: list of NmapService
        """

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
        """
            Protected method parsing a scanned service from a targeted host.
            This protected method cannot be called directly.
            A <port/> tag can be directly passed to parse() and the below
            method will be called and return a NmapService object
            representing the state of the service.

            :param scanport_data: <port> XML tag from a nmap scan
            :type scanport_data: xml.ElementTree.Element or a string

            :return: NmapService
        """

        xelement = cls.__format_element(scanport_data)

        _port = cls.__format_attributes(xelement)
        _portid = _port['portid'] if 'portid' in _port else None
        _protocol = _port['protocol'] if 'protocol' in _port else None

        _state = None
        _service = None
        _service_extras = []
        for xport in xelement:
            if xport.tag == 'state':
                _state = cls.__format_attributes(xport)
            elif xport.tag == 'service':
                _service = cls.__format_attributes(xport)
            elif xport.tag == 'script':
                _script_dict = cls.__format_attributes(xport)
                _service_extras.append(_script_dict)

        if(_portid is None or _protocol is None
                or _state is None or _service is None):
            raise NmapParserException("XML <port> tag is incomplete. One "
                                      "of the following tags is missing: "
                                      "portid, protocol state or service.")

        nport = NmapService(_portid,
                            _protocol,
                            _state,
                            _service,
                            _service_extras)
        return nport

    @classmethod
    def __parse_os_fingerprint(cls, os_data):
        """
            Private method parsing the data from an OS fingerprint (-O).
            Contents of <os> is returned as a dict.

            :param os_data: portion of XML describing the results of the
            os fingerprinting attempt
            :type os_data: xml.ElementTree.Element or a string

            :return: python dict representing the XML os tag
        """
        rdict = {}
        xelement = cls.__format_element(os_data)

        os_class_probability = []
        os_match_probability = []
        os_ports_used = []
        os_fp = {}
        for xos in xelement:
            if xos.tag == 'osclass':
                os_class_proba = cls.__format_attributes(xos)
                os_class_probability.append(os_class_proba)
            elif xos.tag == 'osmatch':
                os_match_proba = cls.__format_attributes(xos)
                os_match_probability.append(os_match_proba)
            elif xos.tag == 'portused':
                os_portused = cls.__format_attributes(xos)
                os_ports_used.append(os_portused)
            elif xos.tag == 'osfingerprint':
                os_fp = cls.__format_attributes(xos)

        rdict['osmatch'] = os_match_probability
        rdict['osclass'] = os_class_probability
        rdict['ports_used'] = os_ports_used
        rdict['osfingerprint'] = os_fp['fingerprint']

        return rdict

    @classmethod
    def __parse_runstats(cls, scanrunstats_data):
        """
            Private method parsing a portion of a nmap scan result.
            Receives a <runstats> XML tag.

            :param scanrunstats_data: <runstats> XML tag from a nmap scan
            :type scanrunstats_data: xml.ElementTree.Element or a string

            :return: python dict representing the XML runstats tag
        """

        xelement = cls.__format_element(scanrunstats_data)

        rdict = {}
        for xmltag in xelement:
            if xmltag.tag in ['finished', 'hosts']:
                rdict[xmltag.tag] = cls.__format_attributes(xmltag)
            else:
                raise NmapParserException("Unpexpected data structure "
                                          "for <runstats>")

        return rdict

    @staticmethod
    def __format_element(elt_data):
        """
            Private method which ensures that a XML portion to be parsed is
            of type xml.etree.ElementTree.Element.
            If elt_data is a string, then it is converted to an
            XML Element type.

            :param elt_data: XML Element to be parsed or string
            to be converted to a XML Element

            :return: Element
        """
        if isinstance(elt_data, str):
            try:
                xelement = ET.fromstring(elt_data)
            except:
                raise NmapParserException("Error while trying "
                                          "to instanciate XML Element from "
                                          "string {0}".format(elt_data))
        elif ET.iselement(elt_data):
            xelement = elt_data
        else:
            raise NmapParserException("Error while trying to parse supplied "
                                      "data: unsupported format")
        return xelement

    @staticmethod
    def __format_attributes(elt_data):
        """
            Private method which converts a single XML tag to a python dict.
            It also checks that the elt_data given as argument is of type
            xml.etree.ElementTree.Element

            :param elt_data: XML Element to be parsed or string
            to be converted to a XML Element

            :return: Element
        """

        rval = {}
        if not ET.iselement(elt_data):
            raise NmapParserException("Error while trying to parse supplied "
                                      "data attributes: format is not XML or "
                                      "XML tag is empty")
        try:
            for dkey in elt_data.keys():
                rval[dkey] = elt_data.get(dkey)
                if rval[dkey] is None:
                    raise NmapParserException("Error while trying to build-up "
                                              "element attributes: empty "
                                              "attribute {0}".format(dkey))
        except:
            raise
        return rval


class NmapParserException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
