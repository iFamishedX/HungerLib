import requests

from hungerlib.api.command import CommandAPI
from hungerlib.api.schedule import ScheduleAPI
from hungerlib.api.filemanager import FileManagerAPI
from hungerlib.api.backups import BackupsAPI
from hungerlib.api.databases import DatabasesAPI
from hungerlib.api.startup import StartupAPI
from hungerlib.config import DefaultConfig


class Panel:
    """High-level panel object"""
    def __init__(self, name=None, url=None, api_key=None, Config=DefaultConfig):
        self.Config = Config

        # If Config is provided, use its defaults
        self.name = name or Config.panel_name
        self.url = (url or Config.panel_url).rstrip("/")
        self.api_key = api_key or Config.panel_api_key 

        # API modules
        self.schedules = ScheduleAPI(self)
        self.files = FileManagerAPI(self)
        self.backups = BackupsAPI(self)
        self.databases = DatabasesAPI(self)
        self.startup = StartupAPI(self)
        self.commands = CommandAPI(self)


    def __str__(self):
        return f"Panel name: {self.name}\nURL: {self.url}\nAPI key: {self.api_key}"

    # http core
    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    def get(self, path, timeout=5):
        return requests.get(f"{self.url}{path}", headers=self.headers, timeout=timeout)
    def post(self, path, json=None, timeout=5):
        return requests.post(f"{self.url}{path}", headers=self.headers, json=json, timeout=timeout)
    def delete(self, path, timeout=5):
        return requests.delete(f"{self.url}{path}", headers=self.headers, timeout=timeout)
    def patch(self, path, json=None, timeout=5):
        return requests.patch(f"{self.url}{path}", headers=self.headers, json=json, timeout=timeout)

    # Special-case raw upload (multipart)
    def _raw_upload(self, url, file_data):
        return requests.post(
            f"{self.url}{url}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            files=file_data
        )


    # panel health
    def ping(self):
        try:
            r = self.get("/api/client")
            return r.status_code == 200
        except:
            return False
    def validateAPI(self):
        r = self.get("/api/client/account")
        return r.status_code == 200
