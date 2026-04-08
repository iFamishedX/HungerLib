# Universal server class
import time
import re
import mcrcon
from hungerlib.panel import Panel
from hungerlib.config import Config


class GenericServer:
    def __init__(
        self,
        name,
        panel: Panel,
        server_id,
        server_domain,
        server_port,
        rcon_port,
        rcon_password,
        Config: Config
    ):
        '''A universal server class'''
        self.name = name
        self.panel = panel
        self.server_id = server_id
        self.server_domain = server_domain
        self.server_port = server_port
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.Config = Config
        self._cached_resources = None

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    def _translate_mc_colors(self, msg):
        for tag, code in self.Config.mc_color_map.items():
            msg = msg.replace(tag, code)
        return msg

    # ============================================================
    # RESOURCE & STATUS
    # ============================================================

    def refresh(self):
        r = self.panel.get(f"/api/client/servers/{self.server_id}/resources")
        self._cached_resources = r.json().get("attributes", {}).get("resources", {})
        return self._cached_resources

    def resources(self):
        return self._cached_resources or self.refresh()

    def getRAM(self, rounding=2, gb=False):
        mem = self.resources().get("memory_bytes")
        if mem is None:
            return None
        div = 1024 * 1024 * (1024 if gb else 1)
        return round(mem / div, rounding)

    def getCPU(self, rounding=2):
        cpu = self.resources().get("cpu_absolute")
        return round(cpu, rounding) if cpu is not None else None

    def getDisk(self, rounding=2, gb=False):
        disk = self.resources().get("disk_bytes")
        if disk is None:
            return None
        div = 1024 * 1024 * (1024 if gb else 1)
        return round(disk / div, rounding)

    def getNetworkIn(self, rounding=2, gb=False):
        rx = self.resources().get("network_rx_bytes")
        if rx is None:
            return None
        div = 1024 * 1024 * (1024 if gb else 1)
        return round(rx / div, rounding)

    def getNetworkOut(self, rounding=2, gb=False):
        tx = self.resources().get("network_tx_bytes")
        if tx is None:
            return None
        div = 1024 * 1024 * (1024 if gb else 1)
        return round(tx / div, rounding)

    def getUptime(self, formatted=False):
        uptime = self.resources().get("uptime")
        if uptime is None:
            return None
        seconds = uptime // 1000
        if not formatted:
            return seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    def getStatus(self):
        r = self.panel.get(f"/api/client/servers/{self.server_id}/resources")
        return r.json().get("attributes", {}).get("current_state")

    # ============================================================
    # STATE HELPERS
    # ============================================================

    def isOnline(self):
        return self.getStatus() == "running"

    def isOffline(self):
        return self.getStatus() == "offline"

    # ============================================================
    # POWER ACTIONS
    # ============================================================

    def powerAction(self, action):
        valid = {"start", "restart", "stop", "kill"}
        if action not in valid:
            raise ValueError(f"Invalid power action '{action}'")
        payload = {"signal": action}
        r = self.panel.post(f"/api/client/servers/{self.server_id}/power", json=payload)
        return r.status_code, r.text

    def start(self): return self.powerAction("start")
    def restart(self): return self.powerAction("restart")
    def stop(self): return self.powerAction("stop")
    def kill(self): return self.powerAction("kill")

    # ============================================================
    # FILE MANAGER
    # ============================================================

    def listFiles(self, directory="/"):
        return self.panel.fm_list(self.server_id, directory)

    def downloadFile(self, path):
        return self.panel.fm_download(self.server_id, path)

    def uploadFile(self, directory, file_data):
        return self.panel.fm_upload(self.server_id, directory, file_data)

    def deleteFiles(self, root, files):
        return self.panel.fm_delete(self.server_id, root, files)

    def renameFiles(self, root, files):
        return self.panel.fm_rename(self.server_id, root, files)

    def copyFiles(self, root, files):
        return self.panel.fm_copy(self.server_id, root, files)

    def moveFiles(self, root, files):
        return self.panel.fm_move(self.server_id, root, files)

    def createFolder(self, directory, name):
        return self.panel.fm_create_folder(self.server_id, directory, name)

    def compress(self, root, files):
        return self.panel.fm_compress(self.server_id, root, files)

    def decompress(self, file_path):
        return self.panel.fm_decompress(self.server_id, file_path)

    # ============================================================
    # BACKUPS
    # ============================================================

    def listBackups(self):
        return self.panel.backups_list(self.server_id)

    def createBackup(self, name="Auto Backup"):
        return self.panel.backups_create(self.server_id, name)

    def deleteBackup(self, backup_id):
        return self.panel.backups_delete(self.server_id, backup_id)

    def downloadBackup(self, backup_id):
        return self.panel.backups_download(self.server_id, backup_id)

    # ============================================================
    # DATABASES
    # ============================================================

    def listDatabases(self):
        return self.panel.db_list(self.server_id)

    def createDatabase(self, name, remote="%", host=None):
        return self.panel.db_create(self.server_id, name, remote, host)

    def rotateDatabasePassword(self, db_id):
        return self.panel.db_rotate_password(self.server_id, db_id)

    def deleteDatabase(self, db_id):
        return self.panel.db_delete(self.server_id, db_id)

    # ============================================================
    # STARTUP VARIABLES
    # ============================================================

    def getStartupVariables(self):
        return self.panel.startup_list(self.server_id)

    def updateStartupVariable(self, key, value):
        return self.panel.startup_update(self.server_id, key, value)

    # ============================================================
    # SCHEDULES
    # ============================================================

    def listSchedules(self):
        return self.panel.schedules_list(self.server_id)

    def createSchedule(self, payload):
        return self.panel.schedules_create(self.server_id, payload)

    def updateSchedule(self, schedule_id, payload):
        return self.panel.schedules_update(self.server_id, schedule_id, payload)

    def deleteSchedule(self, schedule_id):
        return self.panel.schedules_delete(self.server_id, schedule_id)

    def runSchedule(self, schedule_id):
        return self.panel.schedules_run(self.server_id, schedule_id)

    # ============================================================
    # HEALTH SNAPSHOT
    # ============================================================

    def snapshot(self):
        return {
            "ram": self.getRAM(),
            "cpu": self.getCPU(),
            "disk": self.getDisk(),
            "network_in": self.getNetworkIn(),
            "network_out": self.getNetworkOut(),
            "uptime": self.getUptime(),
            "status": self.getStatus()
        }