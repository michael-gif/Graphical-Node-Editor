@echo off

echo Compiling to EXE
py -3.8 -m PyInstaller --noconsole --add-data="icon.ico;." --icon="%CD%\icon.ico" --name="NodeEditor" main.py

echo Cleaning up
del /f NodeEditor.spec
rmdir /S /Q build
echo Build complete!
echo EXE location: ./dist/NodeEditor/NodeEditor.exe

pause