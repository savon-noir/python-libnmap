#!/usr/bin/env python
import csv
from datetime import datetime
from libnmap.objects import NmapService
from libnmap.plugins.backendplugin import NmapBackendPlugin

class NmapCsvPlugin(NmapBackendPlugin):
    """
        CSV plugin class for libnmap
        All subclass MUST at least implement the following methods
    """
    def __init__(self):
        NmapBackendPlugin.__init__(self)
        self.dict = {}

    def insert(self, report, doc_type=None):
        """
            insert NmapReport in the backend
            :param NmapReport:
            :return: str the filenmae of the object in the backend for
            future usage
            or None
        """
        if doc_type is None:
            doc_type = 'NmapReport'
        if report.is_from_file:
            id = report.filename
        else:
            rep_date = datetime.fromtimestamp(int(report.started))
            id = "nmap-{0}".format(rep_date.strftime('%Y-%m-%d_%H-%M'))
        with open(str(id) + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['address', 'hostnames', 'status']
            fieldnames = fieldnames + report.services
            # servicesset = set()
            # serviceformat = '{0.id}/{0.service}'
            # servicesort = lambda p: p[p.find('.'):p.find('/')]
            # for host in report.hosts:
            #     for service in host.services:
            #         servicesset.add(serviceformat.format(service))
            # servicefilenames = sorted(list(servicesset),
            #                           key = servicesort)
            # fieldnames = fieldnames + servicefilenames
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writeheader()
            for host in report.hosts:
            #     data = {key: value for key, value in host.get_dict().items()
            #             if key in fieldnames}
            #     for service in host.services:
            #         data[serviceformat.format(service)] = service.state
                 csvwriter.writerow(host.get_dict())
        return id


    def delete(self, id):
        """
            delete NmapReport if the backend
            :param id: str, filenmae
        """
        raise NotImplementedError

    def get(self, id):
        """
            retreive a NmapReport from the backend
            :param id: str, filenmae
            :return: NmapReport
        """
        raise NotImplementedError

    def getall(self, filter):
        """
            :return: collection of tuple (id,NmapReport)
            :param filter: Nice to have implement a filter capability
        """
        raise NotImplementedError
