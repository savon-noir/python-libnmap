#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.parser import NmapParser


def nested_obj(objname):
    rval = None
    splitted = objname.split("::")
    if len(splitted) == 2:
        rval = splitted
    return rval


def print_diff_added(obj1, obj2, added):
    for akey in added:
        nested = nested_obj(akey)
        if nested is not None:
            if nested[0] == 'NmapHost':
                subobj1 = obj1.get_host_byid(nested[1])
            elif nested[0] == 'NmapService':
                subobj1 = obj1.get_service_byid(nested[1])
            print("+ {0}".format(subobj1))
        else:
            print("+ {0} {1}: {2}".format(obj1, akey, getattr(obj1, akey)))


def print_diff_removed(obj1, obj2, removed):
    for rkey in removed:
        nested = nested_obj(rkey)
        if nested is not None:
            if nested[0] == 'NmapHost':
                subobj2 = obj2.get_host_byid(nested[1])
            elif nested[0] == 'NmapService':
                subobj2 = obj2.get_service_byid(nested[1])
            print("- {0}".format(subobj2))
        else:
            print("- {0} {1}: {2}".format(obj2, rkey, getattr(obj2, rkey)))


def print_diff_changed(obj1, obj2, changes):
    for mkey in changes:
        nested = nested_obj(mkey)
        if nested is not None:
            if nested[0] == 'NmapHost':
                subobj1 = obj1.get_host_byid(nested[1])
                subobj2 = obj2.get_host_byid(nested[1])
            elif nested[0] == 'NmapService':
                subobj1 = obj1.get_service_byid(nested[1])
                subobj2 = obj2.get_service_byid(nested[1])
            print_diff(subobj1, subobj2)
        else:
            print("~ {0} {1}: {2} => {3}".format(obj1, mkey,
                                                 getattr(obj2, mkey),
                                                 getattr(obj1, mkey)))


def print_diff(obj1, obj2):
    ndiff = obj1.diff(obj2)

    print_diff_changed(obj1, obj2, ndiff.changed())
    print_diff_added(obj1, obj2, ndiff.added())
    print_diff_removed(obj1, obj2, ndiff.removed())


def main():
    newrep = NmapParser.parse_fromfile('libnmap/test/files/2_hosts_achange.xml')
    oldrep = NmapParser.parse_fromfile('libnmap/test/files/1_hosts.xml')

    print_diff(newrep, oldrep)


if __name__ == "__main__":
    main()
