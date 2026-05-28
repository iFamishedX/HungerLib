import time
import re

from hungerlib.panel import Panel
from hungerlib.servers import GenericServer
from hungerlib.bridgeclient import BridgeClient
from hungerlib.utils.exceptions import InvalidModeError


class MinecraftServer(GenericServer):
    '''Minecraft Pterodactyl Server'''
    def __init__(
        self,
        name: str,
        panel: Panel,
        server_id: str,
        server_domain: str,
        server_port: int,
        bridge_port: int,
        bridge_token: str,
    ):
        super().__init__(
            name,
            panel,
            server_id,
        )

        # Minecraft-specific fields
        self.server_domain = server_domain
        self.server_port = server_port

        # HungerBridge client
        bridge_url = f'http://{server_domain}:{bridge_port}'
        self.bridge = BridgeClient(bridge_url, bridge_token)


    def getPlayers(self, mode: str = 'count') -> int | list | None:
        '''Returns current online players'''
        if mode == 'count':
            return self.bridge.getPlayers('count')
        elif mode == 'list':
            return self.bridge.getPlayers('list')
        else:
            raise InvalidModeError(f"Invalid mode: '{mode}'")

    def getTPS(self, mode: str = 'current', rounding: int = 3) -> float | None:
        '''
        HungerBridge-native TPS getter
        '''
        try:
            value = self.bridge.getTPS(mode)
        except InvalidModeError:
            return None
        if value is None:
            return None
        return round(value, rounding) if rounding is not None else value

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
