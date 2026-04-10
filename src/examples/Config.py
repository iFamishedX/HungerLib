from hungerlib import Config
from pathlib import Path
from hungerlib.addons.colormap import ASCI_COLOR_MAP, MC_COLOR_MAP

ExampleConfig = Config(
    # --- Panel settings ---
    panel_name="My Panel",
    panel_url="https://example.com",
    panel_api_key='API_KEY_HERE',
    
    # --- Generic server settings ---
    gs_name='My Server',
    gs_panel_url='https://example.com',
    gs_panel_api_key='API_KEY_HERE',
    gs_server_id='SERVER_ID_HERE',

    # --- Minecraft server settings ---
    mc_name='My Minecraft Server',
    mc_panel_url='https://example.com',
    mc_panel_api_key='API_KEY_HERE',
    mc_server_id='SERVER_ID_HERE',
    mc_server_domain='mc.example.com',
    mc_server_port=25565,
    mc_rcon_port=25575,
    mc_rcon_password='RCON_PASSWORD_HERE',
    mc_tpsCommand='tt20 tps',

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