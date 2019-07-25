# pylint: skip-file
import sys
from typing import TYPE_CHECKING

if sys.platform == "win32":
    from .win_structures import *

    if TYPE_CHECKING:
        from .linux_structures import *
else:
    from .linux_structures import *
