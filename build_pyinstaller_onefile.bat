@echo off

echo Compiling to EXE
py -3.8 -m PyInstaller --onefile --noconsole --add-data="icon.ico;." --icon="%CD%\icon.ico" --name="NodeEditor" main.py

echo Moving EXE to root folder
move "%CD%\dist\NodeEditor.exe" "%CD%"

echo Cleaning up
del /f NodeEditor.spec
rmdir /S /Q build
rmdir /S /Q dist
echo Build complete!

pause