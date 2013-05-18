libnmap.process
===============

What
----
This modules enables you to launch nmap scans with simples python commands::

    from libnmap.process import NmapProcess
    
    nm = NmapProcess("scanme.nmap.org", options="-sV")
    rc = nm.run()
    
    if nm.rc == 0:
        print nm.stdout
    else:
        print nm.stderr

This module is also able to trigger a callback function provided by the user. This callback will be triggered each time nmap returns data to the lib.
It is to note that the lib forces nmap to return its status (progress and etc) every two seconds. The event callback could then play around with those values while running.

The full `source code <https://github.com/savon-noir/python-nmap-lib>`_ is available on GitHub. Please, do not hesitate to fork it and issue pull requests.

Code API
--------

.. automodule:: libnmap.process
.. autoclass:: NmapProcess
    :members:
