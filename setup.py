from distutils.core import setup

with open("README.rst") as rfile:
    long_description = rfile.read()

setup(
    name='python-libnmap',
    version='0.5.0',
    author='Ronald Bister',
    author_email='mini.pelle@gmail.com',
    packages=['libnmap', 'libnmap.plugins', 'libnmap.objects'],
    url='http://pypi.python.org/pypi/python-libnmap/',
    license='Creative Common "Attribution" license (CC-BY) v3',
    description=('Python NMAP library enabling you to start async nmap tasks, '
                 'parse and compare/diff scan results'),
    long_description=long_description,
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 2.6",
                 "Programming Language :: Python :: 2.7",
                 "Topic :: System :: Networking"]
)
