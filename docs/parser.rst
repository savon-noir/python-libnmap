libnmap.parser
==============

Security note for libnmap.parser
--------------------------------

**TLDR:** if you are importing/parsing untrusted XML scan outputs with python-libnmap, install defusedxml library: 

.. code-block:: bash

    ronald@brouette:~/dev$ pip install defusedxml

By default, python-libnmap's parser module does not enforces an extra XML parser module than the one provided in the python core distribution.

In versions previous to 0.7.2, by default, the `ElementTree XML API was used <https://docs.python.org/3/library/xml.etree.elementtree.html>`_.
This XML library is vulnerable to several `XML External Entities attacks <https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing>`_ which may lead to:

- Denial of Service attacks
- Remote and local files inclusions
- Remote code execution

This implies, de facto, that parsing any untrusted XML file could result in any of the above. 

Fortunately, one of the python core developer is maintaining an alternative Python XML parsing library: `defusedxml <https://pypi.org/project/defusedxml/>`_ which addresses all the above vulnerabilities.

Since the above vulnerabilities will only affect you if you are parsing untrusted XML scan outputs, by default, the defusedxml library is not enforced. 
But if the defusedxml library is installed, it will be the preferred XML parser picked by python-libnmap.

Consider the following lines from libnmap.parser module:

.. literalinclude:: ../libnmap/parser.py
   :linenos:
   :lines: 3-10


- Line 4 first tries to import defusedxml 
- if it fails, it then tries to load cElementTree (known to be more performant)
- if it fails, it then defaults to XML ElementTree.

Purpose of libnmap.parser
-------------------------

This modules enables you to parse nmap scans' output. For now on, only XML parsing is supported. NmapParser is a factory which will return a NmapReport, NmapHost or NmapService object.
All these objects' API are documented.

The module is capable of parsing:

- a complete nmap XML scan report
- an incomplete/interrupted nmap XML scan report
- partial nmap xml tags: <host>, <ports> and <port>

Input the above capabilities could be either a string or a file path.

Based on the provided data, NmapParse.parse() could return the following:

- NmapReport object: in case a full nmap xml/dict report was prodivded
- NmapHost object: in case a nmap xml <host> section was provided
- NmapService object: in case a nmap xml <port> section was provided
- Python dict with following keys: ports and extraports; python lists.

Using libnmap.parser module
---------------------------

NmapParser parse the whole data and returns nmap objects usable via their documented API.

The NmapParser should never be instanciated and only the following methods should be called:

- NmapParser.parse(string)
- NmapParser.parse_fromfile(file_path)
- NmapParser.parse_fromstring(string)

All of the above methods can receive as input:

- a full XML nmap scan result and returns a NmapReport object
- a scanned host in XML (<host>...</host> tag) and will return a NmapHost object
- a list of scanned services in XML (<ports>...</ports> tag) and will return a python array of NmapService objects
- a scanned service in XML (<port>...</port> tag) and will return a NmapService object

Small example:

.. code-block:: python

    from libnmap.parser import NmapParser
    
    nmap_report = NmapParser.parse_fromfile('libnmap/test/files/1_os_banner_scripts.xml')
    print "Nmap scan summary: {0}".format(nmap_report.summary)

Basic usage from a processed scan:

.. code-block:: python

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
