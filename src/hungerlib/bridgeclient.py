import time
import requests
from .utils.exceptions import HungerBridgeError, InvalidLevelError, InvalidModeError


class BridgeClient:
    '''
    Python client for the HungerBridge v2 API
    '''
    def __init__(self, url: str, token: str):
        self.base = url.rstrip('/') + '/v2/'
        self.headers = {
            'X-Auth-Key': token,
            'Content-Type': 'application/json'
        }

    # internal helpers
    def _post(self, path: str, payload):
        r = requests.post(self.base + path, headers=self.headers, json=payload)
        if not r.ok:
            raise HungerBridgeError(f'HungerBridge error {r.status_code}: {r.text}')
        try:
            return r.json()
        except Exception:
            return r.text

    def _get(self, path: str):
        r = requests.get(self.base + path, headers=self.headers)
        if not r.ok:
            raise HungerBridgeError(f'HungerBridge error {r.status_code}: {r.text}')
        try:
            return r.json()
        except Exception:
            return r.text

    def _extract(self, data, field):
        if not isinstance(data, dict):
            raise HungerBridgeError('_extract() expects a dict response')
        return data.get(field)

    # raw endpoints
    def v2_ping(self) -> dict:
        return self._get('ping')

    def v2_info(self) -> dict:
        return self._get('info')

    def v2_status(self) -> dict:
        return self._get('status')

    def v2_tps(self) -> dict:
        return self._get('tps')

    def v2_players(self) -> dict:
        return self._get('players')

    # public api
    def runCommand(
        self,
        command: str,
        show_console: bool = False,
        silent: bool = False,
        normalize: bool = True
    ):
        '''
        Execute a command on the server.
        Returns normalized output unless normalize=False.
        '''
        data = self._post('run', {
            'command': command,
            'silent': silent,
            'show_console': show_console
        })
        if not normalize:
            return data
        if isinstance(data, dict):
            out = data.get('output')
            if isinstance(out, list):
                return '\n'.join(str(x) for x in out)
            if isinstance(out, (str, bytes)):
                return out
            return None
        if isinstance(data, list):
            return '\n'.join(str(x) for x in data)
        if isinstance(data, (str, bytes)):
            return data
        return None

    def log(self, message: str, level: str = 'info') -> dict:
        '''
        Logs a message to the server console
        '''
        valid_levels = ['info', 'warn', 'error', None]
        if level not in valid_levels:
            raise InvalidLevelError(f'\'{level}\' is not a valid log level')
        if level is not None:
            return self._post('log', {
                'level': level,
                'message': message
            })
        no_level_message = ('\b' * 20) + message
        return self._post('log', {
            'level': 'info',
            'message': no_level_message
        })

    # convenience getters
    def getPing(self) -> int:
        '''
        Round-trip latency (ms) measured client-side.
        '''
        start = time.time()
        self.v2_ping()
        end = time.time()
        return int((end - start) * 1000)

    def getVersion(self) -> str | None:
        '''Returns HungerBridge version'''
        info = self.v2_info()
        bridge = self._extract(info, 'bridge')
        return bridge.get('version') if isinstance(bridge, dict) else None

    def getPlatform(self) -> str | None:
        '''Returns server platform'''
        info = self.v2_info()
        bridge = self._extract(info, 'bridge')
        return bridge.get('platform') if isinstance(bridge, dict) else None

    def getMinecraftVersion(self) -> str | None:
        '''Returns Minecraft version'''
        info = self.v2_info()
        bridge = self._extract(info, 'bridge')
        return bridge.get('minecraft') if isinstance(bridge, dict) else None

    def getStatus(self) -> bool:
        '''Validates connection status'''
        return self._extract(self.v2_status(), 'ok')

    def getTPS(self, mode: str = 'current') -> float:
        '''
        Returns TPS values:
        - current:   EMA20
        - 1m:        EMA1200
        - 5m:        EMA6000
        - tick_time: avg tick time (ms)
        '''
        data = self.v2_tps()
        if mode == 'current':
            return self._extract(data, 'tps')
        if mode == '1m':
            return self._extract(data, 'tps_1m')
        if mode == '5m':
            return self._extract(data, 'tps_5m')
        if mode == 'tick_time':
            return self._extract(data, 'tick_time_ms')

        raise InvalidModeError(f'Invalid mode: \'{mode}\'')

    def getPlayers(self, mode: str = 'count') -> int | list:
        '''
        Returns:
        - count: number of players
        - list: list of player names
        '''
        data = self.v2_players()

        if mode == 'count':
            return self._extract(data, 'count')
        if mode == 'list':
            return self._extract(data, 'players')
        raise InvalidModeError(f'Invalid mode: \'{mode}\'')
