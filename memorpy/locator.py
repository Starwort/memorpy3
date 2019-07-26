import copy
import time
from .address import Address
import struct


class Locator(object):
    """ 
            take a memoryworker and a type to search
            then you can feed the locator with values and it will reduce the addresses possibilities
    """

    def __init__(self, mw, type="unknown", start=None, end=None):
        self.mw = mw
        self.type = type
        self.last_iteration = {}
        self.last_value = None
        self.start = start
        self.end = end

    def find(self, value, erase_last=True):
        return self.feed(value, erase_last)

    def feed(self, value, erase_last=True):
        self.last_value = value
        new_iter = copy.copy(self.last_iteration)
        if self.type == "unknown":
            all_types = [
                "uint",
                "int",
                "long",
                "ulong",
                "float",
                "double",
                "short",
                "ushort",
            ]
        else:
            all_types = [self.type]
        for _type in all_types:
            if _type not in new_iter:
                try:
                    new_iter[_type] = [
                        Address(x, self.mw.process, _type)
                        for x in self.mw.mem_search(
                            value, _type, start_offset=self.start, end_offset=self.end
                        )
                    ]
                except struct.error:
                    new_iter[_type] = []
            else:
                l = []
                for address in new_iter[_type]:
                    try:
                        found = self.mw.process.read(address, _type)
                        if int(found) == int(value):
                            l.append(Address(address, self.mw.process, _type))
                    except Exception:
                        pass

                new_iter[_type] = l

        if erase_last:
            del self.last_iteration
            self.last_iteration = new_iter
        return new_iter

    def get_addresses(self):
        return self.last_iteration

    def diff(self, erase_last=False):
        return self.get_modified_addr(erase_last)

    def get_modified_addr(self, erase_last=False):
        last = self.last_iteration
        new = self.feed(self.last_value, erase_last=erase_last)
        ret = {}
        for type, l in last.iteritems():
            typeset = set(new[type])
            for addr in l:
                if addr not in typeset:
                    if type not in ret:
                        ret[type] = []
                    ret[type].append(addr)

        return ret
