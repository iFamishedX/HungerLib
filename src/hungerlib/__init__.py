# HungerLib public API with safe lazy imports

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
]

import importlib


def __getattr__(name):
    if name == "utils":
        return importlib.import_module("hungerlib.utils")

    if name == "scheduler":
        return importlib.import_module("hungerlib.scheduler")

    if name == "logger":
        return importlib.import_module("hungerlib.logger")

    if name == "config":
        return importlib.import_module("hungerlib.config")

    if name == "colormap":
        return importlib.import_module("hungerlib.colormap")

    if name == "mchelpers":
        return importlib.import_module("hungerlib.mchelpers")

    if name == "Panel":
        return importlib.import_module("hungerlib.panel").Panel

    if name == "GenericServer":
        return importlib.import_module("hungerlib.servers._generic").GenericServer

    if name == "MinecraftServer":
        return importlib.import_module("hungerlib.servers.minecraft").MinecraftServer

    if name == "checkLag":
        return importlib.import_module("hungerlib.utils").checkLag

    raise AttributeError(f"module 'hungerlib' has no attribute '{name}'")
