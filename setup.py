# type: ignore
from setuptools import setup, find_packages
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, "README.md")) as file:
        long_description = file.read()
else:
    with open(os.path.join(_here, "README.md"), encoding="utf-8") as file:
        long_description = file.read()

version = {}
with open(os.path.join(_here, "memorpy", "version.py")) as file:
    exec(file.read(), version)

setup(
    name="mempy3",
    version=version["__version__"],
    description=("A python 3 port of memorpy, a library by n1nj4sec"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="starwort",
    url="https://github.com/starwort/memorpy3",
    license="MPL-2.0",
    packages=find_packages(),
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3.6"],
)
