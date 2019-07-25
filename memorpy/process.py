import sys
from .base_process import *  # pylint: disable=unused-wildcard-import

if sys.platform == "win32":
    from .win_process import WinProcess as Process
elif sys.platform == "darwin":
    from .osx_process import OSXProcess as Process
elif "sunos" in sys.platform:
    from .sun_process import SunProcess as Process
else:
    from .linux_process import LinProcess as Process
