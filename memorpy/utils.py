import re
import struct
import typing


double = typing.NewType("double", float)
long = typing.NewType("long", int)
short = typing.NewType("short", int)
uint = typing.NewType("uint", int)
ulong = typing.NewType("ulong", int)
ushort = typing.NewType("ushort", int)

MemoryValue = typing.Union[
    double, float, int, long, short, uint, ulong, ushort, str, bytes
]


def re_to_unicode(s: str) -> str:
    newstring = ""
    for c in s:
        newstring += re.escape(c) + "\\x00"

    return newstring


def type_unpack(_type: str) -> typing.Tuple[str, int]:
    """ return the struct and the len of a particular type """
    _type = _type.lower()
    s = None
    l = None
    if _type == "short":
        s = "h"
        l = 2
    elif _type == "ushort":
        s = "H"
        l = 2
    elif _type == "int":
        s = "i"
        l = 4
    elif _type == "uint":
        s = "I"
        l = 4
    elif _type == "long":
        s = "l"
        l = 4
    elif _type == "ulong":
        s = "L"
        l = 4
    elif _type == "float":
        s = "f"
        l = 4
    elif _type == "double":
        s = "d"
        l = 8
    else:
        raise TypeError("Unknown type %s" % _type)
    return ("<" + s, l)


def hex_dump(
    data: typing.Union[bytes, str],
    addr: int = 0,
    prefix: str = "",
    ftype: str = "bytes",
) -> str:
    """
    function originally from pydbg, modified to display other types
    """
    dump = prefix
    _slice = ""
    if ftype != "bytes":
        structtype, structlen = type_unpack(ftype)
        for i in range(0, len(data), structlen):
            if addr % 16 == 0:
                dump += " "
                for char in _slice:
                    if ord(char) >= 32 and ord(char) <= 126:
                        dump += char
                    else:
                        dump += "."

                dump += "\n%s%08X: " % (prefix, addr)
                _slice = ""
            tmpval = "NaN"
            try:
                packedval = data[i : i + structlen]
                tmpval = struct.unpack(structtype, packedval)[0]  # type: ignore
            except Exception as e:
                print(e)

            if tmpval == "NaN":
                dump += "{:<15} ".format(tmpval)
            elif ftype == "float":
                dump += "{:<15.4f} ".format(tmpval)
            else:
                dump += "{:<15} ".format(tmpval)
            addr += structlen

    else:
        for byte in data:
            if addr % 16 == 0:
                dump += " "
                for char in _slice:
                    if ord(char) >= 32 and ord(char) <= 126:
                        dump += char
                    else:
                        dump += "."

                dump += "\n%s%08X: " % (prefix, addr)
                _slice = ""
            dump += "%02X " % ord(byte)  # type: ignore
            _slice += byte  # type: ignore
            addr += 1

    remainder = addr % 16
    if remainder != 0:
        dump += "   " * (16 - remainder) + " "
    for char in _slice:
        if ord(char) >= 32 and ord(char) <= 126:
            dump += char
        else:
            dump += "."

    return dump + "\n"

