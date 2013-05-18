libnmap.diff
==============

What
----
This modules enables the user to diff two NmapObjects: NmapService, NmapHost, NmapReport.

The constructor returns a NmapDiff object which he can then use to call its inherited methods:

    - added()
    - removed()
    - changed()
    - unchanged()

Those methods return a python set() of keys which have been changed/added/removed/unchanged from one
object to another.
The keys of each objects could be found in the implementation of the get_dict() methods of the compared objects.

The example below is a heavy version of going through all nested objects to see waht has changed after a diff::

    #!/usr/bin/env python
    
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
        print "diff({0}, {1}) [{2}:{3}] [{4}:{5}]".format(changed_service1.id,
                                                         changed_service2.id,
                                                         diff_attr,
                                                         getattr(changed_service1, diff_attr),
                                                         diff_attr,
                                                         getattr(changed_service2, diff_attr))

This outputs the following line::

   (pydev)$ python /tmp/z.py
   diff(tcp.3306, tcp.3306) [state:open] [state:filtered]
   (pydev)$

Of course, the above code is quite ugly and heavy but the idea behind diff was to be as generic as possible in order to
let the user of the lib defines its own algorithms to extract the data.

A less manual and more clever approach would be to recursively retrieve the changed attributes and values of nested objects.
It is left as "exercize" until we put it in this documentation.

Code API
--------

.. automodule:: libnmap.diff
.. autoclass:: NmapDiff
    :members:
