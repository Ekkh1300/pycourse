"""
ساخت فایل exe با PyInstaller.

اجرا:  python build_exe.py

خروجی:  dist\\PythonTerminal\\PythonTerminal.exe
(یک پوشه‌ی کامل که می‌توانی زیپ کنی و هرجا بفرستی)
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

# کنسول ویندوز پیش‌فرض cp1252 است و متن فارسی را خراب می‌کند
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parent
NAME = "PythonTerminal"


def main() -> int:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller نصب نیست. در حال نصب…")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    for folder in ("build", "dist"):
        shutil.rmtree(ROOT / folder, ignore_errors=True)

    data_dirs = ["web", "lessons", "exercises", "solutions", "projects", "practice"]

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",  # بدون پنجره‌ی کنسول
        "--name", NAME,
        "--onefile",  # یک فایل exe
        "--add-data", f"{ROOT / 'web'}{';'}web",
        "--add-data", f"{ROOT / 'lessons'}{';'}lessons",
        "--add-data", f"{ROOT / 'exercises'}{';'}exercises",
        "--add-data", f"{ROOT / 'solutions'}{';'}solutions",
        "--add-data", f"{ROOT / 'projects'}{';'}projects",
        "--add-data", f"{ROOT / 'practice'}{';'}practice",
        "--hidden-import", "pycourse.paths",
        "--exclude-module", "tkinter",
        "--exclude-module", "playwright",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        str(ROOT / "app.py"),
    ]

    print("در حال ساخت exe… (ممکن است ۱ تا ۳ دقیقه طول بکشد)")
    result = subprocess.run(command, cwd=str(ROOT))
    if result.returncode != 0:
        print("❌ ساخت ناموفق بود")
        return result.returncode

    exe = ROOT / "dist" / f"{NAME}.exe"
    if not exe.exists():
        print("❌ فایل exe ساخته نشد")
        return 1

    size_mb = exe.stat().st_size / (1024 * 1024)
    print("=" * 60)
    print(f"✅ ساخته شد: {exe}")
    print(f"   حجم: {size_mb:.1f} مگابایت")
    print()
    print("   این فایل را هرجا کپی کن و دابل‌کلیک کن.")
    print("   مرورگر خودکار باز می‌شود. برای بستن، پنجره‌ی مرورگر را ببند")
    print("   و از Task Manager پروسه را ببند، یا با PYCOURSE_NO_BROWSER=1 اجرا کن.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
