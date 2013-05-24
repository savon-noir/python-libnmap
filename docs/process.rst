libnmap.process
===============

Using libnmap.process
---------------------

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

To go a bit further, you can always use the threading capabilities of the NmapProcess class and run the class in the background

.. literalinclude:: ../examples/proc_async.py

The above code will print out the following on standard output::

    (pydev)[dev@bouteille python-nmap-lib]$ python examples/proc_async.py
    Nmap Scan running: ETC: 0 DONE: 0%
    Nmap Scan running: ETC: 1369433951 DONE: 2.45%
    Nmap Scan running: ETC: 1369433932 DONE: 13.55%
    Nmap Scan running: ETC: 1369433930 DONE: 25.35%
    Nmap Scan running: ETC: 1369433931 DONE: 33.40%
    Nmap Scan running: ETC: 1369433932 DONE: 41.50%
    Nmap Scan running: ETC: 1369433931 DONE: 52.90%
    Nmap Scan running: ETC: 1369433931 DONE: 62.55%
    Nmap Scan running: ETC: 1369433930 DONE: 75.55%
    Nmap Scan running: ETC: 1369433931 DONE: 81.35%
    Nmap Scan running: ETC: 1369433931 DONE: 99.99%
    rc: 0 output: Nmap done at Sat May 25 00:18:51 2013; 1 IP address (1 host up) scanned in 22.02 seconds
    (pydev)[dev@bouteille python-nmap-lib]$

Another and last example of a simple use of the NmapProcess class. The code below prints out the scan results a la nmap

.. literalinclude:: ../examples/proc_nmap_like.py

The above code will print out the following on standard output::

    (pydev)[dev@bouteille python-nmap-lib]$ python examples/proc_nmap_like.py
    Starting Nmap 5.51 ( http://nmap.org ) at Sat May 25 00:14:54 2013
    Nmap scan report for localhost (127.0.0.1)
    Host is up.
      PORT     STATE         SERVICE
       22/tcp  open          ssh (product: OpenSSH extrainfo: protocol 2.0 version: 5.3)
       25/tcp  open          smtp (product: Postfix smtpd hostname:  bouteille.localdomain)
       80/tcp  open          http (product: nginx version: 1.0.15)
      111/tcp  open          rpcbind (version: 2-4 extrainfo: rpc #100000)
      631/tcp  open          ipp (product: CUPS version: 1.4)
    Nmap done at Sat May 25 00:15:00 2013; 1 IP address (1 host up) scanned in 6.25 seconds
    (pydev)[dev@bouteille python-nmap-lib]$

The full `source code <https://github.com/savon-noir/python-nmap-lib>`_ is available on GitHub. Please, do not hesitate to fork it and issue pull requests.

NmapProcess methods
-------------------

.. automodule:: libnmap.process
.. autoclass:: NmapProcess
    :members:
