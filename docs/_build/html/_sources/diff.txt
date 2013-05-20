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
Below, you will find a small code example only covering changed attributes. To implement a full diff, just duplicate that code
for added and removed keys::

    #!/usr/bin/env python
    
    from libnmap.parser import NmapParser
    
    
    def nested_obj(objname):
        rval = None
        splitted = objname.split("::")
        if len(splitted) == 2:
            rval = splitted
        return rval
    
    
    def print_diff(obj1, obj2):
        ndiff = obj1.diff(obj2)
    
        changed_keys = ndiff.changed()
    
        for ckey in changed_keys:
            nested = nested_obj(ckey)
            if nested is not None:
                if nested[0] == 'NmapHost':
                    subobj1 = obj1.get_host_byid(nested[1])
                    subobj2 = obj2.get_host_byid(nested[1])
                elif nested[0] == 'NmapService':
                    subobj1 = obj1.get_service_byid(nested[1])
                    subobj2 = obj2.get_service_byid(nested[1])
                print_diff(subobj1, subobj2)
            else:
                print "~ {0} {1}: {2} => {3}".format(obj1, ckey,
                                                 getattr(obj1, ckey),
                                                 getattr(obj2, ckey))
    
    
    def main():
        rep1 = NmapParser.parse_fromfile('libnmap/test/files/1_hosts.xml')
        rep2 = NmapParser.parse_fromfile('libnmap/test/files/1_hosts_diff.xml')
    
        print_diff(rep1, rep2)
    
    
    if __name__ == "__main__":
        main()

This code will output the following::

    (pydev)$ python /tmp/za.py
    ~ NmapService: [open 3306/tcp mysql ()] state: open => filtered
    (pydev)$


Code API
--------

.. automodule:: libnmap.diff
.. autoclass:: NmapDiff
    :members:
