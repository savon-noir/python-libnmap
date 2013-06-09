"""
:mod:`libnmap.plugin.s3` -- S3 Backend Plugin
===================================

.. module:: libnmap.plugin.s3
:platform: Linux
:synopsis: a plugin is representation of a S3 backend using boto
.. moduleauthor:: Ronald Bister
.. moduleauthor:: Mike Boutillier
"""

#!/usr/bin/env python
import json
import os
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
        This plugin save the reports on S3 and compatible
        This is now a beta version who use eucalyptus walrus
    """
    def __init__(self, **kwargs):
        """
            - get access key/secret key from env or kwargs
            - create the conn object
            - create the bucket
            - may raise exception (ie in case of conflict bucket name)
        """
        NmapBackendPlugin.__init__(self)
        try:
            self.awskey = (os.getenv('EC2_ACCESS_KEY') or
                           kwargs['EC2_ACCESS_KEY'])
            self.awssecret = (os.getenv('EC2_SECRET_KEY') or
                              kwargs['EC2_SECRET_KEY'])
            calling_format = OrdinaryCallingFormat()
            self.conn = S3Connection(host="walrus.ecc.eucalyptus.com",
                                     path="/services/Walrus",
                                     port=8773,
                                     calling_format=calling_format,
                                     is_secure=False,
                                     aws_access_key_id=self.awskey,
                                     aws_secret_access_key=self.awssecret)
            self.bucket = self.conn.lookup(kwargs['bucket'])
            if self.bucket is None:
                self.bucket = self.conn.create_bucket(kwargs['bucket'])
        except:
            raise

    def insert(self, report):
        """
            create a json string from an NmapReport instance
            and push it to S3 bucket
            :param NmapReport: obj to insert
            :rtype: string
            :return: str id
            TODO Add tagging option
        """
        try:
            oid = ObjectId()
            mykey = Key(self.bucket)
            mykey.key = str(oid)
            strjsonnmapreport = json.dumps(report, cls=ReportEncoder)
            mykey.set_contents_from_string(strjsonnmapreport)
        except:
            print "Bucket cannot insert"
            raise
        return str(oid)

    def get(self, str_report_id=None):
        """ select a NmapReport by Id
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
                print "Not Found"
        return nmapreport

    def getall(self, dict_filter=None):
        """
            :rtype: List of tuple
            :return: list of key/report
           TODO : add a filter capability
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
