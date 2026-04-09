from importlib.metadata import version as _pkg_version, PackageNotFoundError
import importlib

try:
    __version__ = _pkg_version("hungerlib")
except PackageNotFoundError:
    __version__ = "0.0.0"


# Public API map
# name -> (module_path, attribute_name or None)
_EXPORTS = {
    # core modules
    "panel": ("panel", None),
    "config": ("config", None),
    "logger": ("logger", None),
    "scheduler": ('scheduler', None),

    # core module utilities
    "Panel": ('panel', 'Panel'),
    'DefaultConfig': ('config', 'DefaultConfig'),
    'HungerLogger': ('logger', 'HungerLogger'),
    "snapSchedule": ("scheduler", "snapSchedule"),
    "secsUntil": ("scheduler", "secsUntil"),
    "minsUntil": ("scheduler", "minsUntil"),

    # servers
    "GenericServer": ("servers._generic", "GenericServer"),
    "MinecraftServer": ("servers.minecraft", "MinecraftServer"),

    # addons 
    "genericAddons": ("addons._generic", None),
    "minecraftAddons": ("addons.minecraft", None),
    "colormap": ("addons.colormap", None),

    # addon utilities
    "runCountdownEvents": ("addons._generic", "runCountdownEvents"),
    "validateAll": ("addons._generic", "validateAll"),
    "waitForOnline": ("addons._generic", "waitForOnline"),
    "waitForOffline": ("addons._generic", "waitForOffline"),
    "checkLag": ("addons.minecraft", "checkLag"),
    "MC_COLOR_MAP": ("addons.colormap", "MC_COLOR_MAP"),
    "ASCI_COLOR_MAP": ("addons.colormap", "ASCI_COLOR_MAP"),

    # api endpoints
    "ScheduleAPI": ("api.schedule", "ScheduleAPI"),
    "FileManagerAPI": ("api.filemanager", "FileManagerAPI"),
    "BackupsAPI": ("api.backups", "BackupsAPI"),
    "DatabasesAPI": ("api.databases", "DatabasesAPI"),
    "StartupAPI": ("api.startup", "StartupAPI")

}


__all__ = list(_EXPORTS.keys()) + ["__version__"]


# Lazy loader
def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(f"module 'hungerlib' has no attribute '{name}'")

    module_name, attr = _EXPORTS[name]
    module = importlib.import_module(f"hungerlib.{module_name}")

    # Export module itself
    if attr is None:
        globals()[name] = module
        return module

    # Export attribute from module
    value = getattr(module, attr)
    globals()[name] = value
    return value
