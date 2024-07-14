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

def monitor_ftp():
    while True:
        try:
            with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
                ftp.cwd('/')
                files = ftp.nlst()
                for file in files:
                    if file.endswith('.xml'):
                        local_temp_filename = os.path.join(TEMP_DIR, file)
                        if not os.path.exists(local_temp_filename):
                            download_file(file)
        except Exception as e:
            print(f"Error connecting to FTP server: {e}")
        time.sleep(10)

def process_xml_file(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        data = {child.tag: child.text for child in root}
        print(f"Processed XML to Dictionary: {data}")
        return data
    except ET.ParseError as e:
        print(f"Error parsing XML file {filepath}: {e}")
        return {}

def move_to_trash(filepath):
    try:
        destination = os.path.join(TRASH_DIR, os.path.basename(filepath))
        shutil.move(filepath, destination)
        print(f"Moved to Trash: {filepath} to {destination}")
    except Exception as e:
        print(f"Error moving file to trash {filepath}: {e}")

def on_new_file(event):
    if event.is_directory or not event.src_path.endswith('.xml'):
        return
    print(f"New file in LOCAL_DIR: {event.src_path}")
    data = process_xml_file(event.src_path)
    move_to_trash(event.src_path)

class LocalFolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        on_new_file(event)

if __name__ == "__main__":
    # Start monitoring the FTP server
    ftp_thread = threading.Thread(target=monitor_ftp)
    ftp_thread.daemon = True
    ftp_thread.start()

    # Start monitoring the LOCAL_DIR
    local_observer = Observer()
    event_handler = LocalFolderHandler()
    local_observer.schedule(event_handler, LOCAL_DIR, recursive=False)
    local_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        local_observer.stop()
    local_observer.join()