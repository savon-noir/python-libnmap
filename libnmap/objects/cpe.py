
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
        return self._cpedict['part']

    def get_vendor(self):
        return self._cpedict['vendor']

    def get_product(self):
        return self._cpedict['product']

    def get_version(self):
        return self._cpedict['version']

    def get_update(self):
        return self._cpedict['update']

    def get_edition(self):
        return self._cpedict['edition']

    def get_language(self):
        return self._cpedict['language']

    def is_application(self):
        return (self.get_part() == '/a')

    def is_hardware(self):
        return (self.get_part() == '/h')

    def is_operating_system(self):
        return (self.get_part() == '/o')
