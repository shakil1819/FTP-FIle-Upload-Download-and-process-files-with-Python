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