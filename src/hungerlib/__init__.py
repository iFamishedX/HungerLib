from importlib.metadata import version as _pkg_version, PackageNotFoundError

# Package version
try:
    __version__ = _pkg_version("hungerlib")
except PackageNotFoundError:
    __version__ = "0.0.0"


from . import panel
from . import servers
from . import messagerouter
from . import datamap
from . import configloader
from . import utils

__all__ = [
    "panel",
    "servers",
    "messagerouter",
    "datamap",
    "configloader",
    "utils",
]