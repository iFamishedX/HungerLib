# hungerlib/__init__.py

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


from .datamap import (
    set_default_maps,
    get_default_maps,
    Syntax,
    DataMap,
    datamap as datamap_decorator,
    mapit,
)


__all__ = [
    # modules
    "panel",
    "servers",
    "messagerouter",
    "datamap",
    "configloader",
    "utils",

    # datamap symbols
    "set_default_maps",
    "get_default_maps",
    "Syntax",
    "DataMap",
    "datamap_decorator",
    "mapit",
]
