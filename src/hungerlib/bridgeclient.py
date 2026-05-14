import requests

class HungerBridgeClient:
    def __init__(self, base_url: str, token: str):
        self.base = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def _post(self, path: str, payload: dict):
        r = requests.post(f"{self.base}{path}", headers=self.headers, json=payload)
        if not r.ok:
            raise RuntimeError(f"HungerBridge error {r.status_code}: {r.text}")
        return r.json()

    def _get(self, path: str):
        r = requests.get(f"{self.base}{path}", headers=self.headers)
        if not r.ok:
            raise RuntimeError(f"HungerBridge error {r.status_code}: {r.text}")
        return r.json()

    # -----------------------------
    # Public API
    # -----------------------------
    def health(self):
        return self._get("/health")

    def ping(self):
        return self._get("/ping")

    def runCommand(self, command: str, silent: bool = False):
        return self._post("/run", {
            "command": command,
            "silent": silent
        })

    def log(self, message: str, level: str = "info"):
        return self._post("/log", {
            "level": level,
            "message": message
        })
