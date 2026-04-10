# =====================================
#         CORE CONFIG SYSTEM
# =====================================
# The variables in this file can be used to control many things in Hungerlib's functions.
# It helps keep track of constants and serves as an easy-to-use configuration system.

from dataclasses import dataclass, field
from pathlib import Path
from hungerlib.addons.colormap import *

@dataclass
class Config:
    # panel defaults
    panel_name: str | None = None
    panel_url: str | None = None
    panel_api_key: str | None = None

    # generic server defaults
    gs_name: str | None = None
    gs_panel_url: str | None = None
    gs_panel_api_key: str | None = None
    gs_server_id: str | None = None

    # minecraft server defaults
    mc_name: str | None = None
    mc_panel_url: str | None = None
    mc_panel_api_key: str | None = None
    mc_server_id: str | None = None
    mc_server_domain: str | None = None
    mc_server_port: int = 25565
    mc_rcon_port: int = 25575
    mc_rcon_password: str | None = None
    mc_tpsCommand: str = 'tt20 tps'

    # Color maps
    file_color_map: dict | None = None
    origin_color_map: dict = field(default_factory=lambda: ASCI_COLOR_MAP.copy())
    destination_color_map: dict = field(default_factory=lambda: ASCI_COLOR_MAP.copy())
    mc_color_map: dict = field(default_factory=lambda: MC_COLOR_MAP.copy())

    # Prefixes
    info_prefix: str = '<white>[INFO]: '
    warn_prefix: str = '<yellow>[WARN]: '
    error_prefix: str = '<red>[ERROR]: '
    console_backspaces: int = 8

    # Logging
    log_path: Path = Path("/home/container/logs")
    log_destination_method: str = 'rcon'
    