import requests
import json

class BridgeClient:
    def __init__(self, url, token):
        self.base = url.rstrip("/")
        self.headers = {
            "X-Auth-Key": token,
            "Content-Type": "application/json"
        }

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

    def runCommand(self, command, show_console=False, silent=False, normalize=True):
        data = self._post("/v1/run", {
            "command": command,
            "silent": silent,
            "show_console": show_console
        })

        if not normalize:
            return data

        if isinstance(data, dict):
            if "error" in data or "success" in data:
                return None
            if "output" in data:
                return data["output"]
            return None

        if isinstance(data, list):
            return "\n".join(str(x) for x in data)

        if isinstance(data, (str, bytes)):
            return data

        return None

    def log(self, message, level="info"):
        return self._post("/v1/log", {
            "level": level,
            "message": message
        })

    def getStatus(self):
        return self._get("/v1/status")

    def getVersion(self):
        return self._get("/v1/version")
