#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libnmap.plugins.backendplugin import NmapBackendPlugin
from libnmap.reportjson import ReportEncoder, ReportDecoder

import json
from datetime import datetime

Base = declarative_base()


class NmapSqlPlugin(NmapBackendPlugin):
    """
        This class handle the persistence of NmapRepport object in SQL backend
        Implementation is made using sqlalchemy(0.8.1)
        usage :

        #get a nmapReport object
        from libnmap.parser import NmapParser
        from libnmap.reportjson import ReportDecoder, ReportEncoder
        import json
        nmap_report_obj = NmapParser.parse_fromfile(
               '/home/vagrant/python-nmap-lib/libnmap/test/files/1_hosts.xml')

         #get a backend with in memory sqlite
         from libnmap.plugins.backendpluginFactory import BackendPluginFactory
         mybackend_mem = BackendPluginFactory.create(plugin_name='sql',
                                                     url='sqlite://',
                                                     echo=True)

         mybackend_mysql = BackendPluginFactory.create(plugin_name='sql',
                            url='mysql+mysqldb://scott:tiger@localhost/foo',
                            echo=True)
         mybackend = BackendPluginFactory.create(plugin_name='sql',
                                        url='sqlite:////tmp/reportdb.sql',
                                        echo=True)
         #lets save!!
         nmap_report_obj.save(mybackend)
         mybackend.getall()
         mybackend.get(1)
    """
    class Reports(Base):
        """
            Embeded class for ORM map NmapReport to a
            simple three column table
        """
        __tablename__ = 'reports'

        id = Column('report_id', Integer, primary_key=True)
        inserted = Column('inserted', DateTime(), default='now')
        report_json = Column('report_json', LargeBinary())

        def __init__(self, obj_NmapReport):
            self.inserted = datetime.fromtimestamp(obj_NmapReport.endtime)
            dumped_json = json.dumps(obj_NmapReport,
                                     cls=ReportEncoder)
            self.report_json = bytes(dumped_json.encode('UTF-8'))

        def decode(self):
            json_decoded = self.report_json.decode('utf-8')
            nmap_report_obj = json.loads(json_decoded,
                                         cls=ReportDecoder)
            return nmap_report_obj

    def __init__(self, **kwargs):
        """
            constructor receive a **kwargs as the **kwargs in the sqlalchemy
            create_engine() method (see sqlalchemy docs)
            You must add to this **kwargs an 'url' key with the url to your
            database
            This constructor will :
            - create all the necessary obj to discuss with the DB
            - create all the mapping(ORM)

            todo : suport the : sqlalchemy.engine_from_config

            :param **kwargs:
            :raises: ValueError if no url is given,
                    all exception sqlalchemy can throw
            ie sqlite in memory url='sqlite://' echo=True
            ie sqlite file on hd url='sqlite:////tmp/reportdb.sql' echo=True
            ie mysql url='mysql+mysqldb://scott:tiger@localhost/foo'
        """
        NmapBackendPlugin.__init__(self)
        self.engine = None
        self.url = None
        self.Session = sessionmaker()

        if 'url' not in kwargs:
            raise ValueError
        self.url = kwargs['url']
        del kwargs['url']
        try:
            self.engine = create_engine(self.url, **kwargs)
            Base.metadata.create_all(bind=self.engine, checkfirst=True)
            self.Session.configure(bind=self.engine)
        except:
            raise

    def insert(self, nmap_report):
        """
           insert NmapReport in the backend

           :param NmapReport:

           :returns: the ident of the object in the backend for future usage \
           or None
        """
        sess = self.Session()
        report = NmapSqlPlugin.Reports(nmap_report)
        sess.add(report)
        sess.commit()
        reportid = report.id
        sess.close()
        return reportid if reportid else None

    def get(self, report_id=None):
        """
            retreive a NmapReport from the backend

            :param id: str

            :returns: NmapReport
        """
        if report_id is None:
            raise ValueError
        sess = self.Session()
        our_report = (
            sess.query(NmapSqlPlugin.Reports).filter_by(id=report_id).first())
        sess.close()
        return our_report.decode() if our_report else None

    def getall(self):
        """
            :param filter: Nice to have implement a filter capability

            :returns: collection of tuple (id,NmapReport)
        """
        sess = self.Session()
        nmapreportList = []
        for report in (
                sess.query(NmapSqlPlugin.Reports).
                order_by(NmapSqlPlugin.Reports.inserted)):
            nmapreportList.append((report.id, report.decode()))
        sess.close()
        return nmapreportList

    def delete(self, report_id=None):
        """
            Remove a report from the backend

            :param id: str

            :returns: The number of rows deleted
        """
        if report_id is None:
            raise ValueError
        nb_line = 0
        sess = self.Session()
        nb_line = sess.query(NmapSqlPlugin.Reports).\
            filter_by(id=report_id).delete()
        sess.commit()
        sess.close()
        return nb_line
