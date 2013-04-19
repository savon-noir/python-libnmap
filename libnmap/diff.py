#!/usr/bin/env python


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
    def __init__(self, nmap_obj1, nmap_obj2):
        if nmap_obj1.id != nmap_obj2.id:
            raise NmapDiffException("Comparing objects with non-matching id")

        self.object1 = nmap_obj1.get_dict()
        self.object2 = nmap_obj2.get_dict()

        DictDiffer.__init__(self, self.object1, self.object2)

    def __repr__(self):
        return ('added: [{0}] -- changed: [{1}] -- \
                 unchanged: [{2}] -- removed [{3}]'.format(self.added(),
                                                           self.changed(),
                                                           self.unchanged(),
                                                           self.removed()))


class NmapDiffException(Exception):
    def __init__(self, msg):
        self.msg = msg
