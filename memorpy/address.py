from . import utils
import typing

if typing.TYPE_CHECKING:
    from .base_process import BaseProcess
else:
    BaseProcess = None


class AddressException(Exception):
    pass


class Address(object):
    """ this class is used to have better representation of memory addresses """

    def __init__(self, value: int, process: BaseProcess, default_type: str = "uint"):
        self.value = int(value)
        self.process = process
        self.default_type = default_type
        self.symbolic_name = None

    @typing.overload
    def read(self, maxlen: int = None, errors: str = "raise") -> utils.MemoryValue:
        ...

    @typing.overload
    def read(  # pylint: disable=function-redefined
        self, _type: str = None, maxlen: int = None, errors: str = "raise"
    ) -> utils.MemoryValue:
        ...

    def read(  # type: ignore pylint: disable=function-redefined
        self, _type=None, maxlen=None, errors: str = "raise"
    ) -> utils.MemoryValue:
        if maxlen is None:
            try:
                int(_type)
                maxlen = int(_type)
                _type = None
            except:
                pass

        if not _type:
            _type = self.default_type
        if not maxlen:
            return self.process.read(self.value, _type=_type, errors=errors)
        else:
            return self.process.read(
                self.value, _type=_type, maxlen=maxlen, errors=errors
            )

    def write(self, data: utils.MemoryValue, _type: str = None) -> bool:
        if not _type:
            _type = self.default_type
        return self.process.write(self.value, data, _type=_type)

    def symbol(self) -> str:
        return self.process.get_symbolic_name(self.value)

    def get_instruction(self):
        return self.process.get_instruction(self.value)

    def dump(self, ftype: str = "bytes", size: int = 512, before: int = 32) -> str:
        buf = self.process.read_bytes(self.value - before, size)
        return utils.hex_dump(buf, self.value - before, ftype=ftype)

    def __nonzero__(self):
        return self.value is not None and self.value != 0

    def __add__(self, other):
        return Address(self.value + int(other), self.process, self.default_type)

    def __iadd__(self, other):
        self.value += int(other)
        return self

    def __sub__(self, other):
        return Address(self.value - int(other), self.process, self.default_type)

    def __isub__(self, other):
        self.value -= int(other)
        return self

    def __repr__(self):
        if not self.symbolic_name:
            self.symbolic_name = self.symbol()
        return str("<Addr: %s" % self.symbolic_name + ">")

    def __str__(self):
        if not self.symbolic_name:
            self.symbolic_name = self.symbol()
        return str(
            "<Addr: %s" % self.symbolic_name
            + ' : "%s" (%s)>'
            % (str(self.read()).encode("string_escape"), self.default_type)
        )

    def __int__(self):
        return int(self.value)

    def __hex__(self):
        return hex(self.value)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = int(value)

    def __lt__(self, other):
        return self.value < int(other)

    def __le__(self, other):
        return self.value <= int(other)

    def __eq__(self, other):
        return self.value == int(other)

    def __ne__(self, other):
        return self.value != int(other)

    def __gt__(self, other):
        return self.value > int(other)

    def __ge__(self, other):
        return self.value >= int(other)
