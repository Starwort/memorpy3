import logging

logger = logging.getLogger("memorpy")
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
logger.addHandler(ch)

import sys
from .mem_worker import *
from .locator import *
from .address import *
from .process import *
from .utils import *
