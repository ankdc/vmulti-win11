# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for VMulti Driver Installer - Consolidated Edition
This spec file builds the consolidated driver_installer.py into a standalone executable.
"""
import os
import glob
from pathlib import Path

block_cipher = None

# Get current directory
current_dir = os.path.abspath(os.path.dirname(SPEC))

# Path to driver_dist folder
driver_dist_dir = os.path.join(current_dir, 'driver_dist')

# Create a list of data files to include
data_files = []

# Add all files in driver_dist recursively if it exists
if os.path.exists(driver_dist_dir):
    for folder, _, files in os.walk(driver_dist_dir):
        for file in files:
            file_path = os.path.join(folder, file)
            # Calculate relative path from driver_dist directory to preserve structure
            rel_path = os.path.relpath(folder, driver_dist_dir)
            if rel_path == '.':
                # File is directly in driver_dist
                target_dir = 'driver_dist'
            else:
                # File is in subdirectory
                target_dir = os.path.join('driver_dist', rel_path)
            data_files.append((file_path, target_dir))

# Add devcon.exe files from Windows Kits
devcon_x64 = r"C:\Program Files (x86)\Windows Kits\10\Tools\10.0.26100.0\x64\devcon.exe"
devcon_arm64 = r"C:\Program Files (x86)\Windows Kits\10\Tools\10.0.26100.0\arm64\devcon.exe"

if os.path.exists(devcon_x64):
    data_files.append((devcon_x64, 'driver_dist/x64'))
    print(f"Adding x64 devcon.exe to package")
else:
    print(f"WARNING: x64 devcon.exe not found at: {devcon_x64}")

if os.path.exists(devcon_arm64):
    data_files.append((devcon_arm64, 'driver_dist/ARM64'))
    print(f"Adding ARM64 devcon.exe to package")
else:
    print(f"WARNING: ARM64 devcon.exe not found at: {devcon_arm64}")

# Create the executable
a = Analysis(
    ['driver_installer.py'],
    pathex=[current_dir],
    binaries=[],
    datas=data_files,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'logging',
        'logging.handlers',
        'threading',
        'subprocess',
        'ctypes',
        'pathlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # Not needed, reduce size
        'numpy',       # Not needed, reduce size
        'PIL',         # Not needed, reduce size
        'PyQt5',       # Not needed, reduce size
        'PyQt6',       # Not needed, reduce size
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VMulti_Driver_Installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False for GUI mode, True for console mode
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(current_dir, 'driver_dist', 'icon.ico') if os.path.exists(os.path.join(current_dir, 'driver_dist', 'icon.ico')) else None,
    uac_admin=True,  # Request admin privileges automatically
)

# Create console version as well
exe_console = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VMulti_Driver_Installer_CLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Console version for CLI usage
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,  # Request admin privileges automatically
)

coll = COLLECT(
    exe,
    exe_console,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VMulti_Driver_Installer',
)