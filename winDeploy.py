###
### This script is used to deploy a Qt application on Windows using windeployqt.
### Please do not alter it on any non-windows system, as it is specifically designed for Windows.
### Feel free to modify paths as needed, and use code for other deployments as a reference.
###

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

QT_PROJECT_PATH = f"C:/Users/{user_name}/OneDrive/Desktop/Qt/"

# Construct file paths
exe_path = f"{QT_PROJECT_PATH}{project_name}/build/Desktop_Qt_{qt_version.replace('.', '_')}_MinGW_64_bit-{build_config}/keybinder.exe"
# exe_path = f"{QT_PROJECT_PATH}{project_name}/build/Desktop_Qt_{qt_version}_MinGW_64_bit-{build_config}/keybinder.exe"
QT_BUILD = f"{QT_PROJECT_PATH}deployment/keybinder"
deploy_path = f"{QT_PROJECT_PATH}deployment/keybinder/keybinder.exe"
windeployqt_path = f"C:/Qt/{qt_version}/mingw_64/bin/windeployqt.exe"

## Electron Paths
ELECTRON = f"C:/Users/{user_name}/OneDrive/Desktop/Qt/clickr-app/app/"
ELECTRON_TMP = f"./clickr-win32-x64"
ELECTRON_BUILD = f"./clickr"
ELECTRON_EXE = f"{ELECTRON}dist/clickr-1.0.0-setup.exe"

# endregion
# region: QT Build

def Qt_build():
    # Remove the deployment directory if it exists
    print(f"Removing {QT_BUILD} if it exists")
    shutil.rmtree(QT_BUILD, ignore_errors=True)

    # Create the deployment directory
    print(f"Creating {QT_BUILD}")
    os.makedirs(QT_BUILD, exist_ok=True)

    # Copy the executable to the deployment directory
    print(f"Copying {exe_path} to {QT_BUILD}")
    shutil.copy2(exe_path, QT_BUILD)

    # Change the current working directory to the deployment directory
    # print(f"Changing directory to {deploy_dir}")
    # os.chdir(deploy_dir)

    # Run windeployqt, as i understand it theirs also macdeployqt and linuxdeployqt
    print(f"Running windeployqt on {deploy_path}")
    subprocess.run(f'"{windeployqt_path}" "{deploy_path}"', shell=True)

# endregion
# region: Electron Build

# NEW - smaller ~16.23 MB file size
def Electron_build():
    # Remove the deployment directory if it exists
    print(f"Removing {ELECTRON_BUILD} if it exists")
    shutil.rmtree(ELECTRON_BUILD, ignore_errors=True)
    os.makedirs(ELECTRON_BUILD, exist_ok=True)

    # Run the electron-builder command
    print(f"Running electron-builder on {ELECTRON}")
    subprocess.run([ # WIN: needed to run as admin, Initially
        "electron-builder",
        "build",
        "--win",
        "--x64",
    ], shell=True, cwd=ELECTRON)

    print(f"Copying {ELECTRON} to {ELECTRON_BUILD}")
    destination_path = os.path.join(os.getcwd(), "clickr-1.0.0-setup.exe")
    shutil.copy(ELECTRON_EXE, ELECTRON_BUILD)

# OLD - big ~367.39 MB file size
# def Electron_build():
#     # Remove the deployment directory if it exists
#     print(f"Removing {ELECTRON_BUILD} if it exists")
#     shutil.rmtree(ELECTRON_BUILD, ignore_errors=True)

#     # Package the Electron app
#     print(f"Running electron-packager on {ELECTRON}")
#     subprocess.run(f"electron-packager --compress --prune {ELECTRON}", shell=True) # 

#     print(f"Rename folder {ELECTRON_TMP}")
#     os.rename(ELECTRON_TMP, ELECTRON_BUILD)

    # Define the build options

# endregion
# region: Zip, Run, Size

output_zip_path = f"C:/Users/Lukew/OneDrive/Desktop/Qt/deployment/out.zip"
# output_zip = f"{output_zip_path}/clickr.zip"
def zip_out(folder1_path, folder2_path):
    print(f"Zipping {folder1_path} and {folder2_path} to {output_zip_path}")
    # os.remove(file_path)
    # Create a ZipFile object
    with zipfile.ZipFile(output_zip_path, 'w') as zip_file:
        # Walk through the first folder and add its contents to the zip file
        for root, dirs, files in os.walk(folder1_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, start=os.path.dirname(folder1_path))
                zip_file.write(file_path, rel_path)

        # Walk through the second folder and add its contents to the zip file
        for root, dirs, files in os.walk(folder2_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, start=os.path.dirname(folder2_path))
                zip_file.write(file_path, rel_path)

# Build the apps
Qt_build()
Electron_build()
zip_out(ELECTRON_BUILD, QT_BUILD)

file_size = os.path.getsize(output_zip_path)
if file_size < 1024:
    print(f'The size of the zip file is {file_size} bytes')
elif file_size < 1024 ** 2:
    print(f'The size of the zip file is {file_size / 1024:.2f} KB')
elif file_size < 1024 ** 3:
    print(f'The size of the zip file is {file_size / (1024 ** 2):.2f} MB')
else:
    print(f'The size of the zip file is {file_size / (1024 ** 3):.2f} GB')

# OG: zip file is 367.39 MB
# Keybinder is 16.23 MB