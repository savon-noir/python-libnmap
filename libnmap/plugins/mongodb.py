#!/usr/bin/env python
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

from libnmap.reportjson import ReportEncoder
from libnmap.parser import NmapParser
from libnmap.plugins.backendplugin import NmapBackendPlugin


class NmapMongodbPlugin(NmapBackendPlugin):
    def __init__(self, dbname=None, store=None, **kwargs):
        NmapBackendPlugin.__init__(self)
        if dbname is not None:
            self.dbname = dbname
        if store is not None:
            self.store = store
        self.dbclient = MongoClient(**kwargs)
        self.collection = self.dbclient[self.dbname][self.store]

    def insert(self, report):
        """
            create a json object from an NmapReport instance
            :param NmapReport: obj to insert
            :return: str id
        """
        j = json.dumps(report, cls=ReportEncoder)
        try:
            id = self.collection.insert(json.loads(j))
        except:
            print "MONGODB cannot insert"
            raise
        return str(id)

    def get(self, str_report_id=None):
        """ select a NmapReport by Id
            :param str: id
            :return: NmapReport object
        """
        rid = str_report_id
        nmapreport = None
        if str_report_id is not None and isinstance(str_report_id, str):
            rid = ObjectId(str_report_id)

        if isinstance(rid, ObjectId):
            #get a specific report by mongo's id
            resultSet = self.collection.find({'_id': rid})
            if resultSet.count() == 1:
                #search by id means only one in the iterator
                record = resultSet[0]
                #remove mongo's id to recreate the NmapReport Obj
                del record['_id']
                nmapreport = NmapParser.parse_fromdict(record)
        return nmapreport

    def getall(self, dict_filter=None):
        """return a list of all NmapReport saved in the backend
           TODO : add a filter capability
        """
        nmapreportList = []
        r = self.collection.find()
        for report in r:
            del report['_id']
            nmapreport = NmapParser.parse_fromdict(report)
            nmapreportList.append(nmapreport)
        return nmapreportList

    def delete(self, report_id=None):
        """
            delete an obj from the backend
            :param str: id
            :return: dict document with result or None
        """
        if report_id is not None and isinstance(report_id, str):
            return self.collection.remove({'_id': ObjectId(report_id)})
        else:
            return self.collection.remove({'_id': report_id})
