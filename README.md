# Graphical Node Editor
Node editor using PyGame and Tkinter  
![Example](https://github.com/michael-gif/Graphical-Node-Editor/blob/main/docs/example.png)

# Usage
Download latest release https://github.com/michael-gif/Graphical-Node-Editor/releases  
Run `NodeEditor.exe`

# Requirements
- Python 3.8
- Pygame 1.9.6
- Tkinter (comes with Python)

# Toolbar
| Button | Description |
| ------ | ----------- |
| ![Exit](https://github.com/michael-gif/Graphical-Node-Editor/blob/main/docs/exit.png) | Exits the application |
| ![New Node](https://github.com/michael-gif/Graphical-Node-Editor/blob/main/docs/new_node.png) | Opens the create node dialog |
| ![Edit Node](https://github.com/michael-gif/Graphical-Node-Editor/blob/main/docs/edit_node.png) | Opens the edit node dialog |
| ![Import](https://github.com/michael-gif/Graphical-Node-Editor/blob/main/docs/import.png) | Allows you to import a file |
| ![Export](https://github.com/michael-gif/Graphical-Node-Editor/blob/main/docs/export.png) | Opents the export dialog |

# Export node tree to a file
![Export settings](https://github.com/michael-gif/Graphical-Node-Editor/blob/main/docs/export_dialog.png)  
- Click the button with the three dots to select a save location
- Select the export format (only JSON is currently supported)
- Click on `Export settings` to change the export settings
- `Export` will export the file to the specified format with the configured export settings

# Export settings
![Export settings](https://github.com/michael-gif/Graphical-Node-Editor/blob/main/docs/export_settings.png)  
- Check or uncheck each of the attributes to include or exlude them in the exported file
- Change the name of an attribute to change its name in the exported file

# Building from source code
- Download this repository
- Install Python 3.8 if you don't have it already 
  https://www.python.org/downloads/release/python-380/
- Navigate to the Python38 folder where python.exe is located  
  On windows: `C:\..\AppData\Local\Programs\Python\Python38\`
- Install Pygame 1.9.6 for Python 3.8  
  `python.exe -m pip install -Iv pygame==1.9.6`
- Go to the folder of the respository
### Compiling to exe
*It doesn't matter whether you use the PyInstaller scripts or the py2exe scripts, just pick one*
- Standard compilation
  - PyInstaller: `build_pyinstaller.bat`  
  - py2exe: `build_py2exe.bat`
- Minimal file compilation
  - PyInstaller: `build_pyinstaller_onefile.bat`
  - py2exe: `build_py2exe_onefile.bat`

# Building the installer
The installer is automatically built for you when you build `NodeEditor.exe`, and is located in the `installer` directory as `nodeeditor_setup.exe`  
However if you want to build the installer youself:  
- Download InnoSetup https://jrsoftware.org/isdl.php  
  (Direct link to exe: https://jrsoftware.org/download.php/is.exe?site=1)
- Install InnoSetup
- Navigate to the `installer` directory in this repo
### Method 1
- Run `build_installer.ps1` from PowerShell
- You will end up with `nodeeditor_setup.exe` in the `installer` folder
### Method 2
- Open `installer_script.iss` in Inno Setup Compiler, making sure the name of the script corresponds to the build script you used to generate the app exe.  
- Go to `Build > Compile` and wait for installer to compile
- You will end up with `nodeeditor_setup.exe` in the `installer` folder
