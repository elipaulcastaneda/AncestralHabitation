# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Ancestral Habitation
This ensures all modules and dependencies are properly bundled
"""

block_cipher = None

a = Analysis(
    ['game.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'game_engine',
        'game_engine.game_state',
        'game_engine.ui',
        'game_engine.graphics',
        'game_engine.technologies',
        'game_engine.geography',
        'game_engine.governance',
        'rich',
        'rich.console',
        'rich.panel',
        'rich.table',
        'rich.text',
        'rich.align',
        'rich.progress',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AncestralHabitation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
