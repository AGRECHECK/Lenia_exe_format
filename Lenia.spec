# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


project_dir = Path(SPECPATH)
datas = [
    (str(project_dir / "animals.json"), "."),
    (str(project_dir / "animals3D.json"), "."),
    (str(project_dir / "animals4D.json"), "."),
    (str(project_dir / "found"), "found"),
    (str(project_dir / "resource"), "resource"),
]

a = Analysis(
    [str(project_dir / "LeniaApp.py")],
    pathex=[str(project_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "LeniaND",
        "LeniaNDK",
        "LeniaNDKC",
        "importlib.resources",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Lenia",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
)
