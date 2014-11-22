# -*- coding: utf-8 -*-

import json
from libnmap.reportjson import ReportEncoder
from libnmap.plugins.backendplugin import NmapBackendPlugin
from elasticsearch import Elasticsearch
from datetime import datetime


class NmapElasticsearchPlugin(NmapBackendPlugin):
    """
        This class enables the user to store and manipulate nmap reports \
        in a elastic search db.
    """
    def __init__(self, index=None):
        if index is None:
            self.index = "nmap.{0}".format(datetime.now().strftime('%Y-%m-%d'))
        else:
            self.index = index
        self._esapi = Elasticsearch()

    def insert(self, report, doc_type=None):
        """
            insert NmapReport in the backend
            :param NmapReport:
            :return: str the ident of the object in the backend for
            future usage
            or None
        """
        if doc_type is None:
            doc_type = 'NmapReport'
        j = json.dumps(report, cls=ReportEncoder)
        res = self._esapi.index(
            index=self.index,
            doc_type=doc_type,
            body=json.loads(j))
        rc = res['_id']
        return rc

    def delete(self, id):
        """
            delete NmapReport if the backend
            :param id: str
        """
        raise NotImplementedError

    def get(self, id):
        """
            retreive a NmapReport from the backend
            :param id: str
            :return: NmapReport
        """
        res = self._esapi.get(index=self.index,
                              doc_type="NmapReport",
                              id=id)['_source']
        return res

    def getall(self, filter=None):
        """
            :return: collection of tuple (id,NmapReport)
            :param filter: Nice to have implement a filter capability
        """
        rsearch = self._esapi.search(index=self.index,
                                     body={"query": {"match_all": {}}})
        print("--------------------")
        print(type(rsearch))
        print(rsearch)
        print("------------")
