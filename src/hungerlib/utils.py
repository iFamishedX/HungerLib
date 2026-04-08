import time


# utils.py
# Generic helper functions that operate on server objects.
# No server-specific or Minecraft-specific logic belongs here.


# ============================================================
# LAG CHECKER
# ============================================================

def checkLag(server, ram, cpu, nwi, nwo, tps, logger=None):
    """
    Check if the server is under load based on thresholds.
    Returns True if lag is detected.
    """
    reasons = []

    currentRAM = server.getRAM(gb=True)
    currentCPU = server.getCPU()
    currentNWI = server.getNetworkIn(gb=True)
    currentNWO = server.getNetworkOut(gb=True)
    currentTPS = server.getTPS() if hasattr(server, "getTPS") else None

    if currentRAM is not None and currentRAM >= ram:
        reasons.append(f"RAM: {currentRAM}GB")
    if currentCPU is not None and currentCPU >= cpu:
        reasons.append(f"CPU: {currentCPU}%")
    if currentNWI is not None and currentNWI >= nwi:
        reasons.append(f"Network Inbound: {currentNWI}GB")
    if currentNWO is not None and currentNWO >= nwo:
        reasons.append(f"Network Outbound: {currentNWO}GB")
    if currentTPS is not None and currentTPS <= tps:
        reasons.append(f"TPS: {currentTPS}")

    if reasons:
        if logger:
            logger.warn(f"Lag detected: {', '.join(reasons)}")
        return True

    if logger:
        logger.info("No lag detected.")
    return False


# ============================================================
# VALIDATION
# ============================================================

def validateAll(panel, server):
    """
    Validate panel connectivity, API access, and server running state.
    """
    return (
        panel.ping() is True and
        panel.validateAPI() is True and
        server.getStatus() == "running"
    )


# ============================================================
# TIME HELPERS
# ============================================================

def minify(seconds):
    """Convert seconds to minutes."""
    return seconds // 60


# ============================================================
# SERVER STATE HELPERS
# ============================================================

def waitForOnline(server, timeout=60, interval=2):
    """
    Wait until the server reports status 'running'.
    Returns True if online before timeout.
    """
    elapsed = 0
    while elapsed < timeout:
        if server.isOnline():
            return True
        time.sleep(interval)
        elapsed += interval
    return False


def waitForOffline(server, timeout=60, interval=2):
    """
    Wait until the server reports status 'offline'.
    Returns True if offline before timeout.
    """
    elapsed = 0
    while elapsed < timeout:
        if server.isOffline():
            return True
        time.sleep(interval)
        elapsed += interval
    return False
