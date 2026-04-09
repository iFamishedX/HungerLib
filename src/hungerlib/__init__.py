# HungerLib public API with safe lazy imports and runtime version metadata

from importlib.metadata import version as _pkg_version, PackageNotFoundError
import importlib

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
    "HungerLogger",
    "__version__",
]


def _load(module_name, attr=None):
    """
    Safe lazy loader:
    - loads module via importlib (no __getattr__ recursion)
    - returns module OR attribute
    - caches result in globals() so subsequent access is direct
    """
    module = importlib.import_module(f"hungerlib.{module_name}")

    if attr is not None:
        value = getattr(module, attr)
        globals()[attr] = value
        return value

    # cache module under its short name (e.g., "utils", "config")
    short_name = module_name.rsplit(".", 1)[-1]
    globals()[short_name] = module
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
    if name == "HungerLogger":
        return _load("logger", "HungerLogger")


    raise AttributeError(f"module 'hungerlib' has no attribute '{name}'")
