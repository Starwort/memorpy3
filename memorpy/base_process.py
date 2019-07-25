from . import utils
import struct

""" Base class for process not linked to any platform """


class ProcessException(Exception):
    pass


class BaseProcess:
    def __init__(self, *args, **kwargs):
        """ Create and Open a process object from its pid or from its name """
        self.h_process = None
        self.pid = None
        self.isProcessOpen = False
        self.buffer = None
        self.bufferlen = 0

    def __del__(self):
        self.close()

    def close(self) -> None:
        pass

    def iter_region(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def write_bytes(self, address: int, data: bytes) -> bool:
        raise NotImplementedError

    def read_bytes(self, address: int, _bytes: int = 4) -> bytes:
        raise NotImplementedError

    def get_symbolic_name(self, address: int) -> str:
        return "0x%08X" % int(address)

    def read(
        self, address: int, _type: str = "uint", maxlen: int = 50, errors: str = "raise"
    ) -> utils.MemoryValue:
        if _type == "s" or _type == "string":
            s = self.read_bytes(int(address), _bytes=maxlen)
            news = ""
            for c in s:
                if c == 0:
                    return news
                news += chr(c)
            if errors == "ignore":
                return news
            raise ProcessException("string > maxlen")
        else:
            if _type == "bytes" or _type == "b":
                return self.read_bytes(int(address), _bytes=maxlen)
            format, l = utils.type_unpack(_type)
            return struct.unpack(format, self.read_bytes(int(address), _bytes=l))[0]

    def write(self, address, data, _type="uint") -> bool:
        if _type != "bytes":
            s, _ = utils.type_unpack(_type)
            return self.write_bytes(int(address), struct.pack(s, data))
        else:
            return self.write_bytes(int(address), data)
