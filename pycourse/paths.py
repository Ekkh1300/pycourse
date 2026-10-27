"""
Application paths.

When the program is bundled with PyInstaller, data is loaded from the
temp folder `_MEIPASS` (read-only) and writable files should be placed
next to the exe. This module handles both cases consistently.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

FROZEN = bool(getattr(sys, "frozen", False))

# Application language: "fa" (Persian/RTL) or "en" (English/LTR)
# Override at runtime with: pycourse.paths.set_language("en")
LANGUAGE: str = "fa"


def set_language(lang: str) -> None:
    """Change the application language ('fa' or 'en')."""
    global LANGUAGE
    if lang in ("fa", "en"):
        LANGUAGE = lang


def get_language() -> str:
    return LANGUAGE


def app_root() -> Path:
    """Return the application root directory."""
    if FROZEN:
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass)
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def user_dir() -> Path:
    """Return the user directory."""
    if FROZEN:
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def run_dir() -> Path:
    """Return the temporary run directory."""
    if FROZEN:
        return Path(tempfile.gettempdir()) / "python-terminal-runs"
    return app_root() / ".run"


def progress_file() -> Path:
    return user_dir() / ".progress.json"


def web_dir() -> Path:
    return app_root() / "web"