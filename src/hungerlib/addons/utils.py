import os

def mb_gb(mb, floor=False):
    return mb / 1000 if not floor else mb // 1000

def gb_mb(gb):
    return gb * 1000

def mib_gib(mib, floor=False):
    return mib / 1024 if not floor else mib // 1024

def gib_mib(gib):
    return gib * 1024

def clearTerminal():
    os.system("clear" if os.name == "posix" else "cls")

def validateAll(panel, server):
    """
    Validate panel connectivity, API access, and server running state.
    """
    return (
        panel.ping() is True and
        panel.validateAPI() is True and
        server.getStatus() == "running"
    )