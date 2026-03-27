import os
import shutil
import sys
from pathlib import Path


APP_NAME = "Lenia"


def _bundle_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parent


def _runtime_root() -> Path:
    if getattr(sys, "frozen", False):
        local_appdata = os.environ.get("LOCALAPPDATA")
        if local_appdata:
            return Path(local_appdata) / APP_NAME
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


BUNDLE_ROOT = _bundle_root()
RUNTIME_ROOT = _runtime_root()


def asset_path(*parts: str) -> str:
    return str(BUNDLE_ROOT.joinpath(*parts))


def runtime_path(*parts: str) -> str:
    return str(RUNTIME_ROOT.joinpath(*parts))


def ensure_runtime_file(*parts: str) -> str:
    source = BUNDLE_ROOT.joinpath(*parts)
    target = RUNTIME_ROOT.joinpath(*parts)
    target.parent.mkdir(parents=True, exist_ok=True)

    if source == target:
        return str(target)

    if target.exists():
        return str(target)

    if source.exists():
        shutil.copy2(source, target)

    return str(target)
