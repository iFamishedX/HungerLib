import requests


class Panel:
    def __init__(self, name, url, api_key):
        self.name = name
        self.url = url.rstrip("/")
        self.api_key = api_key

    def __str__(self):
        return f'Panel name: {self.name}\nURL: {self.url}\nAPI key: {self.api_key}'

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    # -----------------------------
    # BASIC HTTP
    # -----------------------------
    def get(self, path, timeout=5):
        return requests.get(f"{self.url}{path}", headers=self.headers, timeout=timeout)

    def post(self, path, json=None, timeout=5):
        return requests.post(f"{self.url}{path}", headers=self.headers, json=json, timeout=timeout)

    def delete(self, path, timeout=5):
        return requests.delete(f"{self.url}{path}", headers=self.headers, timeout=timeout)

    def patch(self, path, json=None, timeout=5):
        return requests.patch(f"{self.url}{path}", headers=self.headers, json=json, timeout=timeout)

    # -----------------------------
    # PANEL STATUS
    # -----------------------------
    def ping(self):
        try:
            r = self.get("/api/client")
            return r.status_code == 200
        except:
            return False

    def validateAPI(self):
        r = self.get("/api/client/account")
        return r.status_code == 200

    # ============================================================
    # FILE MANAGER API (RAW ENDPOINTS)
    # ============================================================

    def fm_list(self, server_id, directory="/"):
        return self.get(f"/api/client/servers/{server_id}/files/list?directory={directory}")

    def fm_download(self, server_id, file_path):
        return self.get(f"/api/client/servers/{server_id}/files/download?file={file_path}")

    def fm_upload(self, server_id, directory, file_data):
        # file_data must be multipart/form-data
        return requests.post(
            f"{self.url}/api/client/servers/{server_id}/files/upload",
            headers={"Authorization": f"Bearer {self.api_key}"},
            files=file_data
        )

    def fm_delete(self, server_id, root, files):
        payload = {"root": root, "files": files}
        return self.post(f"/api/client/servers/{server_id}/files/delete", json=payload)

    def fm_rename(self, server_id, root, files):
        payload = {"root": root, "files": files}
        return self.post(f"/api/client/servers/{server_id}/files/rename", json=payload)

    def fm_copy(self, server_id, root, files):
        payload = {"root": root, "files": files}
        return self.post(f"/api/client/servers/{server_id}/files/copy", json=payload)

    def fm_move(self, server_id, root, files):
        payload = {"root": root, "files": files}
        return self.post(f"/api/client/servers/{server_id}/files/move", json=payload)

    def fm_create_folder(self, server_id, directory, name):
        payload = {"root": directory, "name": name}
        return self.post(f"/api/client/servers/{server_id}/files/create-folder", json=payload)

    def fm_compress(self, server_id, root, files):
        payload = {"root": root, "files": files}
        return self.post(f"/api/client/servers/{server_id}/files/compress", json=payload)

    def fm_decompress(self, server_id, file_path):
        payload = {"file": file_path}
        return self.post(f"/api/client/servers/{server_id}/files/decompress", json=payload)

    # ============================================================
    # BACKUPS API
    # ============================================================

    def backups_list(self, server_id):
        return self.get(f"/api/client/servers/{server_id}/backups")

    def backups_create(self, server_id, name="Auto Backup"):
        payload = {"name": name}
        return self.post(f"/api/client/servers/{server_id}/backups", json=payload)

    def backups_delete(self, server_id, backup_id):
        return self.delete(f"/api/client/servers/{server_id}/backups/{backup_id}")

    def backups_download(self, server_id, backup_id):
        return self.get(f"/api/client/servers/{server_id}/backups/{backup_id}/download")

    # ============================================================
    # DATABASES API
    # ============================================================

    def db_list(self, server_id):
        return self.get(f"/api/client/servers/{server_id}/databases")

    def db_create(self, server_id, name, remote="%", host=None):
        payload = {"database": name, "remote": remote}
        if host:
            payload["host"] = host
        return self.post(f"/api/client/servers/{server_id}/databases", json=payload)

    def db_rotate_password(self, server_id, db_id):
        return self.post(f"/api/client/servers/{server_id}/databases/{db_id}/rotate-password")

    def db_delete(self, server_id, db_id):
        return self.delete(f"/api/client/servers/{server_id}/databases/{db_id}")

    # ============================================================
    # STARTUP VARIABLES API
    # ============================================================

    def startup_list(self, server_id):
        return self.get(f"/api/client/servers/{server_id}/startup")

    def startup_update(self, server_id, key, value):
        payload = {"key": key, "value": value}
        return self.post(f"/api/client/servers/{server_id}/startup/variable", json=payload)

    # ============================================================
    # SCHEDULES API
    # ============================================================

    def schedules_list(self, server_id):
        return self.get(f"/api/client/servers/{server_id}/schedules")

    def schedules_create(self, server_id, payload):
        return self.post(f"/api/client/servers/{server_id}/schedules", json=payload)

    def schedules_update(self, server_id, schedule_id, payload):
        return self.patch(f"/api/client/servers/{server_id}/schedules/{schedule_id}", json=payload)

    def schedules_delete(self, server_id, schedule_id):
        return self.delete(f"/api/client/servers/{server_id}/schedules/{schedule_id}")

    def schedules_run(self, server_id, schedule_id):
        return self.post(f"/api/client/servers/{server_id}/schedules/{schedule_id}/execute")

    # ============================================================
    # COMMAND API
    # ============================================================

    def sendCommand(self, server_id, command):
        payload = {"command": command}
        return self.post(f"/api/client/servers/{server_id}/command", json=payload)
