class CPE(object):
    """
        CPE class offers an API for basic CPE objects.
        These objects could be found in NmapService or in <os> tag
        within NmapHost.

        :todo: interpret CPE string and provide appropriate API
    """
    def __init__(self, cpestring):
        self._cpestring = cpestring

    @property
    def cpestring(self):
        """
            Accessor for the full CPE string.
        """
        return self._cpestring

    def __repr__(self):
        return self._cpestring


class NmapOSMatch(object):
    """
        NmapOSMatch is an internal class used for offering results
        from an nmap os fingerprint. This common interfaces makes
        a compatibility between old nmap xml (<1.04) and new nmap
        xml versions (used in nmapv6 for instance).

        In previous xml version, osclass tags from nmap fingerprints
        were not directly mapped to a osmatch. In new xml version,
        osclass could be embedded in osmatch tag.

        The approach to solve this is to create a common class
        which will, for older xml version, match based on the accuracy
        osclass to an osmatch. If no match, an osmatch will be made up
        from a concat of os class attributes: vendor and osfamily.
        Unmatched osclass will have a line attribute of -1.

        More info, see issue #26 or http://seclists.org/nmap-dev/2012/q2/252
    """
    def __init__(self, osmatch_dict):
        _osmatch_dict = osmatch_dict['osmatch']
        if('name' not in _osmatch_dict or
           'line' not in _osmatch_dict or
           'accuracy' not in _osmatch_dict):
            raise Exception("Cannot create NmapOSClass: missing required key")

        self._name = _osmatch_dict['name']
        self._line = _osmatch_dict['line']
        self._accuracy = _osmatch_dict['accuracy']

        # create osclass list
        self._osclasses = []
        for _osclass in osmatch_dict['osclasses']:
            try:
                _osclassobj = NmapOSClass(_osclass)
            except:
                raise Exception("Could not create NmapOSClass object")
            self._osclasses.append(_osclassobj)

    def add_class(self, class_dict):
        """
            Add a NmapOSClass object to the OSMatch object. This method is
            useful to implement compatibility with older versions of NMAP
            by providing a common interface to access os fingerprint data.
        """
        if 'osclass' in class_dict:
            self.__osclasses.append(class_dict)
        else:
            raise Exception("Cannot add: no osclass data in provided dict")

    @property
    def osclasses(self):
        """
            Accessor for all NmapOSClass objects matching with this OS Match
        """
        return self._osclasses

    @property
    def name(self):
        """
            Accessor for name attribute (e.g.: Linux 2.4.26 (Slackware 10.0.0))
        """
        return self._name

    @property
    def line(self):
        """
            Accessor for line attribute as integer. value equals -1 if this
            osmatch holds orphans NmapOSClass objects. This could happen with
            older version of nmap xml engine (<1.04 (e.g: nmapv6)).

            :return: int
        """
        return int(self._line)

    @property
    def accuracy(self):
        """
            Accessor for accuracy

            :return: int
        """
        return int(self._accuracy)

    def __repr__(self):
        rval = "{0}: {1}".format(self.name, self.accuracy)
        for _osclass in self._osclasses:
            rval += "\r\n  |__ os class: {0}".format(str(_osclass))
        return rval


class NmapOSClass(object):
    """
        NmapOSClass offers an unified API to access data from analysed
        osclass tag. As implemented in libnmap and newer version of nmap,
        osclass objects will always be embedded in a NmapOSMatch.
        Unmatched NmapOSClass will be stored in "dummy" NmapOSMatch objects
        which will have the particularity of have a line attribute of -1.
        On top of this, NmapOSClass will have optional CPE objects
        embedded.
    """
    def __init__(self, osclass_dict):
        _osclass = osclass_dict['osclass']
        if('vendor' not in _osclass or
           'osfamily' not in _osclass or
           'accuracy' not in _osclass):
            raise Exception("Wrong osclass structure: missing required key")

        self._vendor = _osclass['vendor']
        self._osfamily = _osclass['osfamily']
        self._accuracy = _osclass['accuracy']

        self._osgen = ''
        self._type = ''
        # optional data
        if 'osgen' in _osclass:
            self._osgen = _osclass['osgen']
        if 'type' in _osclass:
            self._type = _osclass['type']

        self._cpelist = []
        for _cpe in osclass_dict['cpe']:
            self._cpelist.append(CPE(_cpe))

    @property
    def vendor(self):
        """
            Accessor for vendor information (Microsoft, Linux,...)

            :return: string
        """
        return self._vendor

    @property
    def osfamily(self):
        """
            Accessor for OS family information (Windows, Linux,...)

            :return: string
        """
        return self._osfamily

    @property
    def accuracy(self):
        """
            Accessor for OS class detection accuracy (int)

            :return: int
        """
        return int(self._accuracy)

    @property
    def osgen(self):
        """
            Accessor for OS class generation (7, 8, 2.4.X,...).

            :return: string
        """
        return self._osgen

    @property
    def type(self):
        """
            Accessor for OS class type (general purpose,...)

            :return: string
        """
        return self._type

    def __repr__(self):
        rval = "{0}: {1}, {2}".format(self.type, self.vendor, self.osfamily)
        if len(self.osgen):
            rval += "({0})".format(self.osgen)
        for _cpe in self._cpelist:
            rval += "\r\n    |__ {0}".format(str(_cpe))
        return rval


class NmapOSFingerprint(object):
    """
        NmapOSFingerprint is a easier API for using os fingerprinting.
        Data for OS fingerprint (<os> tag) is instanciated from
        a NmapOSFingerprint which is accessible in NmapHost via NmapHost.os
    """
    def __init__(self, osfp_data):
        self.__osmatches = []
        self.__ports_used = []
        self.__fingerprints = []
        _osclasses = []

        if 'osmatches' in osfp_data:
            for _osmatch in osfp_data['osmatches']:
                _osmatch_obj = NmapOSMatch(_osmatch)
                self.__osmatches.append(_osmatch_obj)
        if 'osclasses' in osfp_data:
            _osclasses = osfp_data['osclasses']
        if 'ports_used' in osfp_data:
            self.__ports_used = osfp_data['ports_used']
        if 'osfingerprints' in osfp_data:
            for _osfp in osfp_data['osfingerprints']:
                if 'fingerprint' in _osfp:
                    self.__fingerprints.append(_osfp['fingerprint'])

    @property
    def osmatches(self):
        return self.__osmatches

    @property
    def fingerprint(self):
        return "\r\n".join(self.__fingerprints)

    @property
    def fingerprints(self):
        return self.__fingerprints

#        for _osclass in _osclasses:
#            _matched = self.is_matched(_osclass)
#
#        __sortfct = lambda osent: int(osent['accuracy'])
#        if 'osmatch' in osfp_data:
#            try:
#                self.__osmatch = sorted(osfp_data['osmatch'],
#                                        key=__sortfct,
#                                        reverse=True)
#            except (KeyError, TypeError):
#                self.__osmatch = []
#
#        if 'osclass' in osfp_data:
#            try:
#                self.__osclass = sorted(osfp_data['osclass'],
#                                        key=__sortfct,
#                                        reverse=True)
#            except (KeyError, TypeError):
#                self.__osclass = []

    def osmatch(self, min_accuracy=90):
        os_array = []
        for match_entry in self.__osmatch:
            try:
                if int(match_entry['accuracy']) >= min_accuracy:
                    os_array.append(match_entry['name'])
            except (KeyError, TypeError):
                pass
        return os_array

    def osclass(self, min_accuracy=90):
        os_array = []
        for osclass_entry in self.__osclass:
            try:
                if int(osclass_entry['accuracy']) >= min_accuracy:
                    _relevantkeys = ['type', 'vendor', 'osfamily', 'osgen']
                    _ftstr = "|".join([vkey + ": " + osclass_entry[vkey]
                                      for vkey in osclass_entry
                                      if vkey in _relevantkeys])
                    os_array.append(_ftstr)
            except (KeyError, TypeError):
                pass
        return os_array

    def __repr__(self):
        rval = ""
        for _osmatch in self.osmatches:
            rval += "\r\n{0}".format(_osmatch)
        rval += "Fingerprints: ".format(self.fingerprint)
        return rval
