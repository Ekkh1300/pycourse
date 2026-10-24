"""
ساخت بسته‌ی نهایی برای انتشار.

اجرا:  python build_release.py

خروجی در پوشه‌ی release\ :
  • PythonTerminal.exe        — برنامه‌ی کامل برای ویندوز
  • PythonTerminal.html       — نسخه‌ی وب تک‌فایلی
  • راهنمای فارسی            — چطور اجرا و منتشر کنم
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

README = """# ترمینال پایتون — محیط آموزش مقدماتی

## ۱) نسخه‌ی ویندوز (پیشنهادی)

فایل `PythonTerminal.exe` را دابل‌کلیک کن. مرورگر خودکار باز می‌شود.
هیچ نصبی لازم نیست — پایتون داخل خودِ فایل exe هست.

- اگر پورت ۸۷۶۵ اشغال بود، خودکار پورت بعدی را می‌گیرد.
- برای بستن برنامه، پنجره‌ی ترمینال را ببند. (اگر بسته نشد، در Task
  Manager پروسه‌ی `PythonTerminal` را ببند.)
- پیشرفت و کدهایت در پوشه‌ی کنار exe ذخیره می‌شود (`.progress.json`).

## ۲) نسخه‌ی وب

دو نسخه هست:

### `PythonTerminal.html` — کوچک و آنلاین (۳۰۰ کیلوبایت)

- **باز کردن محلی:** روی فایل دابل‌کلیک کن.
- **انتشار:** فایل را روی هر هاست استاتیک بگذار:
  GitHub Pages / Netlify / Cloudflare Pages / Vercel / هر سرور وب.
- برای «اجرای کد پایتون» اینترنت لازم است (Pyodide از CDN بارگذاری
  می‌شود — حدود ۱۰ مگابایت، فقط بارِ اول). بقیه‌ی برنامه (جزوه،
  تمرین، آزمون، تشخیص خطای فارسی) کاملاً آفلاین کار می‌کند.

### `PythonTerminal-offline.html` — کاملاً آفلاین (۱۷ مگابایت)

- کل موتور پایتون (Pyodide) داخل خودِ فایل است.
- **هیچ اینترنتی لازم نیست** — حتی با قطع کامل شبکه.
- روی فلش، روی CD، یا با ایمیل کردنش هرجا کار می‌کند.
- دابل‌کلیک کن و باز شود. حتی از روی `file://` کار می‌کند.

## ۳) باز کردن روی گوشی

رابط کامل ریسپانسیو است و روی آیفون/اندروید/تبلت تست شده:
ناوبری پایین صفحه (فهرست / کد / جزوه)، کشوی کناری، هدف‌های لمسی ≥۴۴ پیکسل.

### راه «الف» — سرور محلی (بدون هیچ انتقال فایلی)

۱. `PythonTerminal.exe` را روی کامپیوتر اجرا کن (یا `python app.py`).
۲. در پنجره‌ی مشکی، آدرس گوشی را ببین:  `http://192.168.x.x:8765/`
   یا داخل برنامه، دکمه‌ی «📱 گوشی» در نوار بالا را بزن.
۳. گوشی باید روی **همان وای‌فای** کامپیوتر باشد.
۴. همان آدرس را در مرورگر گوشی تایپ کن.

نکته: اگر باز نشد، فایروال ویندوز را بررسی کن (پاپ‌آپ اولین اجرا را
«اجازه» بزن) و مطمئن شو گوشی روی داده‌ی موبایل نیست.

### راه «ب» — انتقال خودِ فایل

**اندروید** (ساده‌ترین حالت):
- `PythonTerminal.html` را با WhatsApp/Telegram/ایمیل به خودت بفرست،
  ذخیره کن، بعد در Chrome باز کن.
- یا با کابل USB در پوشه‌ی `Download` کپی کن و باز کن.

**آیفون**:
- فایل را در اپلیکیشن «Files» ذخیره کن.
- روی فایل ضربه بزن → Share → **Open in Safari**.

### راه «ج» — انتشار آنلاین (برای هر دو گوشی، بهترین راه)

فایل `PythonTerminal.html` را در **Netlify Drop** (app.netlify.com/drop)
بکش و رها کن. بعد از ۳۰ ثانیه یک آدرس مثل
`https://چیزی-صادفانه.netlify.app` می‌گیری که در هر مرورگری باز می‌شود.
برای انتشار دائمی‌تر، GitHub Pages هم همین‌طور کار می‌کند.

### راه «د» — فلش/بلوتوث

`PythonTerminal.zip` (۱۶ مگابایت) را به گوشی بفرست، استخراج کن و
`PythonTerminal-offline.html` داخلش را باز کن. این نسخه هیچ اینترنتی
نمی‌خواهد.

> نسخه‌ی آنلاین برای «اجرای کد پایتون» به اینترنت نیاز دارد (بار اول حدود
> ۱۰ مگابایت). بقیه‌ی برنامه آفلاین است.

## ۴) اگر خواستی خودت توسعه بدهی

```powershell
python app.py                 # اجرای نسخه‌ی محلی با سرور
python build_exe.py            # ساخت exe
python build_html.py           # ساخت html
python build_html.py --download   # (فقط یک‌بار) دانلود Pyodide برای نسخه‌ی آفلاین
python build_release.py        # ساخت همه + بسته‌ی نهایی
```

تست‌ها:

```powershell
python tests\\_test_diag.py       # تشخیص خطاها
python tests\\_test_solutions.py  # راه‌حل‌ها
python tests\\_test_api.py        # APIها (سرور باید بالا باشد)
python tests\\_test_ui.py         # رابط کاربری
python tests\\_test_static.py     # نسخه‌ی HTML آنلاین
python tests\\_test_offline.py    # نسخه‌ی HTML آفلاین (اینترنت قطع می‌شود)
python tests\\_test_mobile.py     # موبایل: سرور + هر دو فایل HTML
```
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
