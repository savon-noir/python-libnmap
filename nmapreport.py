#!/usr/bin/env python 
import xml.etree.ElementTree as ET
from StringIO import StringIO

#<host starttime="1361737906" endtime="1361738040"><status state="up" reason="echo-reply"/>
#<address addr="74.207.244.221" addrtype="ipv4"/>
#<hostnames>
#<hostname name="scanme.nmap.org" type="user"/>
#<hostname name="scanme.nmap.org" type="PTR"/>
#</hostnames>
#<ports><extraports state="closed" count="996">
#<extrareasons reason="resets" count="996"/>
#</extraports>
#<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="53"/><service name="ssh" method="table" conf="3"/></port>
#<port protocol="tcp" portid="25"><state state="filtered" reason="admin-prohibited" reason_ttl="253" reason_ip="109.133.192.1"/><service name="smtp" method="table" conf="3"/></port>
#<port protocol="tcp" portid="80"><state state="open" reason="syn-ack" reason_ttl="51"/><service name="http" method="table" conf="3"/></port>
#<port protocol="tcp" portid="9929"><state state="open" reason="syn-ack" reason_ttl="53"/><service name="nping-echo" method="table" conf="3"/></port>
#</ports>
#<times srtt="177425" rttvar="1981" to="185349"/>
#</host>"

class NmapReport:
    def __init__(self, nmap_report=None, type='XML'):
        self._nmap_xml_report = nmap_report
        self._nmap_dict_report = {'hosts': []}

#<host starttime="1361738377" endtime="1361738377"><status state="up" reason="localhost-response"/>
#<address addr="127.0.0.1" addrtype="ipv4"/>
#<hostnames>
#<hostname name="localhost" type="user"/>
#<hostname name="localhost" type="PTR"/>
#</hostnames>
    def __struct_host(self, xelement):
    # parses out all host  xml element to create a NmapHost
        nhost = NmapHost()
        for h in xelement:
            if h.tag == 'ports': nhost.ports = self.__struct_ports(h)
            elif h.tag == 'hostnames': nhost.hostnames = self.__struct_hostnames(h)
            elif h.tag in ('status', 'address'): setattr(nhost, h.tag, h.attrib)
            else: print "struct host unknown attr: %s value: %s" % (h.tag, h.get(h.tag))
        self._nmap_dict_report['hosts'].append(nhost)

    def __struct_ports(self, xelement):
    # creates a service dictionary to be added in a NmapHost's ports attribute
        plist = []
        for p in xelement:
            pdict = {}
            if p.tag == 'port':
                pdict['port'] = p.get('portid')
                pdict['protocol'] = p.get('protocol')
                pdict.update(p.find('state').attrib)
                pdict.update(p.find('service').attrib)
                plist.append(pdict)
            else: print "struct ports unknown attr: %s value: %s" % (p.tag, p.get(p.tag))
        return plist

    def __struct_hostnames(self, xelement):
        hlist = []
        for p in xelement:
            if p.tag == 'hostname': hlist.append(p.get('name'))
        return hlist
                

    def parse(self):
        if not self._nmap_xml_report:
            raise Exception("No report to parse")
        tree = ET.parse(StringIO(self._nmap_xml_report))

        root = tree.getroot()
        self._nmap_dict_report[root.tag] = root.attrib
        for el in root:
            if el.tag == 'host': self.__struct_host(el)
            #else: self._nmap_dict_report[el.tag] = el.attrib
            #else: print "struct pparse unknown attr: %s value: %s" % (el.tag, el.get(el.tag))

    def get_hosts(self):
        return self._nmap_dict_report['hosts'] if self._nmap_dict_report.has_key('hosts') else None


class NmapHost:
    def __init__(self):
        self.hostnames = []
        self.address = {}
        self.status = {}
        # {'22': {'method': 'table', 'state': 'open', 'name': 'ssh', 'conf': '3', 'reason': 'syn-ack', 'reason_ttl': '64'}}
        self.ports = []

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
