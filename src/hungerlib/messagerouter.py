import logging
from pathlib import Path
from datetime import datetime

class MessageRouter:
    def __init__(
        self,
        name,
        server,
        log_path,
        formatter=None,
        console_backspaces=0,

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

    # routing primitives
    def origin(self, msg):
        print(msg)

    def destination(self, msg):
        if not self.server or not hasattr(self.server, "_rcon_send"):
            return
        self.server._rcon_send(
            f'logtellraw targetless "{self.console_backspaces}{msg}"'
        )

    def log(self, msg, level="INFO"):
        {
            "INFO": self.logger.info,
            "WARN": self.logger.warning,
            "ERROR": self.logger.error
        }[level](msg)

    def broadcast(self, msg):
        if hasattr(self.server, "sendBroadcast"):
            self.server.sendBroadcast(msg)

    # high level router
    def say(
        self,
        template,
        level="info",
        destination=False,
        broadcast=False,
        log=True,
        origin=True,
        **fmt
    ):
        if not template:
            return

        if level == "info":
            template = self.info_prefix + template
        elif level == "warn":
            template = self.warn_prefix + template
        elif level == "error":
            template = self.error_prefix + template

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
