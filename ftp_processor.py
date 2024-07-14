import os
import ftplib
import time
import shutil
import threading
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


FTP_HOST = "localhost"
FTP_USER = "nybsys"
FTP_PASS = "12345"


TEMP_DIR = "./TEMP"
LOCAL_DIR = "./LOCAL"
TRASH_DIR = "./TRASH"

for directory in [TEMP_DIR, LOCAL_DIR, TRASH_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

class FTPDownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.xml'):
            return
        move_to_local(event.src_path)


def download_file(filepath):
    try:
        with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
            ftp.cwd('/')
            local_temp_filename = os.path.join(TEMP_DIR, os.path.basename(filepath))
            with open(local_temp_filename, 'wb') as local_file:
                ftp.retrbinary(f"RETR {os.path.basename(filepath)}", local_file.write)
            print(f"Downloaded: {local_temp_filename}")
            move_to_local(local_temp_filename)
    except Exception as e:
        print(f"Error downloading file {filepath}: {e}")
        
def move_to_local(filepath):
    try:
        destination = os.path.join(LOCAL_DIR, os.path.basename(filepath))
        shutil.move(filepath, destination)
        print(f"Moved: {filepath} to {destination}")
    except Exception as e:
        print(f"Error moving file {filepath}: {e}")