#!/usr/bin/env python

class NmapHost(object):
    def __init__(self):
        self.starttime = ''
        self.endtime = ''
        self._hostnames = []
        self._status = {}
        self._address = {}
        self._services = []

    def __eq__(self,other):
        return  self._hostnames == other._hostnames  

    def __ne__(self,other):
        return  self._hostnames != other._hostnames

    def __repr__(self):
        return self.get_hostname()

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
        return plist.pop() if len(plist) else None
  
    def get_open_ports(self):
        return [ p.port for p in self._services if p.state == 'open' ]

class NmapService(object):
    def __init__(self, portid, protocol='tcp', state={}, service={}):
        self._portid = portid
        self._protocol = protocol
        self._state = state
        self._service = service

    def __eq__(self,other):
        return  self._portid == other._portid  and len(DictDiffer(self._state,other._state).changed()) == 0

    def __ne__(self,other):
        return  self._portid != other._portid  or len(DictDiffer(self._state,other._state).changed()) > 0

    def __repr__(self):
        return "%s(%s - %s - %s -%s)" % (self.__class__, self._portid, self._protocol, self._service, self._state)

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
    
    def getStateChanged(self,other):
        'return a set of keys for which the value has changed'
        return DictDiffer(self._state,other._state).changed() if self.port == other.port and self.protocol == other.protocol else ()

    def getStateUnChanged(self,other):
        'return a set of key for which the value hasn t changed value'
        return DictDiffer(self._state,other._state).unchanged() if self.port == other.port and self.protocol == other.protocol else ()
    
    def getServiceDetailsChanged(self,other):
        'return a set of keys for which the value has changed'
        return DictDiffer(self._service,other._service).changed() if self.port == other.port and self.protocol == other.protocol else ()
 
    def getServiceDetailsUnChanged(self,other):
        'return a set of key for which the value hasn t changed value'
        return DictDiffer(self._service,other._service).unchanged() if self.port == other.port and self.protocol == other.protocol else ()

    def get_banner(self):
        notrelevant = ['name', 'method', 'conf' ]
        b = ''
        if self._service and self._service['method'] == "probed":
            b = " ".join([ k + ": " + self._service[k] for k in self._service.keys() if k not in notrelevant ])
        return b


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
