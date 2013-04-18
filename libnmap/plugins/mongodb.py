#!/usr/bin/env python
from libnmap.plugins.dbplugin import NmapDBPlugin
from pymongo import MongoClient

class NmapMongoPlugin(NmapDBPlugin):
    def __init__(self, **kwargs):
        NmapDBPlugin.__init__(self)
        self.dbclient = MongoClient(**kwargs)
        self.collection = self.dbclient[self.dbname][self.store]

    def db_insert(self, dict_data):
        self.collection.insert(dict_data)
