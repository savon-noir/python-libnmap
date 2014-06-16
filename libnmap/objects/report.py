# -*- coding: utf-8 -*-
from libnmap.diff import NmapDiff


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

            :return: str
        """
        if backend is not None:
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
    def endtimestr(self):
        """
            Accessor returning a human readable time string
            of when the scan ended.

            :return: string
        """
        rval = ''
        try:
            rval = self._runstats['finished']['timestr']
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

        if len(rval) == 0:
            rval = ("Nmap ended at {0} ; {1} IP addresses ({2} hosts up)"
                    " scanned in {3} seconds".format(self.endtimestr,
                                                     self.hosts_total,
                                                     self.hosts_up,
                                                     self.elapsed))
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
        rdict = dict([("{0}::{1}".format(_host.__class__.__name__,
                                         str(_host.id)),
                     hash(_host)) for _host in self.hosts])
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

    def __eq__(self, other):
        """
            Compare eq NmapReport based on :

                - create a diff obj and check the result
                report are equal if added&changed&removed are empty

            :return: boolean
        """
        rval = False
        if(self.__class__ == other.__class__ and self.id == other.id):
            diffobj = self.diff(other)
            rval = (len(diffobj.changed()) == 0 and
                    len(diffobj.added()) == 0 and
                    len(diffobj.removed()) == 0
                    )
        return rval

    def __ne__(self, other):
        """
            Compare ne NmapReport based on:

                - create a diff obj and check the result
                report are ne if added|changed|removed are not empty

            :return: boolean
        """
        rval = True
        if(self.__class__ == other.__class__ and self.id == other.id):
            diffobj = self.diff(other)
            rval = (len(diffobj.changed()) != 0 or
                    len(diffobj.added()) != 0 or
                    len(diffobj.removed()) != 0
                    )
        return rval

    def __repr__(self):
        return "{0}: started at {1} hosts up {2}/{3}".format(
               self.__class__.__name__,
               self.started,
               self.hosts_up,
               self.hosts_total)
