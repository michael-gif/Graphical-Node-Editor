@echo off

echo Compiling to EXE
py -3.8 -m PyInstaller --onefile --noconsole --add-data="icon.ico;." --icon="%CD%\icon.ico" main.py

echo Moving EXE to root folder
move "%CD%\dist\main.exe" "%CD%"
ren main.exe "NodeEditor.exe"

echo Cleaning up
del /f main.spec
rem rmdir /S /Q build
rem rmdir /S /Q dist

pause