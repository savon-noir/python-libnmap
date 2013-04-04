#!/usr/bin/env python


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
        return 0
    def report_export(self, file_path, output='csv'):
        return 0
    def diff(self, other):
        return 0

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

    def __repr__(self):
        return "{0} {1} hosts: {2} {3}".format(self._nmaprun, self._scaninfo, len(self._hosts), self._runstats)
