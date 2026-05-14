import time
import re
import mcrcon

from hungerlib.panel import Panel
from hungerlib.utils.colormaps import MC_COLOR_MAP, ASCII_COLOR_MAP
from hungerlib.servers import GenericServer
from hungerlib.bridge import HungerBridgeClient


class MinecraftServer(GenericServer):
    def __init__(
        self,
        name,
        panel: Panel,
        server_id,
        server_domain,
        server_port,
        rcon_port,
        rcon_password,
        bridge_url=None,
        bridge_token=None,
        mc_color_map=MC_COLOR_MAP,
        ascii_color_map=ASCII_COLOR_MAP,
        tpsCommand='tt20 tps',
    ):
        mc_map = (
            mc_color_map.as_dict()
            if hasattr(mc_color_map, "as_dict")
            else mc_color_map
        )
        ascii_map = (
            ascii_color_map.as_dict()
            if hasattr(ascii_color_map, "as_dict")
            else ascii_color_map
        )

        super().__init__(
            name,
            panel,
            server_id,
            mc_color_map=mc_map,
            ascii_color_map=ascii_map
        )

        # Minecraft-specific fields
        self.server_domain = server_domain
        self.server_port = server_port
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.tpsCommand = tpsCommand

        # Optional HungerBridge client
        self.bridge: HungerBridgeClient | None = None
        if bridge_url and bridge_token:
            self.bridge = HungerBridgeClient(bridge_url, bridge_token)

    # rcon handler (fallback path)
    def _rcon_send(self, command):
        if not self.server_domain or not self.rcon_password:
            return None
        try:
            with mcrcon.MCRcon(self.server_domain, self.rcon_password, port=self.rcon_port) as m:
                resp1 = m.command(command)
                time.sleep(0.05)
                resp2 = m.command("")  # fetch buffered packets
                return (resp1 or "") + (resp2 or "")
        except Exception as e:
            print("RCON error:", e)
            return None

    # getter methods
    def getPlayers(self):
        # Prefer bridge if we ever add an endpoint; for now still RCON
        output = self._rcon_send("list")
        if not output:
            return None
        m = re.search(r"There are (\d+)", output)
        return int(m.group(1)) if m else None

    def getTPS(self, type="raw", rounding=10):
        """
        This has limitations and is not yet complete. It currently ONLY parses TT20's tps command.
        Example: /tt20 tps
        This parser WILL NOT WORK with other configurations!
        """
        output = self._rcon_send(self.tpsCommand)
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
    def sendConsoleCommand(self, command: str):
        # Prefer HungerBridge
        if self.bridge is not None:
            try:
                return self.bridge.runCommand(command)
            except Exception as e:
                print("Bridge command error, falling back to panel:", e)

        # Fallback to panel (which may use RCON or other transport)
        return self.panel.commands.send(self.server_id, command)

    def sendBroadcast(self, message: str):
        translated = self._translate_mc_colors(message)
        safe = translated.replace('"', '\\"')
        cmd = f'tellraw @a {{"text":"{safe}"}}'

        # Prefer HungerBridge
        if self.bridge is not None:
            try:
                return self.bridge.runCommand(cmd)
            except Exception as e:
                print("Bridge broadcast error, falling back to panel:", e)

        # Fallback
        return self.sendConsoleCommand(cmd)
