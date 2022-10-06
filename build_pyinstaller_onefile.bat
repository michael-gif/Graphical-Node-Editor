@echo off

echo Preparing
rmdir /S /Q "dist"
rmdir /S /Q "build"

echo Compiling to EXE
py -3.8 -m PyInstaller --onefile --noconsole --add-data="icon.ico;." --icon="%CD%\icon.ico" --name="NodeEditor" main.py

echo Cleaning up
del /f "NodeEditor.spec"
rmdir /S /Q "build"
echo Build complete!
echo EXE location: ./dist/NodeEditor.exe

echo Building installer
powershell -ExecutionPolicy Bypass -File .\installer\build_installer.ps1
echo Build complete!