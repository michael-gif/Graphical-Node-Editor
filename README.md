# Pygame_NodeEditor
Node editor using PyGame and Tkinter

# Usage
Download latest release  
Run `Node Editor.exe`

# Toolbar
| Button | Description |
| ------ | ----------- |
| ![Exit](https://github.com/michael-gif/Pygame_NodeEditor/blob/main/docs/exit.png) | Exits the application |
| ![New Node](https://github.com/michael-gif/Pygame_NodeEditor/blob/main/docs/new_node.png) | Opens the create node dialog |
| ![Edit Node](https://github.com/michael-gif/Pygame_NodeEditor/blob/main/docs/edit_node.png) | Opens the edit node dialog |
| ![Import](https://github.com/michael-gif/Pygame_NodeEditor/blob/main/docs/import.png) | Allows you to import a file |
| ![Export](https://github.com/michael-gif/Pygame_NodeEditor/blob/main/docs/export.png) | Opents the export dialog |

# Export node tree to a file
![Export settings](https://github.com/michael-gif/Pygame_NodeEditor/blob/main/docs/export_dialog.png)  
- Click the button with the three dots to select a save location
- Select the export format (only JSON is currently supported)
- Click on `Export settings` to change the export settings
- `Export` will export the file to the specified format with the configured export settin

# Export settings
![Export settings](https://github.com/michael-gif/Pygame_NodeEditor/blob/main/docs/export_settings.png)  
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
- Install PyAudio for python 3.8  
  `python.exe -m pip install PyAudio`
- Go to the folder of the respository
- Run `build.bat`