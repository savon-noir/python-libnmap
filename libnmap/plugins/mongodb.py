#!/usr/bin/env python
from libnmap.plugins.dbplugin import NmapDBPlugin
from pymongo import MongoClient
from bson.objectid import ObjectId


class NmapMongoPlugin(NmapDBPlugin):
    def __init__(self, **kwargs):
        NmapDBPlugin.__init__(self)
        self.dbclient = MongoClient(**kwargs)
        self.collection = self.dbclient[self.dbname][self.store]

    def db_insert(self, dict_data):
        self.collection.insert(dict_data)

    def db_get(self, report_id=None):
        rid = report_id
        if report_id is not None and isinstance(report_id, str):
            rid = ObjectId(report_id)

        if isinstance(rid, ObjectId):
            r = self.collection.find({'_id': rid})
        else:
            r = self.collection.find()
        return r

    def db_delete(self, report_id=None):
        if report_id is not None and isinstance(report_id, str):
            self.collection.remove({'_id': ObjectId(report_id)})
        else:
            self.collection.remove({'_id': report_id})
