#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.parser import NmapParser
from elasticsearch import Elasticsearch
from datetime import datetime
import pygeoip


def store_report(nmap_report, database, index):
    rval = True
    for nmap_host in nmap_report.hosts:
        rv = store_reportitem(nmap_host, database, index)
        if rv is False:
            print("Failed to store host {0} in "
                  "elasticsearch".format(nmap_host.address))
            rval = False

    return rval


def get_os(nmap_host):
    rval = {'vendor': 'unknown', 'product': 'unknown'}
    if nmap_host.is_up() and nmap_host.os_fingerprinted:
        cpelist = nmap_host.os.os_cpelist()
        if len(cpelist):
            mcpe = cpelist.pop()
            rval.update({'vendor': mcpe.get_vendor(),
                         'product': mcpe.get_product()})
    return rval


def get_geoip_code(address):
    gi = pygeoip.GeoIP('/usr/share/GeoIP/GeoIP.dat')
    return gi.country_code_by_addr(address)


def store_reportitem(nmap_host, database, index):
    host_keys = ["starttime", "endtime", "address", "hostnames",
                 "ipv4", "ipv6", "mac", "status"]
    jhost = {}
    for hkey in host_keys:
        if hkey == "starttime" or hkey == "endtime":
            val = getattr(nmap_host, hkey)
            jhost[hkey] = datetime.fromtimestamp(int(val) if len(val) else 0)
        else:
            jhost[hkey] = getattr(nmap_host, hkey)

    jhost.update({'country': get_geoip_code(nmap_host.address)})
    jhost.update(get_os(nmap_host))
    for nmap_service in nmap_host.services:
        reportitems = get_item(nmap_service)

        for ritem in reportitems:
            ritem.update(jhost)
            database.index(index=index,
                           doc_type="NmapItem",
                           body=ritem)
    return jhost


def get_item(nmap_service):
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


xmlscans = ['../libnmap/test/files/1_hosts.xml',
            '../libnmap/test/files/full_sudo6.xml',
            '/vagrant/nmap_switches.xml',
            '/vagrant/nmap-5hosts.xml']

for xmlscan in xmlscans:
    nmap_report = NmapParser.parse_fromfile(xmlscan)

    if nmap_report:
        rep_date = datetime.fromtimestamp(int(nmap_report.started))
        index = "nmap-{0}".format(rep_date.strftime('%Y-%m-%d'))
        db = Elasticsearch()
        j = store_report(nmap_report, db, index)
