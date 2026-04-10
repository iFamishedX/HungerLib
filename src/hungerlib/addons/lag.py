def checkLag(server, ram, cpu, nwi, nwo, tps):
    """
    Pure lag check.
    Returns a tuple: (lag_detected: bool, reasons: list[str])
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

    return (len(reasons) > 0, reasons)