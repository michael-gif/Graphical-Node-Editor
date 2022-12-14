@echo off

echo Preparing
rmdir /S /Q "dist"
rmdir /S /Q "build"

py -3.8 "setup_onefile.py" py2exe

echo Copying icon
copy "icon.ico" ".\dist"

echo Build complete!
echo EXE location: ./dist/NodeEditor.exe

echo Building installer
powershell -ExecutionPolicy Bypass -File .\installer\build_installer.ps1
echo Build complete!