### Project Overview

This project provides a complete solution to download, process, and manage XML files from an FTP server. It includes a Dockerized FTP server, a Python script for handling the files, and a FastAPI-based REST API for uploading, retrieving, and managing the files.

### Getting Started

Follow these steps to set up and run the project:

### 1. Run Docker Compose

First, ensure you have Docker and Docker Compose installed on your system. Then, start the FTP server using Docker Compose:

```bash
docker-compose up -d
```

This command will start the FTP server in detached mode.

### 2. Upload Files Using FileZilla

Next, upload your XML files to the FTP server using FileZilla or any other FTP client. Use the following credentials:

- **Host**: `localhost`
- **Port**: `21`
- **Username**: `nybsys`
- **Password**: `12345`

### 3. Execute the Python Script

Run the Python script to start processing the files:

```bash
python3 ftp_processor.py
```

This script will:

- Download XML files from the FTP server to a temporary folder.
- Move the downloaded files to a local folder.
- Process the XML files to extract data into a dictionary.
- Move the processed files to a trash folder.


### Project Files

- **docker-compose.yml**: Defines the FTP server setup.
- **ftp_processor.py**: Python script for downloading, processing, and managing XML files.
