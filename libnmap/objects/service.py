# -*- coding: utf-8 -*-
from libnmap.diff import NmapDiff
from libnmap.objects.os import CPE


class NmapService(object):
    """
        NmapService represents a nmap scanned service. Its id() is comprised
        of the protocol and the port.

        Depending on the scanning options, some additional details might be
        available or not. Like banner or extra datas from NSE (nmap scripts).
    """
    def __init__(self, portid, protocol='tcp', state=None,
                 service=None, owner=None, service_extras=None):
        """
            Constructor

            :param portid: port number
            :type portid: string
            :param protocol: protocol of port scanned (tcp, udp)
            :type protocol: string
            :param state: python dict describing the service status
            :type state: python dict
            :param service: python dict describing the service name and banner
            :type service: python dict
            :param service_extras: additional info about the tested service
            like scripts' data
        """
        try:
            self._portid = int(portid or -1)
        except (ValueError, TypeError):
            raise
        if self._portid < 0 or self._portid > 65535:
            raise ValueError

        self._protocol = protocol
        self._state = state if state is not None else {}
        self._service = service if service is not None else {}

        self._cpelist = []
        if 'cpelist' in self._service:
            for _cpe in self._service['cpelist']:
                _cpeobj = CPE(_cpe)
                self._cpelist.append(_cpeobj)

        self._owner = ''
        if owner is not None and 'name' in owner:
            self._owner = owner['name']

        self._reason = ''
        self._reason_ip = ''
        self._reason_ttl = ''
        self._servicefp = ''
        self._tunnel = ''

        if 'reason' in self._state:
            self._reason = self._state['reason']
        if 'reason_ttl' in self._state:
            self._reason_ttl = self._state['reason_ttl']
        if 'reason_ip' in self._state:
            self._reason_ip = self._state['reason_ip']

        if 'servicefp' in self._service:
            self._servicefp = self._service['servicefp']
        if 'tunnel' in self._service:
            self._tunnel = self._service['tunnel']

        self._service_extras = []
        if service_extras is not None:
            self._service_extras = service_extras

    def __eq__(self, other):
        """
            Compares two NmapService objects to see if they are the same or
            if one of them changed.

            :param other: NmapService

            :return: boolean
        """
        rval = False
        if(self.__class__ == other.__class__ and self.id == other.id):
            rval = (self.changed(other) == 0)
        return rval

    def __ne__(self, other):
        """
            Compares two NmapService objects to see if they are different
            if one of them changed.

            :param other: NmapService

            :return: boolean
        """
        rval = True
        if(self.__class__ == other.__class__ and self.id == other.id):
            rval = (self.changed(other) > 0)
        return rval

    def __repr__(self):
        return "{0}: [{1} {2}/{3} {4} ({5})]".format(self.__class__.__name__,
                                                     self.state,
                                                     str(self.port),
                                                     self.protocol,
                                                     self.service,
                                                     self.banner)

    def __hash__(self):
        return (hash(self.port) ^ hash(self.protocol) ^ hash(self.state) ^
                hash(self.reason) ^ hash(self.service) ^ hash(self.banner))

    def changed(self, other):
        """
            Checks if a NmapService is different from another.

            :param other: NmapService

            :return: boolean
        """
        return len(self.diff(other).changed())

    @property
    def port(self):
        """
            Accessor for port.

            :return: integer or -1
        """
        return self._portid

    @property
    def protocol(self):
        """
            Accessor for protocol

            :return: string
        """
        return self._protocol

    @property
    def state(self):
        """
            Accessor for service's state (open, filtered, closed,...)

            :return: string
        """
        return self._state['state'] if 'state' in self._state else None

    @property
    def reason(self):
        """
            Accessor for service's state reason (syn-ack, filtered,...)

            :return: string or empty if not applicable
        """
        return self._reason

    @property
    def reason_ip(self):
        """
            Accessor for service's state reason ip

            :return: string or empty if not applicable
        """
        return self._reason_ip

    @property
    def reason_ttl(self):
        """
            Accessor for service's state reason ttl

            :return: string or empty if not applicable
        """
        return self._reason_ttl

    @property
    def service(self):
        """
            Accessor for service name.

            :return: string or empty
        """
        return self._service['name'] if 'name' in self._service else ''

    @property
    def service_dict(self):
        """
            Accessor for service dictionary.

            :return: dict or None
        """
        return self._service

    def open(self):
        """
            Tells if the port was open or not

            :return: boolean
        """
        return 'state' in self._state and self._state['state'] == 'open'

    @property
    def owner(self):
        """
            Accessor for service owner if available
        """
        return self._owner

    @property
    def banner(self):
        """
            Accessor for the service's banner. Only available
            if the nmap option -sV or similar was used.

            :return: string
        """
        notrelevant = ['name', 'method', 'conf', 'cpelist',
                       'servicefp', 'tunnel']
        relevant = ['product', 'version', 'extrainfo']
        b = ''
        skeys = self._service.keys()
        if 'method' in self._service and self._service['method'] == "probed":
            for relk in relevant:
                if relk in skeys:
                    b += '{0}: {1} '.format(relk, self._service[relk])
            for mkey in skeys:
                if mkey not in notrelevant and mkey not in relevant:
                    b += '{0}: {1} '.format(mkey, self._service[mkey])
        return b.rstrip()

    @property
    def cpelist(self):
        """
            Accessor for list of CPE for this particular service
        """
        return self._cpelist

    @property
    def scripts_results(self):
        """
            Gives a python list of the nse scripts results.

            The dict key is the name (id) of the nse script and
            the value is the output of the script.

            :return: dict
        """
        scripts_dict = None
        try:
            scripts_dict = self._service_extras['scripts']
        except (KeyError, TypeError):
            pass
        return scripts_dict

    @property
    def servicefp(self):
        """
            Accessor for the service's fingerprint
            if the nmap option -sV or -A is used

            :return: string if available
        """
        return self._servicefp

    @property
    def tunnel(self):
        """
            Accessor for the service's tunnel type
            if applicable and available from scan
            results

            :return: string if available
        """
        return self._tunnel

    @property
    def id(self):
        """
            Accessor for the id() of the NmapService.

            This is used for diff()ing NmapService object via NmapDiff.

            :return: tuple
        """
        return "{0}.{1}".format(self.protocol, self.port)

    def get_dict(self):
        """
            Return a python dict representation of the NmapService object.

            This is used to diff() NmapService objects via NmapDiff.

            :return: dict
        """
        return ({'id': str(self.id), 'port': str(self.port),
                 'protocol': self.protocol, 'banner': self.banner,
                 'service': self.service, 'state': self.state,
                 'reason': self.reason})

    def diff(self, other):
        """
            Calls NmapDiff to check the difference between self and
            another NmapService object.

            Will return a NmapDiff object.

            This objects return python set() of keys describing the elements
            which have changed, were added, removed or kept unchanged.

            :return: NmapDiff object
        """
        return NmapDiff(self, other)
