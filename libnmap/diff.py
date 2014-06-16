# -*- coding: utf-8 -*-


class DictDiffer(object):
    """
        Calculate the difference between two dictionaries as:
        (1) items added
        (2) items removed
        (3) keys same in both but changed values
        (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict = current_dict
        self.past_dict = past_dict
        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return (set(o for o in self.intersect
                if self.past_dict[o] != self.current_dict[o]))

    def unchanged(self):
        return (set(o for o in self.intersect
                if self.past_dict[o] == self.current_dict[o]))


class NmapDiff(DictDiffer):
    """
        NmapDiff compares two objects of same type to enable the user to check:

        - what has changed
        - what has been added
        - what has been removed
        - what was kept unchanged

        NmapDiff inherit from DictDiffer which makes the actual comparaison.
        The different methods from DictDiffer used by NmapDiff are the
        following:

        - NmapDiff.changed()
        - NmapDiff.added()
        - NmapDiff.removed()
        - NmapDiff.unchanged()

        Each of the returns a python set() of key which have changed in the
        compared objects. To check the different keys that could be returned,
        refer to the get_dict() method of the objects you which to
        compare (i.e: libnmap.objects.NmapHost, NmapService,...).
    """
    def __init__(self, nmap_obj1, nmap_obj2):
        """
            Constructor of NmapDiff:

            - Checks if the two objects are of the same class
            - Checks if the objects are "comparable" via a call to id() (dirty)
            - Inherits from DictDiffer and
        """
        if(nmap_obj1.__class__ != nmap_obj2.__class__ or
           nmap_obj1.id != nmap_obj2.id):
            raise NmapDiffException("Comparing objects with non-matching id")

        self.object1 = nmap_obj1.get_dict()
        self.object2 = nmap_obj2.get_dict()

        DictDiffer.__init__(self, self.object1, self.object2)

    def __repr__(self):
        return ("added: [{0}] -- changed: [{1}] -- "
                "unchanged: [{2}] -- removed [{3}]".format(self.added(),
                                                           self.changed(),
                                                           self.unchanged(),
                                                           self.removed()))


class NmapDiffException(Exception):
    def __init__(self, msg):
        self.msg = msg
