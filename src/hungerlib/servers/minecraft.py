import time
import re

from hungerlib.panel import Panel
from hungerlib.utils.colormaps import MC_COLOR_MAP, ASCII_COLOR_MAP
from hungerlib.servers import GenericServer
from hungerlib.bridgeclient import BridgeClient
from hungerlib.datamap import mapit


class MinecraftServer(GenericServer):
    '''Minecraft Pterodacty Server'''
    def __init__(
        self,
        name: str,
        panel: Panel,
        server_id: str,
        server_domain: str,
        server_port: int,
        bridge_port: int,
        bridge_token: str,
        tpsCommand: str = 'tt20 tps',
    ):
        super().__init__(
            name,
            panel,
            server_id,
        )

        # Minecraft-specific fields
        self.server_domain = server_domain
        self.server_port = server_port
        self.tpsCommand = tpsCommand

        # HungerBridge client
        bridge_url = f"http://{server_domain}:{bridge_port}"
        self.bridge = BridgeClient(bridge_url, bridge_token)


    # getter methods
    def getPlayers(self) -> int | None:
        '''Returns current online players'''
        output = self.bridge.runCommand("list")
        if not output:
            return None
        m = re.search(r"There are (\d+)", output)
        return int(m.group(1)) if m else None

    def getTPS(self, type: str = "raw", rounding: int = 10) -> float| None:
        """
        This has limitations and is not yet complete. It currently ONLY parses TT20's tps command.
        Example: /tt20 tps
        This parser WILL NOT WORK with other configurations!
        In the future, this will likely be replaced by a native HungerBridge tps command.
        """
        output = self.sendConsoleCommand(self.tpsCommand)
        if not output:
            return None
        clean = re.sub(r"§.", "", output)
        m = re.search(
            r"TPS\s+([0-9]+\.[0-9]+)\s+with average\s+([0-9]+\.[0-9]+)\s+accurate\s+([0-9]+\.[0-9]+)",
            clean
        )
        if not m:
            return None
        raw, avg, acc = map(float, m.groups())
        table = {"raw": raw, "avg": avg, "acc": acc}
        value = table.get(type, avg)
        return round(value, rounding) if rounding else value

    # commands
    def sendConsoleCommand(
        self,
        command: str,
        show_console: bool = False,
        silent: bool = False,
        normalize: bool = True
    ):
        '''Runs a Minecraft command with optional output capture'''
        return self.bridge.runCommand(
        command,
        show_console=show_console,
        silent=silent,
        normalize=normalize
    )

    def sendBroadcast(self, message: str):
        '''Sends a broadcast using tellraw'''
        safe = message.replace('"', '\\"')
        cmd = f'tellraw @a {{"text":"{safe}"}}'
        return self.bridge.runCommand(cmd, show_console=True)
