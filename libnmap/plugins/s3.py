#!/usr/bin/env python
"""
:mod:`libnmap.plugin.s3` -- S3 Backend Plugin
=============================================

.. module:: libnmap.plugin.s3

:platform: Linux
:synopsis: a plugin is representation of a S3 backend using boto

.. moduleauthor:: Ronald Bister
.. moduleauthor:: Mike Boutillier
"""
import json
from bson.objectid import ObjectId
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.key import Key
from boto.s3.bucketlistresultset import bucket_lister
from boto.exception import S3ResponseError
from libnmap.reportjson import ReportEncoder
from libnmap.parser import NmapParser
from libnmap.plugins.backendplugin import NmapBackendPlugin


class NmapS3Plugin(NmapBackendPlugin):
    """
        This plugin save the reports on S3 and compatible.
    """
    def __init__(self, **kwargs):
        """
            - create the conn object
            - create the bucket (if it doesn't exist)
                - if not given, awsaccessKey_nmapreport
            - may raise exception (ie in case of conflict bucket name)
            - sample :
            To connect to walrus:
            from libnmap.plugins.backendpluginFactory import
                            BackendPluginFactory
            walrusBackend =
              BackendPluginFactory.create(
                    plugin_name='s3',
                    host="walrus.ecc.eucalyptus.com",
                    path="/services/Walrus",port=8773,
                    is_secure=False,
                    aws_access_key_id='UU72FLVJCAYRATLXI70YH',
                    aws_secret_access_key=
                               'wFg7gP5YFHjVlxakw1g1uCC8UR2xVW5ax9ErZCut')
           To connect to S3:
           mybackend_S3 =
             BackendPluginFactory.create(
                plugin_name='s3',
                is_secure=True,
                aws_access_key_id='MYACCESSKEY',
                aws_secret_access_key='MYSECRET')
        """
        NmapBackendPlugin.__init__(self)
        try:
            calling_format = OrdinaryCallingFormat()
            if 'bucket' not in kwargs:
                self.bucket_name = ''.join(
                    [kwargs['aws_access_key_id'].lower(),
                     "_nmapreport"])
            else:
                self.bucket_name = kwargs['bucket']
                del kwargs['bucket']
            kwargs['calling_format'] = calling_format
            self.conn = S3Connection(**kwargs)
            self.bucket = self.conn.lookup(self.bucket_name)
            if self.bucket is None:
                self.bucket = self.conn.create_bucket(self.bucket_name)
        except:
            raise

    def insert(self, report):
        """
            create a json string from an NmapReport instance
            and push it to S3 bucket.

            :param NmapReport: obj to insert
            :rtype: string
            :return: str id
            :todo: Add tagging option
        """
        try:
            oid = ObjectId()
            mykey = Key(self.bucket)
            mykey.key = str(oid)
            strjsonnmapreport = json.dumps(report, cls=ReportEncoder)
            mykey.set_contents_from_string(strjsonnmapreport)
        except:
            raise Exception("Failed to add nmap object in s3 bucket")
        return str(oid)

    def get(self, str_report_id=None):
        """
            select a NmapReport by Id.

            :param str: id
            :rtype: NmapReport
            :return: NmapReport object
        """
        nmapreport = None
        if str_report_id is not None and isinstance(str_report_id, str):
            try:
                mykey = Key(self.bucket)
                mykey.key = str_report_id
                nmapreportjson = json.loads(mykey.get_contents_as_string())
                nmapreport = NmapParser.parse_fromdict(nmapreportjson)
            except S3ResponseError:
                pass
        return nmapreport

    def getall(self, dict_filter=None):
        """
            :rtype: List of tuple
            :return: list of key/report
            :todo: add a filter capability
        """
        nmapreportlist = []
        for key in bucket_lister(self.bucket):
            if isinstance(key, Key):
                nmapreportjson = json.loads(key.get_contents_as_string())
                nmapreport = NmapParser.parse_fromdict(nmapreportjson)
                nmapreportlist.append((key.key, nmapreport))
        return nmapreportlist

    def delete(self, report_id=None):
        """
            delete an obj from the backend

            :param str: id
            :return: dict document with result or None
        """
        rcode = None
        if report_id is not None and isinstance(report_id, str):
            rcode = self.bucket.delete_key(report_id)
        return rcode
