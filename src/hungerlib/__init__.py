from importlib.metadata import version as _pkg_version, PackageNotFoundError

try:
    __version__ = _pkg_version('hungerlib')
except PackageNotFoundError:
    __version__ = '0.0.0'

# === MODULES ===
from . import panel
from . import servers
from . import messagerouter
from . import datamap
from . import configloader
from . import utils

# === SYMBOLS ===
from .panel import Panel

from .configloader import loadConfig
from .messagerouter import MessageRouter
from .servers import GenericServer, MinecraftServer
from .datamap import Syntax, DataMap, datamap, mapit, set_default_maps, get_default_maps
from .utils import (
    ASCII_COLOR_MAP,
    MC_COLOR_MAP,
    ColorMap,
    snapSchedule,
    runCountdownEvents,
    waitForOnline,
    waitForOffline,
    secsUntil,
    minsUntil,
    Snapshot,
    clearTerminal,
    validateAll
)

__all__ = [
    # === MODULES ===
    'panel',
    'servers',
    'messagerouter',
    'datamap',
    'configloader',
    'utils',

    # === SYMBOLS ===
    'Panel',
    'loadConfig',
    'MessageRouter',
    
    'GenericServer',
    'MinecraftServer',

    'Syntax',
    'DataMap',
    'datamap',
    'mapit',
    'set_default_maps',
    'get_default_maps',

    'ASCII_COLOR_MAP',
    'MC_COLOR_MAP',
    'ColorMap',
    'snapSchedule',
    'runCountdownEvents',
    'waitForOnline',
    'waitForOffline',
    'secsUntil',
    'minsUntil',
    'Snapshot',
    'clearTerminal',
    'validateAll'
]