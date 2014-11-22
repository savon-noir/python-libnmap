python-libnmap
==============

Code status
-----------

|Build Status|

Use cases
---------

libnmap is a python library enabling python developpers to manipulate nmap process and data.

libnmap is what you were looking for if you need to implement the following:

- automate or schedule nmap scans on a regular basis
- manipulate nmap scans results to do reporting
- compare and diff nmap scans to generate graphs
- batch process scan reports
- ...

The above uses cases will be easy to implement with the help of the libnmap modules.

libnmap modules
---------------

The lib currently offers the following modules:

- **process**: enables you to launch nmap scans
- **parse**: enables you to parse nmap reports or scan results (only XML so far) from a file, a string,...
- **report**: enables you to manipulate a parsed scan result and de/serialize scan results in a json format
- **diff**: enables you to see what changed between two scans
- **common**: contains basic nmap objects like NmapHost and NmapService. It is to note that each object can be "diff()ed" with another similar object.
- **plugins**: enables you to support datastores for your scan results directly in the "NmapReport" object. from report module:

 - mongodb: insert/get/getAll/delete
 - sqlalchemy: insert/get/getAll/delete
 - aws s3: insert/get/getAll/delete (not supported for python3 since boto is not supporting py3)
 - csv: todo (easy to implement)
 - elastic search: todo

Documentation
-------------

All the documentation is available on `read the docs`_. This documentation contains small code samples that you directly reuse.

Dependencies
------------

libnmap has by default no dependencies.

The only additional python modules you'll have to install depends if you wish to use libnmap to store reports on an exotic data store via libnmap's independents plugins.

Below the list of optional dependencies:

- `sqlalchemy`_ (+the driver ie:MySQL-python)
- `pymongo`_
- `boto`_

Python Support
--------------

The libnmap code is tested against the following python interpreters:

- Python 2.6
- Python 2.7
- Python 3.3
- Python 3.4

Install
-------

You can install libnmap via pip::

    pip install libnmap

or via git::

    $ git clone https://github.com/savon-noir/python-libnmap.git
    $ cd python-libnmap
    $ python setup.py install

Examples
--------

Some codes samples are available in the examples directory or in the `documentation`_.

Among other example, you notice an sample code pushing nmap scan reports in an ElasticSearch instance and allowing you to create fancy dashboards in Kibana like the screenshot below:

.. image:: https://github.com/savon-noir/python-libnmap/blob/es/examples/kibanalibnmap.png
    :alt: Kibanane
    :align: center

Contributors
------------

Mike @bmx0r Boutillier for S3 and SQL-Alechemy plugins and for the constructive critics. Thanks!

.. |Build Status| image:: https://travis-ci.org/savon-noir/python-libnmap.png?branch=master
   :target: https://travis-ci.org/savon-noir/python-libnmap

.. _read the docs: https://libnmap.readthedocs.org

.. _documentation: https://libnmap.readthedocs.org

.. _boto: https://github.com/boto/boto

.. _pymongo: https://github.com/mongodb/mongo-python-driver/

.. _sqlalchemy: https://github.com/zzzeek/sqlalchemy
