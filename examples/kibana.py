#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.parser import NmapParser
from libnmap.reportjson import ReportDecoder
from libnmap.plugins.es import NmapElasticsearchPlugin
from datetime import datetime
import json


def report_store(nmap_report, database):
    jhostlist = []
    for nmap_host in nmap_report.hosts:
        jhost = host_store(nmap_host, database)
        jhostlist.append(jhost)

    for jhost in jhostlist:
        database.insert(jhost, doc_type="NmapHost")

    return jhostlist


def get_os(nmap_host):
    rval = {'os': '', 'accuracy': 0}
    if nmap_host.is_up() and nmap_host.os_fingerprinted:
        os_list = []
        for osm in nmap_host.os.osmatches:
            os_list.append({"os": osm.name, "accuracy": osm.accuracy})
            os_list.sort(key=lambda x: x['accuracy'], reverse=True)

        if len(os_list):
            rval.update(os_list[0])
    return rval


def host_store(nmap_host, database):
    host_keys = ["starttime", "endtime", "address", "hostnames",
                 "ipv4", "ipv6", "mac", "status"]
    jhost = {}
    for hkey in host_keys:
        if hkey == "starttime" or hkey == "endtime":
            val = getattr(nmap_host, hkey)
            jhost[hkey] = int(val) if len(val) else 0
        else:
            jhost[hkey] = getattr(nmap_host, hkey)

    for nmap_service in nmap_host.services:
        reportitems = item_store(nmap_service, database)

        for ritem in reportitems:
            ritem.update(jhost)
            database.insert(ritem, doc_type="ReportItem")
    
    jhost.update(get_os(nmap_host))
    return jhost

def item_store(nmap_service, database):
    service_keys = ["port", "protocol", "state"]
    ritems = []

    # create report item for basic port scan
    jservice = {}
    for skey in service_keys:
        jservice[skey] = getattr(nmap_service, skey)
    jservice['type'] = 'port-scan'
    jservice['service'] = nmap_service.service
    jservice['service-data'] = nmap_service.banner
    ritems.append(jservice)

    # create report items from nse script output
    for nse_item in nmap_service.scripts_results:
        jnse = {}
        for skey in service_keys:
            jnse[skey] = getattr(nmap_service, skey)
        jnse['type'] = 'nse-script'
        jnse['service'] = nse_item['id']
        jnse['service-data'] = nse_item['output']
        ritems.append(jnse)

    return ritems


xmlscans = ['../libnmap/test/files/1_hosts.xml', '../libnmap/test/files/full_sudo6.xml']
for xmlscan in xmlscans:
    nmap_report = NmapParser.parse_fromfile(xmlscan)

    if nmap_report:
        mindex = datetime.fromtimestamp(nmap_report.started).strftime('%Y-%m-%d')
        db = NmapElasticsearchPlugin(index=mindex)
        j = report_store(nmap_report, db)
