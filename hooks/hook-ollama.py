from PyInstaller.utils.hooks import collect_submodules, collect_data_files
hiddenimports = collect_submodules('ollama')
datas = collect_data_files('ollama', subdir='data')