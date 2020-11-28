# python-libnmap

## Code status

![preflight-check](https://github.com/savon-noir/python-libnmap/workflows/Preflight%20Check/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/savon-noir/python-libnmap/badge.svg?branch=master)](https://coveralls.io/github/savon-noir/python-libnmap?branch=master)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Use cases

libnmap is a python library enabling python developers to manipulate nmap process and data.

libnmap is what you were looking for if you need to implement the following:

- automate or schedule nmap scans on a regular basis
- manipulate nmap scans results to do reporting
- compare and diff nmap scans to generate graphs
- batch process scan reports
- ...

The above uses cases will be easy to implement with the help of the libnmap modules.

## libnmap modules

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

## Documentation

All the documentation is available on [read the docs](https://libnmap.readthedocs.org). This documentation contains small code samples that you directly reuse.

## Dependencies

libnmap has by default no dependencies.

The only additional python modules you'll have to install depends if you wish to use libnmap to store reports on an exotic data store via libnmap's independents plugins.

Below the list of optional dependencies:

- [sqlalchemy](https://github.com/zzzeek/sqlalchemy) (+the driver ie:MySQL-python)
- [pymongo](https://github.com/mongodb/mongo-python-driver/)
- [boto](https://github.com/boto/boto)

## Python Support

The libnmap code is tested against the following python interpreters:

- Python 2.6
- Python 2.7
- Python 3.3
- Python 3.4
- Python 3.5
- Python 3.6
- Python 3.7
- Python 3.8

## Install

You can install libnmap via pip:

```bash
ronald@brouette:~$ pip install python-libnmap
```

or via git and dist utils (à l'ancienne):

```bash
ronald@brouette:~$ git clone https://github.com/savon-noir/python-libnmap.git
ronald@brouette:~$ cd python-libnmap
ronald@brouette:~$ python setup.py install
```

or via git and pip:

```bash
ronald@brouette:~$ git clone https://github.com/savon-noir/python-libnmap.git
ronald@brouette:~$ cd python-libnmap
ronald@brouette:~$ pip install .
```

## Examples

Some codes samples are available in the examples directory or in the [documentation](https://libnmap.readthedocs.org).

Among other example, you notice an sample code pushing nmap scan reports in an ElasticSearch instance and allowing you to create fancy dashboards in Kibana like the screenshot below:

![Kibanane](https://github.com/savon-noir/python-libnmap/blob/es/examples/kibanalibnmap.png)

## Contributors

Mike @bmx0r Boutillier for S3 and SQL-Alechemy plugins and for the constructive critics. Thanks!
