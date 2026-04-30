import logging
from pathlib import Path
from datetime import datetime
from hungerlib.addons import clrz, ASCII_COLOR_MAP, MC_COLOR_MAP


class MessageRouter:
    def __init__(
        self,
        name,
        server,
        log_path,
        formatter=None,
        console_backspaces=0,

        origin_map=ASCII_COLOR_MAP,
        destination_map=MC_COLOR_MAP,
        broadcast_map=MC_COLOR_MAP,
        log_map=None,

        info_prefix="<white>[INFO]: ",
        warn_prefix="<yellow>[WARN]: ",
        error_prefix="<red>[ERROR]: "
    ):
        self.name = name
        self.server = server
        self.formatter = formatter

        self.log_path = Path(log_path)
        self.log_path.mkdir(parents=True, exist_ok=True)

        self.console_backspaces = "\b" * console_backspaces

        self._origin_map = origin_map
        self._destination_map = destination_map
        self._broadcast_map = broadcast_map
        self._log_map = log_map

        self.info_prefix = info_prefix
        self.warn_prefix = warn_prefix
        self.error_prefix = error_prefix

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._init_file_logger()

    def _init_file_logger(self):
        log_file = self.log_path / f"{self.name}_{datetime.now().strftime('%Y-%m-%d')}.log"
        if not self.logger.handlers:
            handler = logging.FileHandler(str(log_file))
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    # colormap getters/setters
    def setOriginMap(self, cmap): self._origin_map = cmap
    def getOriginMap(self): return self._origin_map

    def setDestinationMap(self, cmap): self._destination_map = cmap
    def getDestinationMap(self): return self._destination_map

    def setBroadcastMap(self, cmap): self._broadcast_map = cmap
    def getBroadcastMap(self): return self._broadcast_map

    def setLogMap(self, cmap): self._log_map = cmap
    def getLogMap(self): return self._log_map

    # routing primatives
    def origin(self, msg):
        colored = clrz(msg, cmap=self._origin_map)
        print(colored)

    def destination(self, msg):
        if not self.server or not hasattr(self.server, "_rcon_send"):
            return
        colored = clrz(msg, cmap=self._destination_map)
        self.server._rcon_send(
            f'logtellraw targetless "{self.console_backspaces}{colored}"'
        )

    def log(self, msg, level="INFO"):
        clean = msg
        if self._log_map:
            for tag in self._log_map.as_dict().keys():
                clean = clean.replace(tag, "")
        {
            "INFO": self.logger.info,
            "WARN": self.logger.warning,
            "ERROR": self.logger.error
        }[level](clean)

    def broadcast(self, msg):
        if hasattr(self.server, "sendBroadcast"):
            colored = clrz(msg, cmap=self._broadcast_map)
            self.server.sendBroadcast(colored)

    # high level router
    def say(
        self,
        template,
        level="info",
        origin=True,
        destination=False,
        log=True,
        broadcast=False,
        **fmt
    ):
        if not template:
            return

        if self.formatter:
            msg = self.formatter(template, **fmt)
        else:
            msg = template

        if origin:
            self.origin(msg)

        if destination:
            self.destination(msg)

        if log:
            self.log(msg, level=level.upper())

        if broadcast:
            self.broadcast(msg)

    # level helpers
    def info(self, template, **fmt):
        self.say(self.info_prefix + template, level="info", **fmt)

    def warn(self, template, **fmt):
        self.say(self.warn_prefix + template, level="warn", **fmt)

    def error(self, template, **fmt):
        self.say(self.error_prefix + template, level="error", **fmt)
