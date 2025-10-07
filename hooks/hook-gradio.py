from PyInstaller.utils.hooks import collect_all

# This is the most robust method to package complex libraries like Gradio.
# The `collect_all` function recursively finds and includes:
# - All Python source code (.py)
# - All data files (like .json, .js, .css, etc.)
# - All binary files (.dll, .so, etc.)
# for the specified packages.

# By collecting all data for both 'gradio' and 'gradio_client', we ensure
# that no files are missed, resolving the persistent FileNotFoundError issues.
datas, binaries, hiddenimports = collect_all('gradio')
datas_client, binaries_client, hiddenimports_client = collect_all('gradio_client')

datas.extend(datas_client)
binaries.extend(binaries_client)
hiddenimports.extend(hiddenimports_client)