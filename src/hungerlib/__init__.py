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

# Lazy imports to avoid import-time failures during packaging
def __getattr__(name):
    if name == "utils":
        from . import utils
        return utils
    if name == "scheduler":
        from . import scheduler
        return scheduler
    if name == "logger":
        from . import logger
        return logger
    if name == "config":
        from . import config
        return config
    if name == "colormap":
        from . import colormap
        return colormap
    if name == "mchelpers":
        from . import mchelpers
        return mchelpers
    if name == "Panel":
        from .panel import Panel
        return Panel
    if name == "GenericServer":
        from .servers._generic import GenericServer
        return GenericServer
    if name == "MinecraftServer":
        from .servers.minecraft import MinecraftServer
        return MinecraftServer
    if name == "checkLag":
        from .utils import checkLag
        return checkLag

    raise AttributeError(f"module 'hungerlib' has no attribute '{name}'")
