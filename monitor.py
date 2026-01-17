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

    def is_ignored(self, path):
        filename = os.path.basename(path)
        if filename in self.ignore_list or any(ig in path for ig in self.ignore_list):
            return True
        return False

    def on_modified(self, event):
        if event.is_directory or self.is_ignored(event.src_path):
            return

        new_hash = calc_sha256(event.src_path)
        old_hash = self.baseline.get(os.path.abspath(event.src_path))

        if new_hash != old_hash:
            logging.warning(f"[MODIFIED] - {os.path.relpath(event.src_path)}")
            self.baseline[os.path.abspath(event.src_path)] = new_hash

    def on_created(self, event):
        if event.is_directory or self.is_ignored(event.src_path):
            return

        logging.warning(f"[CREATED] {os.path.relpath(event.src_path)}")
        new_hash = calc_sha256(event.src_path)
        self.baseline[os.path.abspath(event.src_path)] = new_hash

    def on_deleted(self, event):
        if event.is_directory or self.is_ignored(event.src_path):
            return

        logging.warning(f"[DELETED] {os.path.relpath(event.src_path)}")
        abs_path = os.path.abspath(event.src_path)
        if abs_path in self.baseline:
            del self.baseline[abs_path]


def start_realtime_monitor(target_path, baseline, ignores):
    event_handler = AegisHandler(baseline, ignores)
    observer = Observer()
    observer.schedule(event_handler, target_path, recursive=True)
    observer.start()
    logging.info(f"Watching for changes in {target_path}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Real-time monitoring stopped.")
        observer.join()
