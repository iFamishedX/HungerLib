import inspect

def load():
    caller = inspect.currentframe().f_back.f_globals

    # All modules that support .load()
    from . import (
        datamap,
        servers,
        configloader,
        panel,
        messagerouter,
        utils
    )

    modules = {
        "datamap": datamap,
        "servers": servers,
        "configloader": configloader,
        "panel": panel,
        "messagerouter": messagerouter,
        "utils": utils,
    }

    # For each module the user imported, call its loader
    for name, module in modules.items():
        if name in caller:
            loader = getattr(module, "load", None)
            if callable(loader):
                loader()
