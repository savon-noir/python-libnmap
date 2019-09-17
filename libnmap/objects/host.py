# -*- coding: utf-8 -*-

from libnmap.diff import NmapDiff
from libnmap.objects.os import NmapOSFingerprint


class NmapHost(object):
    """
        NmapHost is a class representing a host object of NmapReport
    """
    def __init__(self, starttime='', endtime='', address=None, status=None,
                 hostnames=None, services=None, traceroute=None, extras=None):
        """
            NmapHost constructor
            :param starttime: unix timestamp of when the scan against
            that host started
            :type starttime: string
            :param endtime: unix timestamp of when the scan against
            that host ended
            :type endtime: string
            :param address: dict ie :{'addr': '127.0.0.1', 'addrtype': 'ipv4'}
            :param status: dict ie:{'reason': 'localhost-response',
                                    'state': 'up'}
            :return: NmapHost:
        """
        self._starttime = starttime
        self._endtime = endtime
        self._hostnames = hostnames if hostnames is not None else []
        self._status = status if status is not None else {}
        self._services = services if services is not None else []
        self._traceroute = traceroute if traceroute is not None else {}
        self._extras = extras if extras is not None else {}
        self._osfingerprinted = False
        self.os = None
        if 'os' in self._extras:
            self.os = NmapOSFingerprint(self._extras['os'])
            self._osfingerprinted = True
        else:
            self.os = NmapOSFingerprint({})

        self._ipv4_addr = None
        self._ipv6_addr = None
        self._mac_addr = None
        self._vendor = None
        for addr in address:
            if addr['addrtype'] == "ipv4":
                self._ipv4_addr = addr['addr']
            elif addr['addrtype'] == 'ipv6':
                self._ipv6_addr = addr['addr']
            elif addr['addrtype'] == 'mac':
                self._mac_addr = addr['addr']
            if 'vendor' in addr:
                self._vendor = addr['vendor']

        self._main_address = self._ipv4_addr or self._ipv6_addr or ''
        self._address = address

    def __eq__(self, other):
        """
            Compare eq NmapHost based on :

                - hostnames
                - address
                - if an associated services has changed

            :return: boolean
        """
        rval = False
        if(self.__class__ == other.__class__ and self.id == other.id):
            rval = (self.changed(other) == 0)
        return rval

    def __ne__(self, other):
        """
            Compare ne NmapHost based on:

                - hostnames
                - address
                - if an associated services has changed

            :return: boolean
        """
        rval = True
        if(self.__class__ == other.__class__ and self.id == other.id):
            rval = (self.changed(other) > 0)
        return rval

    def __repr__(self):
        """
            String representing the object
            :return: string
        """
        return "{0}: [{1} ({2}) - {3}]".format(self.__class__.__name__,
                                               self.address,
                                               " ".join(self._hostnames),
                                               self.status)

    def __hash__(self):
        """
            Hash is needed to be able to use our object in sets
            :return: hash
        """
        return (hash(self.status) ^ hash(self.address) ^
                hash(frozenset(self._services)) ^
                hash(frozenset(" ".join(self._hostnames))))

    def changed(self, other):
        """
            return the number of attribute who have changed
            :param other: NmapHost object to compare
            :return int
        """
        return len(self.diff(other).changed())

    @property
    def starttime(self):
        """
            Accessor for the unix timestamp of when the scan was started

            :return: string
        """
        return self._starttime

    @property
    def endtime(self):
        """
            Accessor for the unix timestamp of when the scan ended

            :return: string
        """
        return self._endtime

    @property
    def address(self):
        """
            Accessor for the IP address of the scanned host

            :return: IP address as a string
        """
        return self._main_address

    @address.setter
    def address(self, addrdict):
        """
            Setter for the address dictionnary.

            :param addrdict: valid dict is {'addr': '1.1.1.1',
                                            'addrtype': 'ipv4'}
        """
        if addrdict['addrtype'] == 'ipv4':
            self._ipv4_addr = addrdict['addr']
        elif addrdict['addrtype'] == 'ipv6':
            self._ipv6_addr = addrdict['addr']
        elif addrdict['addrtype'] == 'mac':
            self._mac_addr = addrdict['addr']
        if 'vendor' in addrdict:
            self._vendor = addrdict['vendor']

        self._main_address = self._ipv4_addr or self._ipv6_addr or ''
        self._address = addrdict

    @property
    def ipv4(self):
        """
            Accessor for the IPv4 address of the scanned host

            :return: IPv4 address as a string
        """
        return self._ipv4_addr or ''

    @property
    def mac(self):
        """
            Accessor for the MAC address of the scanned host

            :return: MAC address as a string
        """
        return self._mac_addr or ''

    @property
    def vendor(self):
        """
            Accessor for the vendor attribute of the scanned host

            :return: string (vendor) of empty string if no vendor defined
        """
        return self._vendor or ''

    @property
    def ipv6(self):
        """
            Accessor for the IPv6 address of the scanned host

            :return: IPv6 address as a string
        """
        return self._ipv6_addr or ''

    @property
    def status(self):
        """
            Accessor for the host's status (up, down, unknown...)

            :return: string
        """
        return self._status['state']

    @status.setter
    def status(self, statusdict):
        """
            Setter for the status dictionnary.

            :param statusdict: valid dict is {"state": "open",
                                              "reason": "syn-ack",
                                              "reason_ttl": "0"}
                                'state' is the only mandatory key.
        """
        self._status = statusdict

    def is_up(self):
        """
            method to determine if host is up or not

            :return: bool
        """
        rval = False
        if self.status == 'up':
            rval = True
        return rval

    @property
    def hostnames(self):
        """
            Accessor returning the list of hostnames (array of strings).

            :return: array of string
        """
        return self._hostnames

    @property
    def services(self):
        """
            Accessor for the array of scanned services for that host.

            An array of NmapService objects is returned.

            :return: array of NmapService
        """
        return self._services

    def get_ports(self):
        """
            Retrieve a list of the port used by each service of the NmapHost

            :return: list: of tuples (port,'proto') ie:[(22,'tcp'),(25, 'tcp')]
        """
        return [(p.port, p.protocol) for p in self._services]

    def get_open_ports(self):
        """
            Same as get_ports() but only for open ports

            :return: list: of tuples (port,'proto') ie:[(22,'tcp'),(25, 'tcp')]
        """
        return ([(p.port, p.protocol)
                for p in self._services if p.state == 'open'])

    def get_service(self, portno, protocol='tcp'):
        """
            :param portno: int the portnumber
            :param protocol='tcp': string ('tcp','udp')

            :return: NmapService or None
        """
        plist = [p for p in self._services if
                 p.port == portno and p.protocol == protocol]
        if len(plist) > 1:
            raise Exception("Duplicate services found in NmapHost object")
        return plist.pop() if len(plist) else None

    def get_service_byid(self, service_id):
        """
            Returns a NmapService by providing its id.

            The id of a nmap service is a python tupl made of (protocol, port)
        """
        rval = None
        for _tmpservice in self._services:
            if _tmpservice.id == service_id:
                rval = _tmpservice
        return rval

    def os_class_probabilities(self):
        """
            Returns an array of possible OS class detected during
            the OS fingerprinting.

            :return: Array of NmapOSClass objects
        """
        rval = []
        if self.os is not None:
            rval = self.os.osclasses
        return rval

    def os_match_probabilities(self):
        """
            Returns an array of possible OS match detected during
            the OS fingerprinting

            :return: array of NmapOSMatches objects
        """
        rval = []
        if self.os is not None:
            rval = self.os.osmatches
        return rval

    @property
    def os_fingerprinted(self):
        """
            Specify if the host has OS fingerprint data available

            :return: Boolean
        """
        return self._osfingerprinted

    @property
    def os_fingerprint(self):
        """
            Returns the fingerprint of the scanned system.

            :return: string
        """
        rval = ''
        if self.os is not None:
            rval = "\n".join(self.os.fingerprints)
        return rval

    def os_ports_used(self):
        """
            Returns an array of the ports used for OS fingerprinting

            :return: array of ports used: [{'portid': '22',
                                            'proto': 'tcp',
                                            'state': 'open'},]
        """
        rval = []
        try:
            rval = self._extras['os']['ports_used']
        except (KeyError, TypeError):
            pass
        return rval

    @property
    def tcpsequence(self):
        """
            Returns the difficulty to determine remotely predict
            the tcp sequencing.

            return: string
        """
        rval = ''
        try:
            rval = self._extras['tcpsequence']['difficulty']
        except (KeyError, TypeError):
            pass
        return rval

    @property
    def ipsequence(self):
        """
            Return the class of ip sequence of the remote hosts.

            :return: string
        """
        rval = ''
        try:
            rval = self._extras['ipidsequence']['class']
        except (KeyError, TypeError):
            pass
        return rval

    @property
    def uptime(self):
        """
            uptime of the remote host (if nmap was able to determine it)

            :return: string (in seconds)
        """
        rval = 0
        try:
            rval = int(self._extras['uptime']['seconds'])
        except (KeyError, TypeError):
            pass
        return rval

    @property
    def lastboot(self):
        """
            Since when the host was booted.

            :return: string
        """
        rval = ''
        try:
            rval = self._extras['uptime']['lastboot']
        except (KeyError, TypeError):
            pass
        return rval

    @property
    def distance(self):
        """
            Number of hops to host

            :return: int
        """
        rval = 0
        try:
            rval = int(self._extras['distance']['value'])
        except (KeyError, TypeError):
            pass
        return rval

    @property
    def scripts_results(self):
        """
            Scripts results specific to the scanned host

            :return: array of <script> dictionary
        """
        rval = {}
        try:
            rval = self._extras['hostscript']
        except (KeyError, TypeError):
            pass
        return rval

    @property
    def id(self):
        """
            id of the host. Used for diff()ing NmapObjects

            :return: string
        """
        return self.address

    @property
    def extraports_state(self):
        """
            dictionnary containing state and amount of extra ports scanned
            for which a common state, usually, closed was discovered.

            :return: dict with keys 'state' and 'count' or None
        """
        _xtrports = self._extras.get('extraports', None)

        if _xtrports is None:
            return None

        return {'state': _xtrports['state'], 'count': _xtrports['count']}

    @property
    def extraports_reasons(self):
        """
            dictionnary containing reasons why extra ports scanned
            for which a common state, usually, closed was discovered.

            :return: array of dict containing keys 'state' and 'count' or None
        """
        r = self._extras.get('extraports', {})

        if r is None:
            return None

        return r.get('reasons', None)

    def get_dict(self):
        """
            Return a dict representation of the object.

            This is needed by NmapDiff to allow comparaison

            :return dict
        """
        d = dict([("{0}::{1}".format(s.__class__.__name__, str(s.id)),
                   hash(s))
                 for s in self.services])

        d.update({'address': self.address, 'status': self.status,
                  'hostnames': " ".join(self._hostnames)})
        return d

    def diff(self, other):
        """
            Calls NmapDiff to check the difference between self and
            another NmapHost object.

            Will return a NmapDiff object.

            This objects return python set() of keys describing the elements
            which have changed, were added, removed or kept unchanged.

            :param other: NmapHost to diff with

            :return: NmapDiff object
        """
        return NmapDiff(self, other)

    @property
    def traceroute(self):
        """
            dictionary object of the traceroute data. Does not show
            localhost (or its ip) as the first entry, it is assumed

            :return: dict
        """

        return self._traceroute