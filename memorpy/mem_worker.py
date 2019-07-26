import sys
import string
import re
import logging
from . import process
from . import utils
import struct
from .address import Address
from .base_process import ProcessException
import traceback
import binascii
from .structures import *  # pylint: disable=unused-wildcard-import

logger = logging.getLogger("memorpy")

REGEX_TYPE = type(re.compile("^plop$"))


class MemWorker(object):
    def __init__(
        self, pid=None, name=None, end_offset=None, start_offset=None, debug=True
    ):
        self.process = process.Process(name=name, pid=pid, debug=debug)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.process.close()

    def Address(self, value, default_type="uint"):
        """ wrapper to instanciate an Address class for the memworker.process"""
        return Address(value, process=self.process, default_type=default_type)

    def umem_replace(self, regex, replace):
        """ like search_replace_mem but works with unicode strings """
        regex = utils.re_to_unicode(regex)
        replace = replace.encode("utf-16-le")
        return self.mem_replace(re.compile(regex, re.UNICODE), replace)

    def mem_replace(self, regex, replace):
        """ search memory for a pattern and replace all found occurrences """
        allWritesSucceed = True
        for _, start_offset in self.mem_search(regex, ftype="re"):
            if self.process.write_bytes(start_offset, replace) == 1:
                logger.debug("Write at offset %s succeeded !" % start_offset)
            else:
                allWritesSucceed = False
                logger.debug("Write at offset %s failed !" % start_offset)

        return allWritesSucceed

    def umem_search(self, regex):
        """ like mem_search but works with unicode strings """
        regex = utils.re_to_unicode(regex)
        for _, i in self.mem_search(str(regex), ftype="re"):
            yield i

    def group_search(self, group, start_offset=None, end_offset=None):
        regex = ""
        for value, type in group:
            if type == "f" or type == "float":
                f = struct.pack("<f", float(value))
                regex += ".." + f[2:4]
            else:
                raise NotImplementedError("unknown type %s" % type)

        return self.mem_search(
            regex, ftype="re", start_offset=start_offset, end_offset=end_offset
        )

    def search_address(self, addr):
        a = "%08X" % addr
        logger.debug("searching address %s" % a)
        regex = ""
        for i in range(len(a) - 2, -1, -2):
            regex += binascii.unhexlify(a[i : i + 2])

        for _, a in self.mem_search(re.escape(regex), ftype="re"):
            yield a

    def parse_re_function(self, b, value, offset):
        for name, regex in value:
            for res in regex.finditer(b):
                yield name, self.Address(offset + res.start(), "bytes")
                """
                index = b.find(res)
                while index != -1:
                    soffset = offset + index
                    if soffset not in duplicates_cache:
                        duplicates_cache.add(soffset)
                        yield name, self.Address(soffset, 'bytes')
                    index = b.find(res, index + len(res))
                """

    def parse_float_function(self, b, value, offset):
        for index in range(0, len(b)):
            try:
                structtype, _ = utils.type_unpack("float")
                tmpval = struct.unpack(structtype, b[index : index + 4])[0]
                if int(value) == int(tmpval):
                    soffset = offset + index
                    yield self.Address(soffset, "float")
            except Exception:
                pass

    def parse_named_groups_function(self, b, value, offset=None):
        for name, regex in value:
            for res in regex.finditer(b):
                yield name, res.groupdict()

    def parse_groups_function(self, b, value, offset=None):
        for name, regex in value:
            for res in regex.finditer(b):
                yield name, res.groups()

    def parse_any_function(self, b, value, offset):
        index = b.find(value)
        while index != -1:
            soffset = offset + index
            yield self.Address(soffset, "bytes")
            index = b.find(value, index + 1)

    def mem_search(
        self,
        value,
        ftype="match",
        protec=PAGE_READWRITE | PAGE_READONLY,
        optimizations=None,
        start_offset=None,
        end_offset=None,
    ):
        """ 
                iterator returning all indexes where the pattern has been found
        """

        # pre-compile regex to run faster
        if ftype == "re" or ftype == "groups" or ftype == "ngroups":

            # value should be an array of regex
            if not isinstance(value, list):
                value = [value]

            tmp = []
            for reg in value:
                if isinstance(reg, tuple):
                    name = reg[0]
                    if not isinstance(reg[1], REGEX_TYPE):
                        regex = re.compile(reg[1], re.IGNORECASE)
                    else:
                        regex = reg[1]
                elif isinstance(reg, REGEX_TYPE):
                    name = ""
                    regex = reg
                else:
                    name = ""
                    regex = re.compile(reg, re.IGNORECASE)

                tmp.append((name, regex))
            value = tmp

        elif ftype not in ["match", "group", "re", "groups", "ngroups", "lambda"]:
            structtype, _ = utils.type_unpack(ftype)
            value = struct.pack(structtype, value)

        # different functions avoid if statement before parsing the buffer
        if ftype == "re":
            func = self.parse_re_function

        elif ftype == "groups":
            func = self.parse_groups_function

        elif ftype == "ngroups":
            func = self.parse_named_groups_function

        elif ftype == "float":
            func = self.parse_float_function
        elif ftype == "lambda":  # use a custom function
            func = value
        else:
            func = self.parse_any_function

        if not self.process.isProcessOpen:
            raise ProcessException(
                "Can't read_bytes, process %s is not open" % (self.process.pid)
            )

        for offset, chunk_size in self.process.iter_region(
            start_offset=start_offset,
            end_offset=end_offset,
            protec=protec,
            optimizations=optimizations,
        ):
            b = b""
            current_offset = offset
            chunk_read = 0
            chunk_exc = False
            while chunk_read < chunk_size:
                try:
                    b += self.process.read_bytes(current_offset, chunk_size)
                except IOError as e:
                    traceback.print_exc()
                    if e.errno == 13:
                        raise
                    else:
                        logger.warning(e)
                    chunk_exc = True
                    break
                except Exception as e:
                    logger.warning(e)
                    chunk_exc = True
                    break
                finally:
                    current_offset += chunk_size
                    chunk_read += chunk_size

            if chunk_exc:
                continue

            if b:
                if ftype == "lambda":
                    for res in func(b, offset):
                        yield res
                else:
                    for res in func(b, value, offset):
                        yield res
