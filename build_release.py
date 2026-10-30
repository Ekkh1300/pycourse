"""
ساخت بسته‌ی نهایی برای انتشار.

اجرا:  python build_release.py

خروجی در پوشه‌ی release\ :
  • PythonTerminal.exe        — برنامه‌ی کامل برای ویندوز
  • PythonTerminal.html       — نسخه‌ی وب تک‌فایلی
  • README.txt                — setup and usage guide
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
RELEASE = ROOT / "release"

README = """# Python Terminal — Beginner Python Course

Python Terminal is a browser-based learning app with lessons, exercises, a code editor, and Python execution.
The interface defaults to English. Use the 🌐 Fa ⇄ En button to switch to Persian (RTL).
Error diagnosis, hints, lessons, exercises, projects, and quiz content are available in both English and Persian. Switch the language at any time — your choice is remembered.

## Windows app

Double-click `PythonTerminal.exe`; your browser opens automatically. No separate Python installation is required.

- If port 8765 is busy, the app selects another port.
- Progress and saved code are stored beside the executable in `.progress.json`.
- To close the app, close its console window, or end `PythonTerminal` in Task Manager.

## Web builds

### `PythonTerminal.html` — lightweight online build

Open the file or host it on GitHub Pages, Netlify, Cloudflare Pages, Vercel, or another static host. Running Python requires internet access to load Pyodide from a CDN (about 10 MB on first use).

### `PythonTerminal-offline.html` — fully offline build

Pyodide is bundled in the HTML file. Open it in a browser, including from `file://`; no internet connection is required.

## Use on a phone or tablet

- **Same Wi-Fi:** run `PythonTerminal.exe` or `python app.py` on your computer and open the displayed network URL on your mobile device.
- **Transfer a file:** send `PythonTerminal-offline.html` to your device and open it in a browser. On iPhone, use Files → Share → Open in Safari.
- **Host online:** upload `PythonTerminal.html` to a static hosting provider.

## Build from source

```powershell
python app.py
python build_exe.py
python build_html.py
python build_html.py --download  # one-time Pyodide download for offline build
python build_release.py
```

Requires Python 3.10 or newer. The app server uses only the Python standard library. UI tests require Playwright.

## Tests

```powershell
python tests\\_test_diag.py
python tests\\_test_solutions.py
python tests\\_test_api.py
python tests\\_test_ui.py
python tests\\_test_static.py
python tests\\_test_offline.py
python tests\\_test_mobile.py
python tests\\_test_recovery.py
```

For the complete documentation, visit https://github.com/Ekkh1300/pycourse.
"""


def main() -> int:
    print("۱) ساخت exe…")
    result = subprocess.run([sys.executable, str(ROOT / "build_exe.py")], cwd=str(ROOT))
    if result.returncode != 0:
        print("❌ ساخت exe ناموفق بود")
        return 1

    print("\n۲) ساخت html…")
    result = subprocess.run([sys.executable, str(ROOT / "build_html.py")], cwd=str(ROOT))
    if result.returncode != 0:
        print("❌ ساخت html ناموفق بود")
        return 1

    print("\n۳) جمع‌بندی بسته…")
    if RELEASE.exists():
        shutil.rmtree(RELEASE)
    RELEASE.mkdir(parents=True)

    exe = DIST / "PythonTerminal.exe"
    html_online = DIST / "PythonTerminal.html"
    html_offline = DIST / "PythonTerminal-offline.html"

    if exe.exists():
        shutil.copy2(exe, RELEASE / exe.name)
    if html_online.exists():
        shutil.copy2(html_online, RELEASE / html_online.name)
    if html_offline.exists():
        shutil.copy2(html_offline, RELEASE / html_offline.name)
    (RELEASE / "راهنما.txt").write_text(README, encoding="utf-8-sig")

    # یک zip هم بساز برای راحتی — اول جای دیگری می‌سازیم (تا خودش داخل
    # خودش زیپ نشود) و بعد داخل release/ جابه‌جا می‌کنیم.
    # فایل‌های مخفی (مثل .progress.json که موقع اجرا ساخته می‌شود) حذف.
    package_items = [
        item for item in sorted(RELEASE.iterdir()) if not item.name.startswith(".")
    ]
    archive = ROOT / "PythonTerminal.zip"
    archive.unlink(missing_ok=True)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in package_items:
            zf.write(item, arcname=item.name)
    shutil.move(str(archive), str(RELEASE / archive.name))

    print("=" * 62)
    print("✅ بسته‌ی نهایی آماده است:")
    print()
    for item in package_items + [RELEASE / archive.name]:
        size = item.stat().st_size / (1024 * 1024)
        print(f"   {item.name:<28} {size:>8.2f} MB")
    print()
    print(f"   پوشه: {RELEASE}")
    print("=" * 62)
    return 0


if __name__ == "__main__":
    sys.exit(main())
