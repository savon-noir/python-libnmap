#!/usr/bin/env python


class NmapBackendPlugin(object):
    def __init__(self):
        self.dbname = 'nmapdb'
        self.store = 'reports'

    def insert(self, dict_data):
        raise NotImplementedError

    def update(self, id):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError

    def getall(self):
        """return a list of all NmapReport saved in the backend
           TODO : add a filter capability
        """
        raise NotImplementedError

    def find(self, key):
        raise NotImplementedError
