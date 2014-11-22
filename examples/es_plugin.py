#!/usr/bin/env python

from libnmap.parser import NmapParser
from libnmap.reportjson import ReportDecoder
from libnmap.plugins.es import NmapElasticsearchPlugin
from datetime import datetime
import json

nmap_report = NmapParser.parse_fromfile('libnmap/test/files/1_hosts.xml')
mindex = datetime.fromtimestamp(nmap_report.started).strftime('%Y-%m-%d')
db = NmapElasticsearchPlugin(index=mindex)
dbid = db.insert(nmap_report)
nmap_json = db.get(dbid)

nmap_obj = json.loads(json.dumps(nmap_json), cls=ReportDecoder)
print(nmap_obj)
#print(db.getall())

