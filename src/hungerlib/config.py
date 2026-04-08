# HungerLib's core config system

from dataclasses import dataclass, field
from pathlib import Path
from hungerlib.colormap import *

@dataclass
class Config:
    file_color_map: dict | None = None
    origin_color_map: dict = field(default_factory=lambda: ASCI_COLOR_MAP.copy())
    destination_color_map: dict = field(default_factory=lambda: ASCI_COLOR_MAP.copy())
    mc_color_map: dict = field(default_factory=lambda: MC_COLOR_MAP.copy())

    info_prefix: str = '<white>[INFO]: '
    warn_prefix: str = '<yellow>[WARN]: '
    error_prefix: str = '<red>[ERROR]: '

    log_path: Path = Path("/home/container/logs")
    log_destination_method: str = 'rcon'

DefaultConfig = Config()
