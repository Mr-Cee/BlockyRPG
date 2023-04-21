# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [('assets', 'assets')]

a = Analysis(
    ['main.py'],
    pathex=['C:\\users\\josh.christie\\pycharmProjects\\blockyRPG\\', 'C:\\Users\\josh.christie\\PycharmProjects\\BlockyRPG\\venv\\Lib\\site-packages\\',
	'C:\\Users\\josh.christie\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\'],
    binaries=[],
    datas=added_files,
    hiddenimports=['pyautogui', 'pygame', 'pygame.base', 'base.cp39-win-amd64.pyd', 'base.pyi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BlockyRPG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BlockyRPG',
)
