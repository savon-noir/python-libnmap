from distutils.core import setup

setup(
    name='libnmap',
    version='0.2',
    author='Ronald Bister',
    author_email='mini.pelle@gmail.com',
    packages=['libnmap', 'libnmap.plugins', 'libnmap.test'],
    url='http://pypi.python.org/pypi/libnmap/',
    license='LICENSE.txt',
    description="""A Python NMAP librairy enabling you to launch nmap scans,
                 parse and compare (diff) scan results""",
    long_description=open('README.md').read(),
)
