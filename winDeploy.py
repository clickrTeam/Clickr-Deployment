
import json
import shutil
import subprocess
import os
import zipfile

# region: File Paths
# Define variables for file locations
user_name = "Lukew"
project_name = "clickr"
build_config = "Release"
qt_version = "6.8.2"


# outside Paths
WINDEPLOYTQT_EXE = f"C:/Qt/{qt_version}/mingw_64/bin/windeployqt.exe"
QT_PROJECT_PATH = f"C:/Users/{user_name}/OneDrive/Desktop/Qt/"
QT_BUILT_EXE = f"{QT_PROJECT_PATH}{project_name}/build/Desktop_Qt_{qt_version.replace('.', '_')}_MinGW_64_bit-{build_config}/keybinder.exe"

ELECTRON = f"C:/Users/{user_name}/OneDrive/Desktop/Qt/clickr-app/app/"
ELECTRON_EXE = f"{ELECTRON}dist/clickr-1.0.0-setup.exe"

# QT file paths
BIN_FOLDER = f"./bin"
QT_BUILD = f"{BIN_FOLDER}/keybinder"
QT_EXE = f"{QT_BUILD}/keybinder.exe"
QT_DEPLOY = f"./keybinder.zip"
QT_STARTUP_PROFILE = f"./startup.json"

## Electron Paths
ELECTRON_TMP = f"{BIN_FOLDER}/clickr-win32-x64"
ELECTRON_BUILD = f"{BIN_FOLDER}/clickr"

# region: QT Build
# Note does not build the QT project, just deploys release build

# Remove the deployment directory if it exists
print(f"Removing {QT_BUILD} if it exists")
shutil.rmtree(QT_BUILD, ignore_errors=True)

# Create the deployment directory
print(f"Creating {QT_BUILD}")
os.makedirs(QT_BUILD, exist_ok=True)

# Copy the executable to the deployment directory
print(f"Copying {QT_BUILT_EXE} to {QT_BUILD}")
shutil.copy2(QT_BUILT_EXE, QT_BUILD)

# Run windeployqt, as i understand it theirs also macdeployqt and linuxdeployqt
print(f"Running windeployqt on {QT_EXE}")
subprocess.run(f'"{WINDEPLOYTQT_EXE}" "{QT_EXE}"', shell=True)

# Copy over default Qt startup profile
# print(f"Copying {QT_STARTUP_PROFILE} to {QT_BUILD}")
# shutil.copy2(QT_STARTUP_PROFILE, QT_BUILD)

# endregion
# region: Electron Build

# Run the electron-builder command
print(f"Running electron-builder on {ELECTRON}")
subprocess.run([ # WIN: needed to run as admin, Initially
    "npm", "run", "build:win"
], shell=True, cwd=ELECTRON)
# endregion

def get_file_size(path):
    try:
        file_size = os.path.getsize(path)
        print(f"The size of the file at {ELECTRON_EXE} is {file_size} bytes")
        print(f"The size of the file at {ELECTRON_EXE} is {file_size / (1024 * 1024):.2f} MB")
    except FileNotFoundError:
        print(f"File not found: {path}")
    
get_file_size(ELECTRON_EXE)

# 8/28/2025 - 85.97 MB / 89.15 MB 