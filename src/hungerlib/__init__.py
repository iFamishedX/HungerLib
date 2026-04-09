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
]

import importlib


def _load(module_name, attr=None):
    """
    Safe lazy loader:
    - loads module with importlib (no recursion)
    - returns module OR attribute
    - caches result in globals()
    """
    module = importlib.import_module(f"hungerlib.{module_name}")

    if attr:
        value = getattr(module, attr)
        globals()[attr] = value
        return value

    globals()[module_name] = module
    return module


def __getattr__(name):
    # module-level exports
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

    # class/function exports
    if name == "Panel":
        return _load("panel", "Panel")

    if name == "GenericServer":
        return _load("servers._generic", "GenericServer")

    if name == "MinecraftServer":
        return _load("servers.minecraft", "MinecraftServer")

    if name == "checkLag":
        return _load("utils", "checkLag")

    # config attributes
    if name == "DefaultConfig":
        return _load("config", "DefaultConfig")

    if name == "HungerSMP":
        return _load("config", "HungerSMP")

    raise AttributeError(f"module 'hungerlib' has no attribute '{name}'")
