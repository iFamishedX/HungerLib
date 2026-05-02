from .colormaps import ColorMap, ASCII_COLOR_MAP, MC_COLOR_MAP
from .time import (
    snapSchedule,
    runCountdownEvents,
    waitForOnline,
    waitForOffline,
    secsUntil,
    minsUntil
)
from .utils import Snapshot, clearTerminal, validateAll

__all__ = [
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
    'load'
]

# === Loader for selective unpacking ===
import inspect

def load():
    caller = inspect.currentframe().f_back.f_globals
    caller.update({
        "ColorMap": ColorMap,
        "ASCII_COLOR_MAP": ASCII_COLOR_MAP,
        "MC_COLOR_MAP": MC_COLOR_MAP,
        "snapSchedule": snapSchedule,
        "runCountdownEvents": runCountdownEvents,
        "waitForOnline": waitForOnline,
        "waitForOffline": waitForOffline,
        "secsUntil": secsUntil,
        "minsUntil": minsUntil,
        "Snapshot": Snapshot,
        "clearTerminal": clearTerminal,
        "validateAll": validateAll,
    })
