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

Code API
--------

.. automodule:: libnmap.diff
.. autoclass:: NmapDiff
    :members:
