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
    ):
        self.name = name
        self.server = server
        self.formatter = formatter

        self.log_path = Path(log_path)
        self.log_path.mkdir(parents=True, exist_ok=True)

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
    def _log_origin(self, msg):
        print(msg)

    def _log_destination(self, msg):
        if hasattr(self.server, "bridge"):
            self.server.bridge.log(msg)

    def _log_file(self, msg, level="INFO"):
        {
            "INFO": self.logger.info,
            "WARN": self.logger.warning,
            "ERROR": self.logger.error
        }[level](msg)

    def _broadcast(self, msg):
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

        if self.formatter:
            msg = self.formatter(template, **fmt)
        else:
            msg = template

        if origin:
            self._log_origin(msg)

        if destination:
            self._log_destination(msg)

        if log:
            self._log_file(msg, level=level.upper())

        if broadcast:
            self._broadcast(msg)

    # level helpers
    def info(self, template, **fmt):
        self.say(template, level="info", **fmt)

    def warn(self, template, **fmt):
        self.say(template, level="warn", **fmt)

    def error(self, template, **fmt):
        self.say(template, level="error", **fmt)
