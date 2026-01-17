import logging
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from hash_engine import calc_sha256


class AegisHandler(FileSystemEventHandler):
    def __init__(self, baseline, ignore_list):
        super().__init__()
        self.baseline = baseline
        self.ignore_list = ignore_list

    def is_ignored(self, path):
        abs_path = os.path.abspath(path)
        filename = os.path.basename(abs_path)

        if filename in self.ignore_list:
            return True
        return any(ig in abs_path for ig in self.ignore_list)

    def on_modified(self, event):
        if event.is_directory or self.is_ignored(event.src_path):
            return

        abs_path = os.path.abspath(event.src_path)
        new_hash = calc_sha256(abs_path)

        if new_hash is None:
            return

        old_hash = self.baseline.get(abs_path)

        if new_hash != old_hash:
            rel_path = os.path.relpath(abs_path)
            logging.warning(f"[WATCHER] MODIFIED: {rel_path}")
            self.baseline[abs_path] = new_hash

    def on_created(self, event):
        if event.is_directory or self.is_ignored(event.src_path):
            return

        abs_path = os.path.abspath(event.src_path)
        rel_path = os.path.relpath(abs_path)

        logging.warning(f"[WATCHER] CREATED: {rel_path}")

        new_hash = calc_sha256(abs_path)
        if new_hash:
            self.baseline[abs_path] = new_hash

    def on_deleted(self, event):
        if event.is_directory or self.is_ignored(event.src_path):
            return

        abs_path = os.path.abspath(event.src_path)
        rel_path = os.path.relpath(abs_path)

        logging.warning(f"[WATCHER] DELETED: {rel_path}")

        if abs_path in self.baseline:
            del self.baseline[abs_path]


def start_realtime_monitor(target_path, baseline, ignores):
    event_handler = AegisHandler(baseline, ignores)
    observer = Observer()
    observer.schedule(event_handler, target_path, recursive=True)
    observer.start()

    logging, info(f"Real-time monitoring active on: {target_path}")
    logging.info("Press Ctrl-C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Real-time monitoring stopped.")
    finally:
        observer.join()
