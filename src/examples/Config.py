from hungerlib import Config, Panel
from pathlib import Path
from hungerlib.addons.colormap import ASCI_COLOR_MAP, MC_COLOR_MAP

ExampleConfig = Config(

    # Color maps
    file_color_map=None,
    origin_color_map=ASCI_COLOR_MAP.copy(),
    destination_color_map=ASCI_COLOR_MAP.copy(),
    mc_color_map=MC_COLOR_MAP.copy(),

    
    # --- Prefixes ---
    info_prefix='<white>[INFO]: ',
    warn_prefix='<yellow>[WARN]: ',
    error_prefix='<red>[ERROR]: ',
    console_backspaces=8,

    # --- Logging ---
    log_path=Path("/home/container/logs"),
    log_destination_method='rcon',

)