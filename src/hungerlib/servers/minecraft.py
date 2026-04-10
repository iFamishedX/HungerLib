# Minecraft server class
import time
import re
import mcrcon
from hungerlib.panel import Panel
from hungerlib.servers.generic import GenericServer


class MinecraftServer(GenericServer):
    def __init__(
        self,
        name,
        panel,
        server_id,
        server_domain,
        server_port=25565,
        rcon_port=25575,
        rcon_password,
        tpsCommand='tt20 tps'
    ):
        super().__init__(name, panel, server_id)

        self.server_domain = server_domain
        self.server_port = server_port
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.tpsCommand = tpsCommand



    # rcon handler
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
        output = self._rcon_send("list")
        if not output:
            return None
        m = re.search(r"There are (\d+)", output)
        return int(m.group(1)) if m else None
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


    # commands
    def sendConsoleCommand(self, command):
        return self.panel.commands.send(self.server_id, command)
    def sendBroadcast(self, message):
        translated = self._translate_mc_colors(message)
        safe = translated.replace('"', '\\"')
        cmd = f'tellraw @a {{"text":"{safe}"}}'
        return self.sendConsoleCommand(cmd)
