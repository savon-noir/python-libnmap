libnmap.parser
==============

Using libnmap.parser module
---------------------------

This modules enables you to parse nmap scans' output. For now on, only XML parsing is supported. NmapParser is a factory which will return a NmapReport, NmapHost or NmapService object.
All these objects' API are documented.
The NmapParser should never be instanciated and only the following methods should be called:

- NmapParser.parse(string)
- NmapParser.parse_fromfile(file_path)
- NmapParser.parse_fromstring(string)

All of the above methods can receive as input:

- a full XML nmap scan result and returns a NmapReport object
- a scanned host in XML (<host>...</host> tag) and will return a NmapHost object
- a list of scanned services in XML (<ports>...</ports> tag) and will return a python array of NmapService objects
- a scanned service in XML (<port>...</port> tag) and will return a NmapService object

Small example::

    from libnmap.parser import NmapParser
    
    nmap_report = NmapParser.parse_fromfile('libnmap/test/files/1_os_banner_scripts.xml')
    print "Nmap scan summary: {0}".format(nmap_report.summary)

Basic usage from a processed scan::

    from libnmap.process import NmapProcess
    from libnmap.parser import NmapParser
    
    nm = NmapProcess("127.0.0.1, scanme.nmap.org")
    nm.run()
    
    nmap_report = NmapParser.parse(nm.stdout)
    
    for scanned_hosts in nmap_report.hosts:
        print scanned_hosts

For more details on using the results from NmapParser, refer to the API of class: NmapReport, NmapHost, NmapService.

NmapParser methods
------------------

.. automodule:: libnmap.parser
.. autoclass:: NmapParser
    :members:
