from PyInstaller.utils.hooks import collect_data_files

# This hook script tells PyInstaller to find and bundle all data files
# associated with the 'gradio_client' package. This is the standard
# and most reliable way to include package data like .json files.
datas = collect_data_files('gradio_client')