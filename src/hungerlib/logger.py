#!/usr/bin/env python3
import os
os.environ['TZ'] = 'America/Chicago'
import time
time.tzset()

import logging
from pathlib import Path
from datetime import datetime
from hungerlib.config import *


class HungerLogger:
    def __init__(
        self,
        loggerName,
        Config=DefaultConfig,
        logDir=None,
        server=None
    ):
        self.loggerName = loggerName
        self.config = Config
        self.server = server

        self.prefixes = {
            "INFO": self.config.info_prefix,
            "WARN": self.config.warn_prefix,
            "ERROR": self.config.error_prefix
        }
        
        self.log_destination_method = self.config.log_destination_method

        self.logDir = Path(logDir) if logDir else self.config.log_path
        self.logDir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)
        self._initializeLogger()

    def _initializeLogger(self):
        logFile = self.logDir / f"{self.loggerName}_{datetime.now().strftime('%Y-%m-%d')}.log"

        if not self.logger.handlers:
            handler = logging.FileHandler(str(logFile))
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info("Logger initialized.")

    def _apply_colors(self, msg, cmap):
        if not cmap:
            return msg
        for tag, code in cmap.items():
            msg = msg.replace(tag, code)
        return msg

    def _strip_colors(self, msg):
        if not self.config.file_color_map:
            return msg
        for tag in self.config.file_color_map.keys():
            msg = msg.replace(tag, "")
        return msg

    def _destinationLog(self, msg):
        if not self.server:
            return
        if not hasattr(self.server, "_rcon_send"):
            return
        colored = self._apply_colors(msg, self.config.destination_color_map)
        if self.log_destination_method == 'rcon':
            self.server._rcon_send(colored)
        if self.log_destination_method == 'api':
            self.server.sendConsoleCommand(f'logtellraw targetless "{colored}"')
            

    def _log(self, level, msg, destination, origin, logs):
        prefix = self.prefixes[level] + f"[{self.loggerName}] "
        full = prefix + msg

        if destination:
            self._destinationLog(full)

        if origin:
            colored = self._apply_colors(full + "<reset>", self.config.origin_color_map)
            print(colored)

        if logs:
            clean = self._strip_colors(full)
            {
                "INFO": self.logger.info,
                "WARN": self.logger.warning,
                "ERROR": self.logger.error
            }[level](clean)

    def info(self, msg, destination=False, origin=True, logs=True):
        self._log("INFO", msg, destination, origin, logs)

    def warn(self, msg, destination=False, origin=True, logs=True):
        self._log("WARN", msg, destination, origin, logs)

    def error(self, msg, destination=False, origin=True, logs=True):
        self._log("ERROR", msg, destination, origin, logs)
