# -*- coding: utf-8 -*-


class CPE(object):
    """
        CPE class offers an API for basic CPE objects.
        These objects could be found in NmapService or in <os> tag
        within NmapHost.

        :todo: interpret CPE string and provide appropriate API
    """
    def __init__(self, cpestring):
        self._cpestring = cpestring
        self.cpedict = {}

        zk = ['cpe', 'part', 'vendor', 'product', 'version',
              'update', 'edition', 'language']
        self._cpedict = dict((k, '') for k in zk)
        splitup = cpestring.split(':')
        self._cpedict.update(dict(zip(zk, splitup)))

    @property
    def cpestring(self):
        """
            Accessor for the full CPE string.
        """
        return self._cpestring

    def __repr__(self):
        return self._cpestring

    def get_part(self):
        """
            Returns the cpe part (/o, /h, /a)
        """
        return self._cpedict['part']

    def get_vendor(self):
        """
            Returns the vendor name
        """
        return self._cpedict['vendor']

    def get_product(self):
        """
            Returns the product name
        """
        return self._cpedict['product']

    def get_version(self):
        """
            Returns the version of the cpe
        """
        return self._cpedict['version']

    def get_update(self):
        """
            Returns the update version
        """
        return self._cpedict['update']

    def get_edition(self):
        """
            Returns the cpe edition
        """
        return self._cpedict['edition']

    def get_language(self):
        """
            Returns the cpe language
        """
        return self._cpedict['language']

    def is_application(self):
        """
            Returns True if cpe describes an application
        """
        return (self.get_part() == '/a')

    def is_hardware(self):
        """
            Returns True if cpe describes a hardware
        """
        return (self.get_part() == '/h')

    def is_operating_system(self):
        """
            Returns True if cpe describes an operating system
        """
        return (self.get_part() == '/o')
