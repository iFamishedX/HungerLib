from importlib.metadata import version as _pkg_version, PackageNotFoundError

try:
    __version__ = _pkg_version("hungerlib")
except PackageNotFoundError:
    __version__ = "0.0.0"

# Import modules normally
from . import panel
from . import servers
from . import messagerouter
from . import datamap as _datamap
from . import configloader
from . import utils

from .datamap import *

__all__ = [
    # modules
    "panel",
    "servers",
    "messagerouter",
    "datamap",
    "configloader",
    "utils",

    * _datamap.__all__,
]