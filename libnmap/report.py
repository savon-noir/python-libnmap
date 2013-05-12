#!/usr/bin/env python
import sys
import inspect
from libnmap.diff import NmapDiff
#from libnmap.plugins.backendplugin import NmapBackendPlugin


class NmapReport(object):
    def __init__(self, name='', raw_data=None):
        self._name = name
        self._nmaprun = {}
        self._scaninfo = {}
        self._hosts = []
        self._runstats = {}
        if raw_data is not None:
            self.set_raw_data(raw_data)

    def report_export(self, file_path, output='csv'):
        """DEPRECATED"""
        return 0

    def read_fromfile(self, file_path):
        """DEPRECATED"""
        self.report_import(file_path)
        return self.get_raw_data()

    def write_tofile(self, file_path, output='csv'):
        """DEPRECATED"""
        return self.report_export(file_path, output)

    def db(self, plugin_name="mongodb", **kwargs):
        """DEPRECATED"""
        r = None
        plugin_path = "libnmap.plugins.%s" % (plugin_name)
        __import__(plugin_path)
        pluginobj = sys.modules[plugin_path]
        pluginclasses = inspect.getmembers(pluginobj, inspect.isclass)
        for classname, classobj in pluginclasses:
            if inspect.getmodule(classobj).__name__.find(plugin_path) == 0:
                r = classobj(**kwargs)
        return r

    def save(self, backend):
        """this fct get an NmapBackendPlugin representing the backend
        """
        if backend is not None:
            #do stuff
            id = backend.insert(self)
        else:
            raise RuntimeError
        return id

    def diff(self, other):
        if self._is_consistent() and other._is_consistent():
            r = NmapDiff(self, other)
        else:
            r = set()
        return r

    def set_raw_data(self, raw_data):
        self._nmaprun = raw_data['_nmaprun']
        self._scaninfo = raw_data['_scaninfo']
        self._hosts = raw_data['_hosts']
        self._runstats = raw_data['_runstats']

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

    @property
    def hosts_up(self):
        return (self._runstats['hosts']['up']
                if 'hosts' in self._runstats
                else '')

    @property
    def hosts_down(self):
        return (self._runstats['hosts']['down']
                if 'hosts' in self._runstats
                else '')

    @property
    def hosts_total(self):
        return (self._runstats['hosts']['total']
                if 'hosts' in self._runstats
                else '')

    def get_raw_data(self):
        raw_data = {'_nmaprun': self._nmaprun,
                    '_scaninfo': self._scaninfo,
                    '_hosts': self._hosts,
                    '_runstats': self._runstats}
        return raw_data

    def _is_consistent(self):
        r = False
        rd = self.get_raw_data()
        _consistent_keys = ['_nmaprun', '_scaninfo', '_hosts', '_runstats']
        if (set(_consistent_keys) == set(rd.keys()) and
                len([k for k in rd.keys() if rd[k] is not None]) == 4):
                r = True
        return r

    def __repr__(self):
        return "{0} {1} hosts: {2} {3}".format(self._nmaprun, self._scaninfo,
                                               len(self._hosts),
                                               self._runstats)

    def get_dict(self):
        d = dict([("%s.%s" % (h.__class__.__name__, str(h.id)), hash(h))
                 for h in self.scanned_hosts])
        d.update({'hosts_up': self.hosts_up, 'hosts_down': self.hosts_down,
                  'hosts_total': self.hosts_total})
        return d

    @property
    def id(self):
        return hash(1)
