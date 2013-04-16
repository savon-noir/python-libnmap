#!/usr/bin/env python
from libnmap.plugins.interface import NmapDataPlugin
from pymongo import MongoClient

class NmapMongoPlugin(NmapDataPlugin):
    def __init__(self):
        NmapDataPlugin.__init__(self)

    def data_add(self, dict_data):
        dbclient = MongoClient()
        reports = dbclient[self.dbname][self.store]
        reports.insert(dict_data)
