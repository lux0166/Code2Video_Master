@echo off
echo Building the Code2Video executable...

rem Set the Python path to include the 'src' directory
set PYTHONPATH=src

rem Run PyInstaller with the correct options
pyinstaller --onefile --windowed --name "Code2Video" src/gui.py

rem Clean up the .spec file
del Code2Video.spec

echo Build complete! The executable is located in the 'dist' directory.
