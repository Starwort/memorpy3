# memorpy3

Python 3 library using ctypes to search/edit windows/linux/OSX/SunOS programs' memory.
Port of [memorpy](https://github.com/n1nj4sec/memorpy)

## This library uses Semantic Versioning

See what this means [here](https://semver.org/)

## Install

```bash
pip install memorpy
```

(ensure that pip uses python3 - on some systems `pip3` or `python3 -m pip` is required)

## Usage examples

In this example, open a notepad.exe and type in some text we will edit from memory!

```python
>>> from memorpy import *
>>> mw = MemWorker(pid=3856)  # you can also select a process by its name with the kwarg name=
>>> l = [x for x in mw.umem_search("hello")]
>>> l
[('', <Addr: 0x003287B0>)]
>>> a = l[0][1]
>>> a
<Addr: 0x003287B0>
>>> a+4
<Addr: 0x003287B4>
>>> print(a)
<Addr: 0x003287B0 : b'h\x00e\x00l\x00l\x00o\x00 \x00t\x00h\x00i\x00s\x00 \x00i\x00s\x00 \x00a\x00 \x00m\x00e\x00s\x00s\x00a\x00g\x00e\x00 \x00I\x00'>
>>> a.dump()
"00328790: 46 00 72 00 61 00 6E 00 63 00 65 00 29 00 00 00  F.r.a.n.c.e.)...\n003287A0: 00 00 00 00 00 00 00 00 F3 8F 57 0C 7F 6A 00 10  ..........W..j..\n003287B0: 63 00 6F 00 75 00 63 00 6F 00 75 00 20 00 74 00  c.o.u.c.o.u. .t.\n003287C0: 68 00 69 00 73 00 20 00 69 00 73 00 20 00 61 00  h.i.s. .i.s. .a.\n003287D0: 20 00 6D 00 65 00 73 00 73 00 61 00 67 00 65 00   .m.e.s.s.a.g.e.\n003287E0: 20 00 49 00 20 00 74 00 79 00 70 00 65 00 64 00   .I. .t.y.p.e.d.\n003287F0: 20 00 69 00 6E 00 20 00 6E 00 6F 00 74 00 65 00   .i.n. .n.o.t.e.\n00328800: 70 00 61 00 64 00 2E 00 65 00 78 00 65 00 20 00  p.a.d...e.x.e. .\n00328810: 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  !...............\n00328820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n00328830: 00 00 00 00 04 00 27 00 F7 8F 74 2B 6A 6A 00 00  ......'...t+jj..\n00328840: 30 7A 32 00 C0 8B 32 00 00 00 00 00 00 00 00 00  0z2...2.........\n00328850: 01 00 01 00 01 01 00 00 00 00 00 00 00 00 00 00  ................\n00328860: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n00328870: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n00328880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n00328890: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n003288A0: 01 00 00 01 00 00 01 00 00 00 00 01 00 00 00 00  ................\n003288B0: 07 00 00 07 59 6A 00 00 B8 79 32 00 E8 35 32 00  ....Yj...y2..52.\n003288C0: 50 54 9D ED E6 EB 55 42 82 89 F8 A3 1E 68 72 28  PT....UB.....hr(\n003288D0: 03 00 00 03 7F 6A 00 00 C0 8B 32 00 E8 35 32 00  .....j....2..52.\n003288E0: AA BA 43 9F 5C 80 8F 67 E2 8F 75 3F 6E 6A 00 0C  ..C.\..g..u?nj..\n003288F0: F0 FE 30 00 70 FE 30 00 F0 FD 30 00 1D 17 ED 00  ..0.p.0...0.....\n00328900: B6 8F 75 6B 7B 6A 00 08 00 00 00 00 00 00 00 00  ..uk{j..........\n00328910: 11 10 0A 61 00 00 00 00 00 00 00 00 A0 00 00 00  ...a............\n00328920: 0D 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n00328930: 00 00 80 41 00 00 80 41 00 00 80 3D 00 00 80 3D  ...A...A...=...=\n00328940: 00 00 D0 00 00 00 30 00 1E FF 20 1F 00 00 00 00  ......0... .....\n00328950: 71 80 0E 00 30 00 30 00 30 00 30 00 30 00 30 00  q...0.0.0.0.0.0.\n00328960: 30 00 30 00 30 00 30 00 30 00 30 00 30 00 30 00  0.0.0.0.0.0.0.0.\n00328970: 30 00 30 00 30 00 30 00 30 00 30 00 30 00 30 00  0.0.0.0.0.0.0.0.\n00328980: 30 00 30 00 30 00 30 00 30 00 30 00 30 00 30 00  0.0.0.0.0.0.0.0."
>>> a.read(100).decode("utf-16-le")
'hello this is a message I typed in notepad.exe !\x00\x00'
>>> a.write("pwned".encode("utf-16-le"))
1
>>> a.read(100).decode("utf-16-le")
'pwned this is a message I typed in notepad.exe !\x00\x00'
```

Look back at your notepad and the text should be changed! :)
A quicker way to do this could be:

```python
>>> mw.umem_replace("hello","pwned")
```

Some other interesting features like searching for different values types in memory and monitor their changes are also implemented through the Locator class. For example if you are looking to cheat in a game and you start with 200 ammo, you could do something like:

```python
>>> lo = Locator(mw)
>>> lo.feed(200)
...
<Addr: 0x0018FDE2>,
<Addr: 0x0018FDE4>,
<Addr: 0x0018FDE6>,
...]}
```

Use some ammo and "refeed" the locator (do this a couple of times until there is one result left)

```python
>>> lo.feed(199)
{'double': [], 'float': [], 'int': [<Addr: 0x0019FAF0>], 'long': [], 'short': [], 'uint': [], 'ulong': [], 'ushort': []}
>>> a = _["int"][0]
>>> a.read()
199
>>> a.write(999999)
1
```

Now you have infinite ammo :o)

I hope this code will be useful to someone.

Have fun!
