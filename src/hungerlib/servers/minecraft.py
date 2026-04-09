# Minecraft server class
import time
import re
import mcrcon
from hungerlib.panel import Panel
from hungerlib.config import Config
from hungerlib.servers._generic import GenericServer


class MinecraftServer(GenericServer):
    def __init__(
        self,
        name,
        panel,
        server_id,
        server_domain,
        server_port,
        Config,
        rcon_port=None,
        rcon_password=None,
        tpsCommand='ticks'
    ):
        '''
        A highly configurable server class for Minecraft servers.
        Supports Rcon.
        '''
        super().__init__(
            name,
            panel,
            server_id,
            server_domain,
            server_port,
            rcon_port,
            rcon_password,
            Config
        )
        self.tpsCommand = tpsCommand

    # ============================================================
    # RCON HANDLER
    # ============================================================

    def _rcon_send(self, command):
        try:
            with mcrcon.MCRcon(self.server_domain, self.rcon_password, port=self.rcon_port) as m:
                resp1 = m.command(command)
                time.sleep(0.05)
                resp2 = m.command("")  # fetch buffered packets
                return (resp1 or "") + (resp2 or "")
        except Exception as e:
            print("RCON error:", e)
            return None

    # ============================================================
    # PLAYERS
    # ============================================================

    def getPlayers(self):
        output = self._rcon_send("list")
        if not output:
            return None
        m = re.search(r"There are (\d+)", output)
        return int(m.group(1)) if m else None

    # ============================================================
    # TPS PARSER
    # ============================================================

    def getTPS(self, type="raw", rounding=10):
        '''
        This has limitations and is not yet complete. It currently ONLY parses TT20's tps command.
        Example: /tt20 tps
        This parser WILL NOT WORK with other configurations!
        '''
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

    # ============================================================
    # COMMANDS
    # ============================================================

    def sendConsoleCommand(self, command):
        return self.panel.commands.send(self.server_id, command)

    def sendBroadcast(self, message):
        translated = self._translate_mc_colors(message)
        safe = translated.replace('"', '\\"')
        cmd = f'tellraw @a {{"text":"{safe}"}}'
        return self.sendConsoleCommand(cmd)
