#!/usr/bin/env python
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

from libnmap.reportjson import ReportDecoder, ReportEncoder
from libnmap.plugins.backendplugin import NmapBackendPlugin


class NmapMongoPlugin(NmapBackendPlugin):
    def __init__(self, dbname=None, store=None, **kwargs):
        NmapBackendPlugin.__init__(self)
        if dbname is not None:
            self.dbname = dbname
        if store is not None:
            self.store = store
        self.dbclient = MongoClient(**kwargs)
        self.collection = self.dbclient[self.dbname][self.store]

    def insert(self, report):
        # create a json object from an NmapReport instance
        j = json.dumps(report, cls=ReportEncoder)
        try:
            id = self.collection.insert(json.loads(j))
        except:
            print "MONGODB cannot insert"
            raise
        return id

    def get(self, report_id=None):
        rid = report_id
        if report_id is not None and isinstance(report_id, str):
            rid = ObjectId(report_id)

        if isinstance(rid, ObjectId):
            r = self.collection.find({'_id': rid})
            nmapreport = json.loads(r, cls=ReportDecoder)
        else:
            r = self.collection.find()
        return r

    def delete(self, report_id=None):
        if report_id is not None and isinstance(report_id, str):
            self.collection.remove({'_id': ObjectId(report_id)})
        else:
            self.collection.remove({'_id': report_id})
