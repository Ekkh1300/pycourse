"""
مسیرهای برنامه.

وقتی برنامه با PyInstaller بسته‌بندی می‌شود، داده‌ها داخل پوشه‌ی موقت
`_MEIPASS` باز می‌شوند (فقط‌خواندنی) و فایل‌های قابل‌نوشتن باید کنار
خودِ exe بنشینند. این ماژول هر دو حالت را یکدست می‌کند.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

FROZEN = bool(getattr(sys, "frozen", False))


def app_root() -> Path:
    """پوشه‌ی داده‌های فقط‌خواندنی (درس‌ها، تمرین‌ها، رابط کاربری)."""
    if FROZEN:
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass)
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def user_dir() -> Path:
    """پوشه‌ی قابل‌نوشتن (پیشرفت، تنظیمات)."""
    if FROZEN:
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def run_dir() -> Path:
    """پوشه‌ی موقت اجرای کد کاربر."""
    if FROZEN:
        return Path(tempfile.gettempdir()) / "python-terminal-runs"
    return app_root() / ".run"


def progress_file() -> Path:
    return user_dir() / ".progress.json"


def web_dir() -> Path:
    return app_root() / "web"
