from importlib.metadata import version as _pkg_version, PackageNotFoundError
from types import SimpleNamespace

# package version
try:
    __version__ = _pkg_version('hungerlib')
except PackageNotFoundError:
    __version__ = '0.0.0'

# modules
from .configloader import loadConfig
from .datamap import setGlobalMaps, getGlobalMaps, Syntax, DataMap, datamap, mapit
from .messagerouter import MessageRouter
from .panel import Panel
from .servers import GenericServer, MinecraftServer
from .bridgeclient import BridgeClient
from .utils import (
    ColorMap,
    ASCII_COLOR_MAP,
    MC_COLOR_MAP,
    STRIP_COLOR_MAP,
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

# namespaces
utils = SimpleNamespace(
    ColorMap = ColorMap,
    ASCII_COLOR_MAP = ASCII_COLOR_MAP,
    MC_COLOR_MAP = MC_COLOR_MAP,
    STRIP_COLOR_MAP = STRIP_COLOR_MAP,
    snapSchedule = snapSchedule,
    runCountdownEvents = runCountdownEvents,
    waitForOnline = waitForOnline,
    waitForOffline = waitForOffline,
    secsUntil = secsUntil,
    minsUntil = minsUntil,
    Snapshot = Snapshot,
    clearTerminal = clearTerminal,
    validateAll = validateAll,
)

servers = SimpleNamespace(
    Panel = Panel,
    Generic = GenericServer,
    Minecraft = MinecraftServer,
)

datamap_api = SimpleNamespace(
    setGlobalMaps = setGlobalMaps,
    getGlobalMaps = getGlobalMaps,
    Syntax = Syntax,
    DataMap = DataMap,
    decorator = datamap,
    mapit = mapit,

    braces = Syntax.braces,
    dollars = Syntax.dollars,
    angles = Syntax.angles,
    percents = Syntax.percents,
)



__all__ = [
    '__version__',

    # modules
    'loadConfig',
    'MessageRouter',
    'Panel',
    'setGlobalMaps',
    'getGlobalMaps',
    'Syntax',
    'DataMap',
    'datamap',
    'mapit',
    'GenericServer',
    'MinecraftServer',
    'ColorMap',
    'ASCII_COLOR_MAP',
    'MC_COLOR_MAP',
    'STRIP_COLOR_MAP',
    'snapSchedule',
    'runCountdownEvents',
    'waitForOnline',
    'waitForOffline',
    'secsUntil',
    'minsUntil',
    'Snapshot',
    'clearTerminal',
    'validateAll',
    'BridgeClient',

    # namespaces
    'utils',
    'servers',
    'datamap_api',
]