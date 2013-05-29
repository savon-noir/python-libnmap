#!/usr/bin/env python


class NmapBackendPlugin(object):
    """
        Abstract class showing to the minimal implementation for a plugin
        All subclass MUST at least implement the following methods
    """
    def __init__(self):
        self.dbname = 'nmapdb'
        self.store = 'reports'

    def insert(self, NmapReport):
        """
            insert NmapReport in the backend
            :param NmapReport:
            :return: str the ident of the object in the backend for
            future usage
            or None
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def getall(self, filter):
        """
            :return: collection of tuple (id,NmapReport)
            :param filter: Nice to have implement a filter capability
        """
        raise NotImplementedError
