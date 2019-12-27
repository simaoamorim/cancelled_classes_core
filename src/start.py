#!/usr/bin/env python3

import datetime
import logging
import os
import os.path
import sys


class Launcher:
    def __init__(self):
        self.logger = ...
        self.file_handler = ...
        self.init_logger()
        self.logger.info("Starting server...")

    def init_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("(%(asctime)s.%(msecs)d) [%(levelname)s]: \"%(name)s\": %(message)s",
                                      "%d-%m-%Y %H:%M:%S")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.WARNING)
        if not os.path.exists("log/"):
            os.mkdir("log/")
        self.file_handler = logging.FileHandler(
            format("log/%s.log" % datetime.datetime.__format__(datetime.datetime.now(), "%d_%m_%Y"))
        )
        self.file_handler.setFormatter(formatter)
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.stream.write(f"###### Opened log file on "
                                       f"{datetime.time.isoformat(datetime.datetime.now().time())}"
                                       f" ######\n")

        self.logger.addHandler(console_handler)
        self.logger.addHandler(self.file_handler)

    def cleanup(self):
        self.logger.info("Shutting down server...")
        self.logger.info("Closing logs...")
        self.file_handler.stream.write(f"###### Closed log file on"
                                       f"{datetime.time.isoformat(datetime.datetime.now().time())}"
                                       f" ######\n\n")
        logging.shutdown()


if __name__ == "__main__":
    app = Launcher()
    app.cleanup()
    sys.exit(0)
