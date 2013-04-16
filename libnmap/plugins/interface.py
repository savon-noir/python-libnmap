#!/usr/bin/env python

class NmapDataPlugin(object):
    def __init__(self):
        self.dbname = 'nmapdb'
        self.store = 'reports'

    def data_add(self, dict_data):
        raise Exception("Method add not implemented")
    def data_del(self, id):
        raise Exception("Method add not implemented")
