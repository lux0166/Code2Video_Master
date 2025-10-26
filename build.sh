#!/bin/bash
echo "Building the Code2Video executable..."

# Set the Python path to include the 'src' directory
export PYTHONPATH=src

# Run PyInstaller with the correct options
pyinstaller --onefile --windowed --name "Code2Video" src/gui.py

# Clean up the .spec file
rm -f Code2Video.spec

echo "Build complete! The executable is located in the 'dist' directory."
