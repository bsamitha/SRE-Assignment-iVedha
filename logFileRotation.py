#!/usr/bin/env python3

"""
-------------------Log File Rotation Automation-------------------

Requires Python 3.13.2

This script automates log file rotation for the /var/logs/ directory.
    - Monitors log files in /var/logs/ for size exceeding 100MB.
    - Compresses and archives oversize log files to /var/logs/archive/.
    - Deletes archived log files older than 30 days to save disk space.

Developer Test Data:
log_dir = "C:\\Users\\Laptop Outlet\\Desktop\\Interview\\test data\\log"
archive_dir = "C:\\Users\\Laptop Outlet\\Desktop\\Interview\\test data\\log\\archive"
size_limit = 10000
delete_older_than = 120

Note: This is real-time monitoring and can be deployed as a systemd service

-------------------DeveloperTested-------------------
"""


import os
import gzip
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log_dir = "/var/logs/"
archive_dir = "/var/logs/archive"
size_limit = 104857600
delete_older_than = 2592000

os.makedirs(archive_dir, exist_ok=True)


def cleanup_archives():
    current_time = time.time()
    for file_name in os.listdir(archive_dir):
        file_path = os.path.join(archive_dir, file_name)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > delete_older_than:
                os.remove(file_path)
                print(f"Deleted old archive: {file_name}")


class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                if file_size > size_limit:
                    file_name = os.path.basename(file_path)
                    compressed_file_path = os.path.join(archive_dir, f"{file_name}.gz")
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(compressed_file_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    print(f"Archived: {file_name} ({file_size} bytes)")
                    os.remove(file_path)


if __name__ == "__main__":
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path=log_dir, recursive=False)
    observer.start()
    print(f"Watching directory: {log_dir}")

    try:
        while True:
            cleanup_archives()
            time.sleep(30)  # check every 30 seconds for remove archive
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
