from distutils.core import setup

setup(
    name='libnmap',
    version='0.1',
    author='Ronald Bister',
    author_email='mini.pelle@gmail.com',
    packages=['libnmap', 'libnmap.test'],
    url='http://pypi.python.org/pypi/pynmap/',
    license='LICENSE.txt',
    description='A Python NMAP librairy enabling you to launch nmap scans and parse XML scan results',
    long_description=open('README.txt').read(),
)
