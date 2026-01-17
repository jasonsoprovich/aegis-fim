import logging
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from hash_engine import calc_sha256


class AegisHandler(FileSystemEventHandler):
    def __init__(self, baseline, ignore_list):
        self.baseline = baseline
        self.ignore_list = ignore_list

        def on_modified(self, event):
            if event.is_directory:
                return

            filename = os.path.basename(even.src_path)
            if filename in self.ignore_list or any(
                ig in event.src_path for ig in self.ignore_list
            ):
                return

            new_hash = calc_sha256(event.src_path)
            old_hash = self.baseline.get(os.path.abspath(event.src_path))

            if new_hash != old_hash:
                logging.warning(
                    f"REAL-TIME: Modified - {os.path.relpath(event.src_path)}"
                )
                self.baseline[os.path.abspath(even.src_path)] = new_hash
