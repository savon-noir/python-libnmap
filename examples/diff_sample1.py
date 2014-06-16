#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.parser import NmapParser

rep1 = NmapParser.parse_fromfile('libnmap/test/files/1_hosts.xml')
rep2 = NmapParser.parse_fromfile('libnmap/test/files/1_hosts_diff.xml')

rep1_items_changed = rep1.diff(rep2).changed()
changed_host_id = rep1_items_changed.pop().split('::')[1]

changed_host1 = rep1.get_host_byid(changed_host_id)
changed_host2 = rep2.get_host_byid(changed_host_id)
host1_items_changed = changed_host1.diff(changed_host2).changed()

changed_service_id = host1_items_changed.pop().split('::')[1]
changed_service1 = changed_host1.get_service_byid(changed_service_id)
changed_service2 = changed_host2.get_service_byid(changed_service_id)
service1_items_changed = changed_service1.diff(changed_service2).changed()

for diff_attr in service1_items_changed:
    print("diff({0}, {1}) [{2}:{3}] [{4}:{5}]".format(changed_service1.id,
                                                      changed_service2.id,
                                                      diff_attr,
                                                      getattr(changed_service1,
                                                              diff_attr),
                                                      diff_attr,
                                                      getattr(changed_service2,
                                                              diff_attr)))
