#!/usr/bin/env python
from libnmap.diff import NmapDiff


class NmapHost(object):
    def __init__(self, starttime='', endtime='', address=None, status=None,
                 hostnames=None, services=None):
        self._starttime = starttime
        self._endtime = endtime
        self._hostnames = hostnames if hostnames is not None else []
        self._status = status if status is not None else {}
        self._address = address if address is not None else {}
        self._services = services if services is not None else []

    def __eq__(self, other):
        return (self._hostnames == other._hostnames and
                self.address == other.address and self.changed(other) == 0)

    def __ne__(self, other):
        return ((self._hostnames != other._hostnames or
                self.address != other.address) and self.changed(other))

    def __repr__(self):
        return "{0}: [{1} ({2}) - {3}]".format(self.__class__.__name__,
                                               self.address,
                                               " ".join(self._hostnames),
                                               self.status)

    def __hash__(self):
        return (hash(self.status) ^ hash(self.address) ^
                hash(frozenset(self._services)) ^
                hash(frozenset(" ".join(self._hostnames))))

    def changed(self, other):
        return len(self.diff(other).changed())

    @property
    def hostnames(self):
        return self._hostnames

    @property
    def services(self):
        return self._services

    @property
    def address(self):
        return self._address['addr']

    @address.setter
    def address(self, addrdict):
        self._address = addrdict

    @property
    def hostname(self):
        return self._hostnames[0] if len(self._hostnames) else self.address

    @property
    def status(self):
        return self._status['state']

    @status.setter
    def status(self, statusdict):
        self._status = statusdict

    @property
    def starttime(self):
        return self._starttime

    @property
    def endtime(self):
        return self._endtime

    def add_hostname(self, hostname):
        self._hostnames.append(hostname)

    def add_service(self, nmapservice):
        v = False
        if isinstance(nmapservice, NmapService):
            self._services.append(nmapservice)
            v = True
        else:
            raise Exception("Object type should be NmapService \
                            for add_service")
        return v

    def get_ports(self):
        return [(p.port, p.protocol) for p in self._services]

    def get_open_ports(self):
        return ([(p.port, p.protocol)
                for p in self._services if p.state == 'open'])

    def get_service(self, portno, protocol='tcp'):
        plist = [p for p in self._services if
                 p.port == portno and p.protocol == protocol]
        return plist.pop() if len(plist) else None

    def get_service_byid(self, id):
        service = [s for s in self.service if s.id() == id]
        if len(service) > 1:
            raise Exception("Duplicate services found in NmapHost object")

        return service.pop() if len(service) == 1 else None

    @property
    def id(self):
        return self.address

    def get_dict(self):
        d = dict([("%s.%s" % (s.__class__.__name__,
                   str(s.id)), hash(s)) for s in self.services])
        d.update({'address': self.address, 'status': self.status,
                  'hostnames': " ".join(self._hostnames)})
        return d

    def diff(self, other):
        return NmapDiff(self, other)


class NmapService(object):
    def __init__(self, portid, protocol='tcp', state=None, service=None):
        try:
            self._portid = int(portid or -1)
        except (ValueError, TypeError):
            raise
        if self._portid < 0 or self._portid > 65535:
            raise ValueError

        self._protocol = protocol
        self._state = state if state is not None else {}
        self._service = service if service is not None else {}

    def __eq__(self, other):
        return (self.id == other.id and self.changed(other) == 0)

    def __ne__(self, other):
        return (self.id != other.id or self.changed(other))

    def __repr__(self):
        return "{0}: [{1} {2}/{3} {4} ({5})]".format(self.__class__.__name__,
                                                     self.state,
                                                     str(self.port),
                                                     self.protocol,
                                                     self.service,
                                                     self.banner)

    def __hash__(self):
        return (hash(self.port) ^ hash(self.protocol) ^ hash(self.state) ^
                hash(self.service) ^ hash(self.banner))

    def changed(self, other):
        return len(self.diff(other).changed())

    @property
    def id(self):
        return hash(self.port) ^ hash(self.protocol)

    @property
    def port(self):
        return self._portid

    @property
    def protocol(self):
        return self._protocol

    @property
    def state(self):
        return self._state['state'] if 'state' in self._state else None

    def add_state(self, state={}):
        self._state = state

    @property
    def service(self):
        return self._service['name'] if 'name' in self._service else None

    def add_service(self, service={}):
        self._service = service

    def open(self):
        return (True
                if self._state['state'] and self._state['state'] == 'open'
                else False)

    @property
    def banner(self):
        notrelevant = ['name', 'method', 'conf']
        b = ''
        if self._service and self._service['method'] == "probed":
            b = " ".join([k + ": " + self._service[k]
                          for k in self._service.keys()
                              if k not in notrelevant])
        return b

    def get_dict(self):
        return ({'id': self.id, 'port': str(self.port),
                'protocol': self.protocol, 'banner': self.banner,
                'service': self.service, 'state': self.state})

    def diff(self, other):
        return NmapDiff(self, other)
