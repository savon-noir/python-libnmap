from distutils.core import setup

with open("README.rst") as rfile:
    long_description = rfile.read()

setup(
    name='python-libnmap',
    version='0.2.1',
    author='Ronald Bister',
    author_email='mini.pelle@gmail.com',
    packages=['libnmap', 'libnmap.plugins', 'libnmap.test'],
    url='http://pypi.python.org/pypi/libnmap/',
    license='LICENSE.txt',
    description=('A Python NMAP library enabling you to launch nmap scans',
                 'parse and compare (diff) scan results'),
    long_description=long_description
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Programming Language :: Python :: 2.6",
                 "Programming Language :: Python :: 2.7",
                 "Topic :: System :: Networking",
                 "Topic :: Software Development :: Libraries :: Python Modules"],
)
