import os
import ftplib
import time
import shutil
import threading
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler