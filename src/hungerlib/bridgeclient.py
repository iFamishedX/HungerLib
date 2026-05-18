import requests
import json

class BridgeClient:
    '''HungerBridge client. Usually used internally, but can be used externally.'''
    def __init__(self, url: str, token: str):
        self.base = url.rstrip("/")
        self.headers = {
            "X-Auth-Key": token,
            "Content-Type": "application/json"
        }

    # internal functions
    def _post(self, path, payload):
        r = requests.post(f"{self.base}{path}", headers=self.headers, json=payload)
        if not r.ok:
            raise RuntimeError(f"HungerBridge error {r.status_code}: {r.text}")
        try:
            return r.json()
        except:
            return r.text

    def _get(self, path):
        r = requests.get(f"{self.base}{path}", headers=self.headers)
        if not r.ok:
            raise RuntimeError(f"HungerBridge error {r.status_code}: {r.text}")
        try:
            return r.json()
        except:
            return r.text


    # public api
    def runCommand(
        self,
        command: str,
        show_console: bool = False,
        silent: bool = False,
        normalize: bool = True
    ):
        '''
        Runs a command on the server running HungerBridge. Paramaters:
        - command: the command to run on the server
        - show_console: if the command should be shown on the Minecraft server
        - silent: if the command should not return output
        - normalize: if the json should be returned as a string
        '''
        data = self._post("/v1/run", {
            "command": command,
            "silent": silent,
            "show_console": show_console
        })
        if not normalize:
            return data
        if isinstance(data, list):
            return "\n".join(str(x) for x in data)
        if isinstance(data, dict):
            out = data.get("output")
            if isinstance(out, list):
                return "\n".join(str(x) for x in out)
            if isinstance(out, (str, bytes)):
                return out
            return None
        if isinstance(data, (str, bytes)):
            return data
        return None

    def log(self, message: str, level: str = "info") -> dict:
        '''
        Log something on the server. Levels:
        - info
        - warn
        - error
        - None
        '''
        return self._post("/v1/log", {
            "level": level,
            "message": message
        })

    def getStatus(self) -> dict:
        '''Returns the status of the server'''
        return self._get("/v1/status")

    def getVersion(self) -> dict:
        '''Returns the version of the bridge and server'''
        return self._get("/v1/version")
