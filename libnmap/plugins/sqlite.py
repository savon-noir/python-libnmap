#!/usr/bin/env python
import sqlite3

#from libnmap.objects import NmapReport
from libnmap.plugins.backendplugin import NmapBackendPlugin


class NmapSqlitePlugin(NmapBackendPlugin):
    def __init__(self, dbname=None):
        NmapBackendPlugin.__init__(self)
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        # Create table if not exist
        curs.execute('''CREATE TABLE f not exists reports
                (date text, trans text, symbol text, qty real, price real)''')

    def db_insert(self, nmap_report):
        pass

    def db_get(self, report_id=None):
        pass

    def db_delete(self, report_id=None):
        pass
