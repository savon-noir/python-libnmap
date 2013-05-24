#!/usr/bin/env python
from libnmap.diff import NmapDiff


class NmapHost(object):
    """
        NmapHost is a class representing a host object of NmapReport

        :todo: add ipsequence parsing (accessor implemented)
    """
    def __init__(self, starttime='', endtime='', address=None, status=None,
                 hostnames=None, services=None, extras=None):
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
        self._address = address if address is not None else {}
        self._services = services if services is not None else []
        self._extras = extras if extras is not None else {}

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
        return self._address['addr']

    @address.setter
    def address(self, addrdict):
        """
            Setter for the address dictionnary.

            :param addrdict: valid dict is {'addr': '1.1.1.1',
                                            'addrtype': 'ipv4'}
        """
        self._address = addrdict

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

            Example [{'accuracy': '96', 'osfamily': 'embedded',
                      'type': 'WAP', 'vendor': 'Netgear'}, {...}]

            :return: dict describing the OS class detected and the accuracy
        """
        rval = []
        try:
            rval = self._extras['os']['osclass']
        except (KeyError, TypeError):
            pass
        return rval

    def os_match_probabilities(self):
        """
            Returns an array of possible OS match detected during
            the OS fingerprinting

            :return: dict describing the OS version detected and the accuracy
        """

        rval = []
        try:
            rval = self._extras['os']['osmatch']
        except (KeyError, TypeError):
            pass
        return rval

    @property
    def os_fingerprint(self):
        """
            Returns the fingerprint of the scanned system.

            :return: string
        """
        rval = ''
        try:
            rval = self._extras['os']['osfingerprint']
        except (KeyError, TypeError):
            pass
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
            rval = self._extras['ports_used']
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
    def id(self):
        """
            id of the host. Used for diff()ing NmapObjects

            :return: string
        """
        return self.address

    def get_dict(self):
        """
            Return a dict representation of the object.

            This is needed by NmapDiff to allow comparaison

            :return dict
        """
        d = dict([("%s::%s" % (s.__class__.__name__, str(s.id)),
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


class NmapService(object):
    """
        NmapService represents a nmap scanned service. Its id() is comprised
        of the protocol and the port.

        Depending on the scanning options, some additional details might be
        available or not. Like banner or extra datas from NSE (nmap scripts).
    """
    def __init__(self, portid, protocol='tcp', state=None,
                 service=None, service_extras=None):
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
                hash(self.service) ^ hash(self.banner))

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
    def service(self):
        """
            Accessor for service dictionnary.

            :return: dict or None
        """
        return self._service['name'] if 'name' in self._service else None

    def open(self):
        """
            Tells if the port was open or not

            :return: boolean
        """
        return 'state' in self._state and self._state['state'] == 'open'

    @property
    def banner(self):
        """
            Accessor for the service's banner. Only available
            if the nmap option -sV or similar was used.

            :return: string
        """
        notrelevant = ['name', 'method', 'conf']
        b = ''
        if 'method' in self._service and self._service['method'] == "probed":
            b = " ".join([k + ": " + self._service[k]
                          for k in self._service.keys()
                              if k not in notrelevant])
        return b

    def scripts_results(self):
        """
            Gives a python dictionary of the nse scripts results.

            The dict key is the name (id) of the nse script and
            the value is the output of the script.

            :return: dict
        """
        scripts_dict = None
        try:
            scripts_dict = dict([(bdct['id'], bdct['output'])
                                 for bdct in self._service_extras])
        except (KeyError, TypeError):
            pass
        return scripts_dict

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
                 'service': self.service, 'state': self.state})

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


class NmapReport(object):
    """
        NmapReport is the usual interface for the end user to
        read scans output.

        A NmapReport as the following structure:

        - Scan headers data
        - A list of scanned hosts (NmapReport.hosts)
        - Scan footer data

        It is to note that each NmapHost comprised in NmapReport.hosts array
        contains also a list of scanned services (NmapService object).

        This means that if NmapParser.parse*() is the input interface for the
        end user of the lib. NmapReport is certainly the output interface for
        the end user of the lib.
    """
    def __init__(self, raw_data=None):
        """
            Constructor for NmapReport object.

            This is usually called by the NmapParser module.
        """
        self._nmaprun = {}
        self._scaninfo = {}
        self._hosts = []
        self._runstats = {}
        if raw_data is not None:
            self.__set_raw_data(raw_data)

    def save(self, backend):
        """
            This method gets a NmapBackendPlugin representing the backend.

            :param backend: libnmap.plugins.PluginBackend object.

            Object created by BackendPluginFactory and enabling nmap reports
            to be saved/stored in any type of backend implemented in plugins.

            The primary key of the stored object is returned.

            :return: integer
        """
        if backend is not None:
            #do stuff
            _id = backend.insert(self)
        else:
            raise RuntimeError
        return _id

    def diff(self, other):
        """
            Calls NmapDiff to check the difference between self and
            another NmapReport object.

            Will return a NmapDiff object.

            :return: NmapDiff object
            :todo: remove is_consistent approach, diff() should be generic.
        """
        if self.is_consistent() and other.is_consistent():
            _rdiff = NmapDiff(self, other)
        else:
            _rdiff = set()
        return _rdiff

    @property
    def started(self):
        """
            Accessor returning a unix timestamp of when the scan was started.

            :return: integer
        """
        rval = -1
        try:
            s_start = self._nmaprun['start']
            rval = int(s_start)
        except(KeyError, TypeError, ValueError):
            pass
        return rval

    @property
    def commandline(self):
        """
            Accessor returning the full nmap command line fired.

            :return: string
        """
        return self._nmaprun['args']

    @property
    def version(self):
        """
            Accessor returning the version of the
            nmap binary used to perform the scan.

            :return: string
        """
        return self._nmaprun['version']

    @property
    def scan_type(self):
        """
            Accessor returning a string which identifies what type of scan
            was launched (syn, ack, tcp,...).

            :return: string
        """
        return self._scaninfo['type']

    @property
    def hosts(self):
        """
            Accessor returning an array of scanned hosts.

            Scanned hosts are NmapHost objects.

            :return: array of NmapHost
        """
        return self._hosts

    def get_host_byid(self, host_id):
        """
           Gets a NmapHost object directly from the host array
           by looking it up by id.

           :param ip_addr: ip address of the host to lookup
           :type ip_addr: string

           :return: NmapHost
        """
        rval = None
        for _rhost in self._hosts:
            if _rhost.address == host_id:
                rval = _rhost
        return rval

    @property
    def endtime(self):
        """
            Accessor returning a unix timestamp of when the scan ended.

            :return: integer
        """
        rval = -1
        try:
            rval = int(self._runstats['finished']['time'])
        except(KeyError, TypeError, ValueError):
            pass
        return rval

    @property
    def summary(self):
        """
            Accessor returning a string describing and
            summarizing the scan.

            :return: string
        """
        rval = ''
        try:
            rval = self._runstats['finished']['summary']
        except(KeyError, TypeError):
            pass

        return rval

    @property
    def elapsed(self):
        """
            Accessor returning the number of seconds the scan took

            :return: float (0 >= or -1)
        """
        rval = -1
        try:
            s_elapsed = self._runstats['finished']['elapsed']
            rval = float(s_elapsed)
        except (KeyError, TypeError, ValueError):
            rval = -1
        return rval

    @property
    def hosts_up(self):
        """
            Accessor returning the numer of host detected
            as 'up' during the scan.

            :return: integer (0 >= or -1)
        """
        rval = -1
        try:
            s_up = self._runstats['hosts']['up']
            rval = int(s_up)
        except (KeyError, TypeError, ValueError):
            rval = -1
        return rval

    @property
    def hosts_down(self):
        """
            Accessor returning the numer of host detected
            as 'down' during the scan.

            :return: integer (0 >= or -1)
        """
        rval = -1
        try:
            s_down = self._runstats['hosts']['down']
            rval = int(s_down)
        except (KeyError, TypeError, ValueError):
            rval = -1
        return rval

    @property
    def hosts_total(self):
        """
            Accessor returning the number of hosts scanned in total.

            :return: integer (0 >= or -1)
        """
        rval = -1
        try:
            s_total = self._runstats['hosts']['total']
            rval = int(s_total)
        except (KeyError, TypeError, ValueError):
            rval = -1
        return rval

    def get_raw_data(self):
        """
            Returns a dict representing the NmapReport object.

            :return: dict
            :todo: deprecate. get rid of this uglyness.
        """
        raw_data = {'_nmaprun': self._nmaprun,
                    '_scaninfo': self._scaninfo,
                    '_hosts': self._hosts,
                    '_runstats': self._runstats}
        return raw_data

    def __set_raw_data(self, raw_data):
        self._nmaprun = raw_data['_nmaprun']
        self._scaninfo = raw_data['_scaninfo']
        self._hosts = raw_data['_hosts']
        self._runstats = raw_data['_runstats']

    def is_consistent(self):
        """
            Checks if the report is consistent and can be diffed().

            This needs to be rewritten and removed: diff() should be generic.

            :return: boolean
        """
        rval = False
        rdata = self.get_raw_data()
        _consistent_keys = ['_nmaprun', '_scaninfo', '_hosts', '_runstats']
        if(set(_consistent_keys) == set(rdata.keys()) and
           len([dky for dky in rdata.keys() if rdata[dky] is not None]) == 4):
            rval = True
        return rval

    def get_dict(self):
        """
            Return a python dict representation of the NmapReport object.
            This is used to diff() NmapReport objects via NmapDiff.

            :return: dict
        """
        rdict = dict([("%s::%s" % (_host.__class__.__name__,
                                   str(_host.id)),
                      hash(_host))
                     for _host in self.hosts])
        rdict.update({'commandline': self.commandline,
                      'version': self.version,
                      'scan_type': self.scan_type,
                      'elapsed': self.elapsed,
                      'hosts_up': self.hosts_up,
                      'hosts_down': self.hosts_down,
                      'hosts_total': self.hosts_total})
        return rdict

    @property
    def id(self):
        """
            Dummy id() defined for reports.
        """
        return hash(1)

    def __repr__(self):
        return "{0}: started at {1} hosts up {2}/{3}".format(
               self.__class__.__name__,
               self.started,
               self.hosts_up,
               self.hosts_total)
