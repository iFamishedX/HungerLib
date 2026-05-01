from importlib.metadata import version as _pkg_version, PackageNotFoundError

try:
    __version__ = _pkg_version("hungerlib")
except PackageNotFoundError:
    __version__ = "0.0.0"

# Import modules
from . import panel
from . import servers
from . import messagerouter
from . import datamap as _datamap
from . import configloader
from . import utils

# Re-export datamap symbols
from .datamap import (
    Syntax,
    DataMap,
    datamap,
    mapit,
    set_default_maps,
    get_default_maps,
)

# Re-export servers symbols
from .servers import (
    MinecraftServer,
    GenericServer,
)

# Re-export panel symbols
from .panel import Panel

# Re-export utils symbols
from .utils import (
    ASCII_COLOR_MAP,
    MC_COLOR_MAP,
    ColorMap,
)

# Re-export configloader symbols
from .configloader import loadConfig

__all__ = [
    # modules
    "panel",
    "servers",
    "messagerouter",
    "datamap",
    "configloader",
    "utils",

    # datamap symbols
    "Syntax",
    "DataMap",
    "datamap",
    "mapit",
    "set_default_maps",
    "get_default_maps",

    # servers symbols
    "MinecraftServer",
    "GenericServer",

    # panel symbols
    "Panel",

    # utils symbols
    "ASCII_COLOR_MAP",
    "MC_COLOR_MAP",
    "ColorMap",

    # configloader symbols
    "loadConfig",
]
