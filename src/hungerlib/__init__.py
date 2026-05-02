from importlib.metadata import version as _pkg_version, PackageNotFoundError

# package version
try:
    __version__ = _pkg_version('hungerlib')
except PackageNotFoundError:
    __version__ = '0.0.0'

# modules
from .configloader import loadConfig
from .datamap import set_default_maps, get_default_maps, Syntax, DataMap, datamap, mapit
from .messagerouter import MessageRouter
from .servers import GenericServer, MinecraftServer
from .utils import (
    ColorMap,
    ASCII_COLOR_MAP,
    MC_COLOR_MAP,
    snapSchedule,
    runCountdownEvents,
    waitForOnline,
    waitForOffline,
    secsUntil,
    minsUntil,
    Snapshot,
    clearTerminal,
    validateAll,
)

__all__ = [
    '__version__',

    'loadConfig',
    'MessageRouter',
    'Panel',

    'set_default_maps',
    'get_default_maps',
    'Syntax',
    'DataMap',
    'datamap',
    'mapit',

    'GenericServer',
    'MinecraftServer',

    'ColorMap',
    'ASCII_COLOR_MAP',
    'MC_COLOR_MAP',
    'snapSchedule',
    'runCountdownEvents',
    'waitForOnline',
    'waitForOffline',
    'secsUntil',
    'minsUntil',
    'Snapshot',
    'clearTerminal',
    'validateAll',
]