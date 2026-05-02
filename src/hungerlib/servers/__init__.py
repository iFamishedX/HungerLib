from .generic import GenericServer
from .minecraft import MinecraftServer

__all__ = [
    "GenericServer",
    "MinecraftServer",
    "load",
]

import inspect

def load():
    caller = inspect.currentframe().f_back.f_globals
    caller.update({
        "GenericServer": GenericServer,
        "MinecraftServer": MinecraftServer,
    })
