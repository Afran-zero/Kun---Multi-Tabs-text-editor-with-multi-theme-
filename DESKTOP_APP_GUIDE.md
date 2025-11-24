# 🖥️ Kun Desktop Application Guide

> **Complete guide to package Kun as a standalone desktop application**

This guide walks you through creating a professional desktop application for Windows, with options for other platforms. You'll learn how to create an executable, add icons, and set up file associations.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Method 1: PyInstaller (Recommended)](#method-1-pyinstaller-recommended)
4. [Method 2: cx_Freeze (Alternative)](#method-2-cx_freeze-alternative)
5. [Method 3: Nuitka (Advanced)](#method-3-nuitka-advanced)
6. [Creating an Icon](#creating-an-icon)
7. [File Associations](#file-associations)
8. [Creating an Installer](#creating-an-installer)
9. [Distribution](#distribution)
10. [Troubleshooting](#troubleshooting)

---

## Overview

### What You'll Create

- **Standalone .exe** - Single executable file (or folder with dependencies)
- **Desktop Icon** - Custom icon for your application
- **File Associations** - Double-click .txt files to open in Kun
- **Start Menu Entry** - Easy access from Windows Start Menu
- **Optional Installer** - Professional installer for distribution

### Estimated Time
- **Basic .exe**: 15-30 minutes
- **With icon and installer**: 1-2 hours

---

## Prerequisites

### Required Software
- **Python 3.8+** installed and working
- **Kun working** - Test with `python main.py` first
- **pip** - Python package installer
- **Git Bash or PowerShell** - For running commands

### Recommended
- **Image editor** (for icon creation): GIMP, Photoshop, or online tools
- **Text editor** - For editing configuration files
- **Inno Setup** (for Windows installer): Free installer creation tool

---

## Method 1: PyInstaller (Recommended)

**Best for:** Quick and easy executable creation with good compatibility.

### Step 1: Install PyInstaller

```powershell
pip install pyinstaller
```

### Step 2: Create Build Configuration

Create a file named `kun.spec` in your Kun directory:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('config', 'config'),
        ('core', 'core'),
        ('ui', 'ui'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'pyspellchecker',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='Kun',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',  # Add icon (create this first)
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Kun',
)
```

### Step 3: Build the Application

**Option A: One-folder bundle (easier to debug)**
```powershell
pyinstaller kun.spec
```

**Option B: One-file bundle (single .exe)**
```powershell
pyinstaller --onefile --windowed --name Kun --icon=assets/icon.ico main.py
```

### Step 4: Find Your Application

- **One-folder**: `dist/Kun/Kun.exe`
- **One-file**: `dist/Kun.exe`

### Step 5: Test the Application

1. Navigate to the `dist` folder
2. Double-click `Kun.exe`
3. Test all features (open files, save, themes, etc.)
4. Try opening a .txt file as an argument

### Step 6: Clean Build (if needed)

```powershell
# Remove old builds
Remove-Item -Recurse -Force build, dist
# Rebuild
pyinstaller kun.spec
```

---

## Method 2: cx_Freeze (Alternative)

**Best for:** Cross-platform support, more control over dependencies.

### Step 1: Install cx_Freeze

```powershell
pip install cx_Freeze
```

### Step 2: Create Setup Script

Create `setup_freeze.py`:

```python
import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["PyQt6", "pyspellchecker"],
    "include_files": [
        ("assets", "assets"),
        ("config", "config"),
        ("core", "core"),
        ("ui", "ui"),
    ],
    "excludes": ["tkinter"],
}

# GUI application (no console)
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Kun",
    version="1.0.0",
    description="Lightweight text editor",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="Kun.exe",
            icon="assets/icon.ico",  # Add icon
        )
    ],
)
```

### Step 3: Build

```powershell
python setup_freeze.py build
```

### Step 4: Find Application

Look in `build/exe.win-amd64-3.x/Kun.exe`

---

## Method 3: Nuitka (Advanced)

**Best for:** Maximum performance, true native compilation.

### Step 1: Install Nuitka

```powershell
pip install nuitka
```

### Step 2: Install C Compiler (Windows)

Download and install **MinGW-w64** or **Microsoft Visual C++ Build Tools**

### Step 3: Build with Nuitka

```powershell
python -m nuitka --standalone --windows-disable-console --enable-plugin=pyqt6 --include-data-dir=assets=assets --include-data-dir=config=config --windows-icon-from-ico=assets/icon.ico --output-dir=dist main.py
```

### Step 4: Test

Application will be in `dist/main.dist/main.exe`

---

## Creating an Icon

### Quick Icon Creation (Online)

1. **Create or find an image** (PNG, 256x256 or larger)
2. **Use an online converter**:
   - https://convertio.co/png-ico/
   - https://icoconvert.com/
   - https://favicon.io/
3. **Upload your image**
4. **Select sizes**: 16x16, 32x32, 48x48, 256x256
5. **Download as .ico**
6. **Save to**: `X:\Kun\assets\icon.ico`

### Design Suggestions for Kun Icon

**Theme: Minimalist Text Editor**
- **Simple letter "K"** in elegant font
- **Moon symbol** (🌙) - matches "Kun" theme
- **Pencil/pen icon** - writing theme
- **Document icon** with "K" overlay

**Colors:**
- Noir theme: White/light gray on dark background
- PixelPop: Neon cyan (#00ffff) or magenta (#ff00ff)
- CuteBlush: Soft pink (#ffb3d9)

### Icon Design Tools

**Free:**
- **GIMP** - Full-featured image editor
- **Paint.NET** - Simple Windows editor
- **Inkscape** - Vector graphics (best for icons)
- **Figma** - Online design tool

**Online:**
- **Canva** - Easy templates
- **Pixlr** - Quick editing
- **Photopea** - Photoshop alternative

### Icon Template (Photoshop/GIMP)

```
Canvas: 512x512px
Background: Dark gray (#2a2a2a) or transparent

Layer 1: Large "K" letter
  - Font: Consolas Bold or Segoe UI
  - Size: 400px
  - Color: White or #00ffff
  - Center aligned

Layer 2: Subtle glow (optional)
  - Outer glow effect
  - Color: Accent color
  - Blur: 10px

Export: PNG with transparency
Convert: To .ico with multiple sizes
```

---

## File Associations

### Method 1: Manual Registry Edit (Advanced)

**⚠️ Warning: Backup registry before editing**

1. **Open Registry Editor** (`Win+R`, type `regedit`)

2. **Navigate to**: `HKEY_CLASSES_ROOT\.txt`

3. **Create new key**: `HKEY_CLASSES_ROOT\Kun.TextFile`

4. **Add string values**:
   ```
   (Default) = "Kun Text File"
   ```

5. **Create subkey**: `HKEY_CLASSES_ROOT\Kun.TextFile\shell\open\command`

6. **Set value**:
   ```
   (Default) = "C:\Path\To\Kun.exe" "%1"
   ```

### Method 2: Installer Script (Recommended)

Use Inno Setup (see next section) which handles associations automatically.

### Method 3: Python Script

Create `register_filetype.py`:

```python
import winreg
import os

def register_filetype(exe_path):
    """Register .txt file association for Kun"""
    
    # Get full exe path
    exe_path = os.path.abspath(exe_path)
    
    try:
        # Create Kun.TextFile key
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "Kun.TextFile")
        winreg.SetValue(key, "", winreg.REG_SZ, "Kun Text File")
        
        # Create shell\open\command key
        cmd_key = winreg.CreateKey(key, r"shell\open\command")
        winreg.SetValue(cmd_key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')
        
        # Associate .txt with Kun.TextFile
        txt_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ".txt")
        winreg.SetValue(txt_key, "", winreg.REG_SZ, "Kun.TextFile")
        
        print("✅ File association registered successfully!")
        print(f"   .txt files will now open with: {exe_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Try running as Administrator")

if __name__ == "__main__":
    # Update this path to your Kun.exe location
    exe_path = r"C:\Path\To\Your\Kun.exe"
    register_filetype(exe_path)
```

**Run as Administrator:**
```powershell
# Right-click PowerShell and "Run as Administrator"
python register_filetype.py
```

---

## Creating an Installer

### Using Inno Setup (Recommended for Windows)

#### Step 1: Install Inno Setup

Download from: https://jrsoftware.org/isdl.php

#### Step 2: Create Installer Script

Create `kun_installer.iss`:

```inno
[Setup]
AppName=Kun Text Editor
AppVersion=1.0.0
AppPublisher=Your Name
AppPublisherURL=https://yourwebsite.com
DefaultDirName={autopf}\Kun
DefaultGroupName=Kun
OutputDir=installer
OutputBaseFilename=KunSetup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\Kun.exe
ChangesAssociations=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"
Name: "quicklaunchicon"; Description: "Create a Quick Launch icon"; GroupDescription: "Additional icons:"; Flags: unchecked
Name: "associatefiles"; Description: "Associate .txt files with Kun"; GroupDescription: "File associations:"

[Files]
; Include entire dist folder from PyInstaller build
Source: "dist\Kun\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Kun Text Editor"; Filename: "{app}\Kun.exe"
Name: "{group}\Uninstall Kun"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Kun Text Editor"; Filename: "{app}\Kun.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Kun Text Editor"; Filename: "{app}\Kun.exe"; Tasks: quicklaunchicon

[Registry]
; Associate .txt files
Root: HKCR; Subkey: ".txt"; ValueType: string; ValueName: ""; ValueData: "KunTextFile"; Flags: uninsdeletevalue; Tasks: associatefiles
Root: HKCR; Subkey: "KunTextFile"; ValueType: string; ValueName: ""; ValueData: "Kun Text File"; Flags: uninsdeletekey; Tasks: associatefiles
Root: HKCR; Subkey: "KunTextFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Kun.exe,0"; Tasks: associatefiles
Root: HKCR; Subkey: "KunTextFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Kun.exe"" ""%1"""; Tasks: associatefiles

[Run]
Filename: "{app}\Kun.exe"; Description: "Launch Kun Text Editor"; Flags: nowait postinstall skipifsilent
```

#### Step 3: Build Installer

1. **Open Inno Setup Compiler**
2. **File > Open** - Select `kun_installer.iss`
3. **Build > Compile** (or press F9)
4. **Find installer** in `installer/KunSetup.exe`

#### Step 4: Test Installer

1. Run `KunSetup.exe`
2. Follow installation wizard
3. Check all options (desktop icon, file associations)
4. Launch Kun after installation
5. Test by double-clicking a .txt file

---

## Distribution

### Option 1: Direct Download

**Setup:**
1. Upload `KunSetup.exe` to file hosting (Google Drive, Dropbox, etc.)
2. Create download link
3. Share link with users

**Pros:** Simple, quick
**Cons:** No automatic updates, manual distribution

### Option 2: GitHub Releases

**Setup:**
1. Create GitHub repository for Kun
2. Tag version: `git tag v1.0.0`
3. Push tag: `git push origin v1.0.0`
4. Go to **Releases** on GitHub
5. Create new release, attach `KunSetup.exe`

**Pros:** Version control, changelog, free hosting
**Cons:** Requires GitHub account

### Option 3: Microsoft Store (Advanced)

**Setup:**
1. Create Microsoft Partner Center account ($19 one-time)
2. Package as MSIX app
3. Submit for review
4. Publish to Store

**Pros:** Official distribution, automatic updates, trusted
**Cons:** Costs money, review process, packaging complexity

### What to Include in Distribution

- **Installer** - `KunSetup.exe`
- **README** - Installation and usage instructions
- **License** - If applicable
- **Changelog** - Version history
- **Screenshots** - Show off your themes!

---

## Complete Build Workflow

### Full Production Build Checklist

```powershell
# 1. Clean previous builds
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# 2. Create/update icon
# (Do this manually with image editor)

# 3. Build executable with PyInstaller
pyinstaller kun.spec

# 4. Test executable
.\dist\Kun\Kun.exe

# 5. Build installer with Inno Setup
# (Open kun_installer.iss in Inno Setup and compile)

# 6. Test installer
.\installer\KunSetup.exe

# 7. Create distribution folder
New-Item -ItemType Directory -Force -Path "release"
Copy-Item "installer\KunSetup.exe" "release\KunSetup_v1.0.0.exe"
Copy-Item "README.md" "release\README.txt"

# 8. Create ZIP for portable version
Compress-Archive -Path "dist\Kun\*" -DestinationPath "release\Kun_v1.0.0_Portable.zip"

# 9. Done! Files ready for distribution in 'release' folder
```

---

## Optimization Tips

### Reduce File Size

**PyInstaller options:**
```powershell
pyinstaller --onefile --windowed --strip --name Kun main.py
```

**UPX Compression:**
```powershell
# Download UPX from https://upx.github.io/
# Add to PyInstaller build
pyinstaller --onefile --windowed --upx-dir=C:\path\to\upx main.py
```

### Improve Startup Time

1. **Use one-folder mode** instead of one-file
2. **Exclude unnecessary packages** in .spec file
3. **Optimize imports** - Remove unused imports
4. **Lazy loading** - Import heavy modules only when needed

### Professional Touches

1. **Version Information:**
   ```python
   # Add to kun.spec
   version='1.0.0',
   description='Kun Text Editor',
   copyright='Copyright © 2025',
   ```

2. **Digital Signature** (optional):
   - Get code signing certificate
   - Sign executable: `signtool sign /f cert.pfx /p password Kun.exe`

3. **Update Checker:**
   - Add version check feature
   - Check GitHub releases API
   - Notify users of updates

---

## Troubleshooting

### "Failed to execute script"

**Cause:** Missing dependencies or files

**Fix:**
1. Check all assets are included in .spec file
2. Verify hiddenimports list
3. Run with console mode first: `console=True` in .spec
4. Check error messages

### "Icon not showing"

**Cause:** Icon path wrong or format issue

**Fix:**
1. Verify icon exists: `assets/icon.ico`
2. Check icon format (must be .ico)
3. Rebuild with correct path
4. Try absolute path in .spec

### "Application crashes on startup"

**Cause:** Path issues or missing Qt plugins

**Fix:**
1. Test Python version first: `python main.py`
2. Add Qt platform plugins:
   ```python
   datas=[
       ('path/to/PyQt6/Qt6/plugins/platforms', 'PyQt6/Qt6/plugins/platforms'),
   ]
   ```
3. Check console output for errors

### "File associations not working"

**Cause:** Registry not updated or wrong path

**Fix:**
1. Run registration script as Administrator
2. Verify exe path in registry
3. Restart Windows Explorer: `taskkill /f /im explorer.exe && start explorer.exe`
4. Check file type in file properties

### "Installer builds but won't run"

**Cause:** Inno Setup configuration error

**Fix:**
1. Check all paths in .iss file
2. Verify dist folder structure matches Source paths
3. Test without compression first
4. Check Inno Setup compiler output for warnings

### "Large file size"

**Solutions:**
1. Use one-folder mode (smaller)
2. Enable UPX compression
3. Exclude unnecessary packages
4. Use virtual environment for clean builds

---

## Advanced: Auto-Update System

### Simple Update Checker

Add to `main_window.py`:

```python
import requests
from PyQt6.QtWidgets import QMessageBox

def check_for_updates(self):
    """Check GitHub releases for updates"""
    try:
        url = "https://api.github.com/repos/yourusername/kun/releases/latest"
        response = requests.get(url, timeout=5)
        latest = response.json()
        latest_version = latest['tag_name'].replace('v', '')
        current_version = "1.0.0"
        
        if latest_version > current_version:
            reply = QMessageBox.question(
                self, 'Update Available',
                f'New version {latest_version} is available!\n\n'
                f'Would you like to download it?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                import webbrowser
                webbrowser.open(latest['html_url'])
    except:
        pass  # Silently fail if no internet
```

---

## Platform-Specific Notes

### macOS

**Build .app bundle:**
```bash
pyinstaller --windowed --name Kun --icon=assets/icon.icns main.py
```

**Create .icns icon:**
```bash
mkdir icon.iconset
sips -z 16 16 icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32 icon.png --out icon.iconset/icon_16x16@2x.png
# ... repeat for other sizes
iconutil -c icns icon.iconset
```

### Linux

**Build AppImage:**
```bash
pyinstaller --onefile --name Kun main.py
# Use appimagetool to create .AppImage
```

**Create .desktop file:**
```desktop
[Desktop Entry]
Type=Application
Name=Kun Text Editor
Exec=/path/to/Kun
Icon=/path/to/icon.png
Categories=TextEditor;Utility;
```

---

## Next Steps

1. ✅ **Build basic .exe** - Start with PyInstaller one-folder
2. ✅ **Create icon** - Design and add icon.ico
3. ✅ **Test thoroughly** - All features working
4. ✅ **Build installer** - Use Inno Setup
5. ✅ **Test installer** - Fresh install on another machine
6. ✅ **Create release** - Package for distribution
7. ✅ **Share** - GitHub, website, or store

---

## Resources

### Tools
- **PyInstaller**: https://pyinstaller.org/
- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **Icon Converters**: https://convertio.co/png-ico/
- **UPX**: https://upx.github.io/

### Documentation
- **PyQt6**: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **Python Packaging**: https://packaging.python.org/
- **Windows Installer**: https://docs.microsoft.com/windows/win32/msi

### Communities
- **r/Python**: Reddit community
- **Stack Overflow**: Q&A for issues
- **PyQt Forum**: https://www.riverbankcomputing.com/mailman/listinfo/pyqt

---

**Ready to ship your desktop app! 🚀**

*Last updated: November 2025*
