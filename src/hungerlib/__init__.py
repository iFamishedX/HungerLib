from importlib.metadata import version as _pkg_version, PackageNotFoundError
import importlib

try:
    __version__ = _pkg_version("hungerlib")
except PackageNotFoundError:
    __version__ = "0.0.0"


# api map
# name > (module_path, attribute_name or None)
_EXPORTS = {
    # modules
    "config": ("config", None),
    "logger": ("logger", None),
    "mchelpers": ("mchelpers", None),
    "panel": ("panel", None),
    "scheduler": ("scheduler", None),

    # addon modules
    "genericAddons": ('addons._generic', None),
    'minecraftAddons': ('addons.minecraft', None),
    "colormap": ("addons.colormap", None),

    # classes / functions
    "Panel": ("panel", "Panel"),
    "GenericServer": ("servers._generic", "GenericServer"),
    "MinecraftServer": ("servers.minecraft", "MinecraftServer"),
    "DefaultConfig": ("config", "DefaultConfig"),
    "HungerLogger": ("logger", "HungerLogger"),
    "MCHelpers": ("mchelpers", "MCHelpers"),

    # schedulers
    "snapSchedule": ("scheduler", "snapSchedule"),
    "secsUntil": ("scheduler", "secsUntil"),
    "minsUntil": ("scheduler", "minsUntil"),

    # addons
    "runCountdownEvents": ('addons._generic', 'runCountdownEvents'),
    'validateAll': ('addons._generic', 'validateAll'),
    "waitForOnline": ("addons._generic", 'waitForOnline'),
    "waitForOffline": ("addons._generic", 'waitForOffline'),
    'checkLag': ('addons.minecraft', 'checkLag'),
    "MC_COLOR_MAP": ("addons.colormap", "MC_COLOR_MAP"),
    "ASCI_COLOR_MAP": ("addons.colormap", "ASCI_COLOR_MAP")

}


__all__ = list(_EXPORTS.keys()) + ["__version__"]


# lazy loader
def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(f"module 'hungerlib' has no attribute '{name}'")

    module_name, attr = _EXPORTS[name]
    module = importlib.import_module(f"hungerlib.{module_name}")

    # If exporting the module itself
    if attr is None:
        globals()[name] = module
        return module

    # If exporting a specific attribute
    value = getattr(module, attr)
    globals()[name] = value
    return value
