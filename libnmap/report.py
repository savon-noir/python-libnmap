#!/usr/bin/env python
from libnmap import NmapParser, NmapParserException, NmapDiff
## TODO:  del/add_host()
#         add/del_service()
class NmapReport(object):
    def __init__(self, name='', raw_data=None):
        self._name = name
        self._nmaprun = {}
        self._scaninfo = {}
        self._hosts = []
        self._runstats = {}
        if raw_data is not None:
            self.set_raw_data(raw_data)

    def report_import(self, file_path):
        try:
            set_raw_data(NmapParser.parse_fromfile(file_path))
        except:
            raise NmapParserException("Error while trying to import file: {0}".format(file_path))

    def report_export(self, file_path, output='csv'):
        return 0

    def diff(self, other):
        if self.is_consistent() and other.is_consistent():
            r = NmapDiff(self, other)
        else:
            r = set()
        return r

    def set_raw_data(self, raw_data):
        self._nmaprun = raw_data['nmaprun']
        self._scaninfo = raw_data['scaninfo']
        self._hosts = raw_data['hosts']
        self._runstats = raw_data['runstats']

    @property
    def name(self):
        return self._name

    ### implement with iterators 
    @property
    def scanned_hosts(self):
        return self._hosts

    @property
    def endtime(self):
        return self._runstats['finished']['time']

    @property
    def summary(self):
        return self._runstats['finished']['summary']

    @property
    def elapsed(self):
        return self._runstats['finished']['elapsed']

    def get_raw_data(self):
        raw_data = { 'nmaprun': self._nmaprun,
                        'scaninfo': self._scaninfo,
                        'hosts': self._hosts, 
                        'runstats': self._runstats,
        }
        return raw_data

    def is_consistent(self):
        r = False
        rd = self.get_raw_data()
        if set(['nmaprun', 'scaninfo', 'hosts', 'runstats']) == set(rd.keys()) and \
            len([ k for k in rd.keys() if rd[k] is not None ]) == 4:
                r = True
        return r

    def __repr__(self):
        return "{0} {1} hosts: {2} {3}".format(self._nmaprun, self._scaninfo, len(self._hosts), self._runstats)

    def get_dict(self):
        return dict([("%s.%s" % (h.__class__.__name__, h.id), hash(h)) for h in self.scanned_hosts ])
