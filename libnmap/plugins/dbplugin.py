#!/usr/bin/env python


class NmapDBPlugin(object):
    def __init__(self):
        self.dbname = 'nmapdb'
        self.store = 'reports'

    def db_insert(self, dict_data):
        raise NotImplementedError

    def db_update(self, id):
        raise NotImplementedError

    def db_delete(self, id):
        raise NotImplementedError

    def db_get(self, id):
        raise NotImplementedError

    def db_find(self, key):
        raise NotImplementedError
