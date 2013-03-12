#!/usr/bin/env python

class NmapHost:
    def __init__(self):
        self.starttime = ''
        self.endtime = ''
        self._hostnames = []
        self._status = {}
        self._address = {}
        self._services = []

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
    def status(self):
        return self._status
    @status.setter
    def status(self, statusdict):
        self._status = statusdict

    def add_hostname(self, hostname):
        self.hostnames.append(hostname)

    def add_service(self, nmapservice):
        v = False
        if isinstance(nmapservice, NmapService):
            self._services.append(nmapservice)
            v = True
        else:
            raise Exception("Object type should be NmapService for add_service")
        return v

    def get_hostname(self):
        return self._hostnames[0] if len(self._hostnames) else self.address

    def get_ports(self):
        return [ p.port for p in self._services ]

    def get_port(self, portno, protocol='tcp'):
        plist = [ p for p in self._services if p.port == portno and p.protocol == protocol ]
        return plist.pop() if len(plist) else {}
  
    def get_open_ports(self):
        return [ p.port for p in self._services if p.state == 'open' ]

class NmapService:
    def __init__(self, portid, protocol='tcp', state={}, service={}):
        self._portid = portid
        self._protocol = protocol
        self._state = state
        self._service = service

    @property
    def port(self):
        return self._portid

    @property
    def protocol(self):
        return self._protocol

    @property
    def state(self):
        return self._state['state']

    @property
    def service(self):
        return self._service['name'] if self._service.has_key('name') else ''

    def open(self):
        return True if self._state['state'] and self._state['state'] == 'open' else False

    def get_banner(self):
        notrelevant = ['name', 'method', 'conf' ]
        b = ''
        if self._service and self._service['method'] == "probed":
            b = " ".join([ k + ": " + self._service[k] for k in self._service.keys() if k not in notrelevant ])
        return b
