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

_internal_config = Config()