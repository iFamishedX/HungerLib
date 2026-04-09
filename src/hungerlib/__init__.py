# HungerLib public API with safe lazy imports

from importlib.metadata import version as _pkg_version, PackageNotFoundError

try:
    __version__ = _pkg_version("hungerlib")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "utils",
    "scheduler",
    "logger",
    "config",
    "colormap",
    "mchelpers",
    "Panel",
    "GenericServer",
    "MinecraftServer",
    "checkLag",
    "DefaultConfig",
    "HungerSMP",
    "__version__",
]

import importlib


def _load(module_name, attr=None):
    module = importlib.import_module(f"hungerlib.{module_name}")
    if attr:
        value = getattr(module, attr)
        globals()[attr] = value
        return value
    globals()[module_name] = module
    return module


def __getattr__(name):
    if name == "utils":
        return _load("utils")
    if name == "scheduler":
        return _load("scheduler")
    if name == "logger":
        return _load("logger")
    if name == "config":
        return _load("config")
    if name == "colormap":
        return _load("colormap")
    if name == "mchelpers":
        return _load("mchelpers")
    if name == "Panel":
        return _load("panel", "Panel")
    if name == "GenericServer":
        return _load("servers._generic", "GenericServer")
    if name == "MinecraftServer":
        return _load("servers.minecraft", "MinecraftServer")
    if name == "checkLag":
        return _load("utils", "checkLag")
    if name == "DefaultConfig":
        return _load("config", "DefaultConfig")
    if name == "HungerSMP":
        return _load("config", "HungerSMP")

    raise AttributeError(f"module 'hungerlib' has no attribute '{name}'")
