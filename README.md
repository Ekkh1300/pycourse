<div align="center">

# 🐍 Python Terminal — Interactive Beginner Python Course

**A local, browser-based Python learning environment with an editor, lessons, exercises, and instant code feedback.**

[![Latest Release](https://img.shields.io/github/v/release/Ekkh1300/pycourse?label=latest%20release)](https://github.com/Ekkh1300/pycourse/releases/latest)
[![License](https://img.shields.io/github/license/Ekkh1300/pycourse)](LICENSE)

**[Download the latest release](https://github.com/Ekkh1300/pycourse/releases/latest) · [فارسی](#راهنمای-فارسی)**

</div>

Python Terminal is a beginner-friendly course app. Read a lesson, write code, run it, and check your work in one place. Python errors can be explained in Persian or English. The app runs locally and requires no third-party Python packages.

## Language

The interface defaults to **English (LTR)**. Use **🌐 Fa ⇄ En** in the title bar to switch to **Persian (RTL)** and back. The language preference is saved locally.

Error diagnoses, exercise hints, lessons, exercises, projects, and quiz questions are available in **both English and Persian**. The language toggle switches all course content.

## Download and run

Download an asset from [GitHub Releases](https://github.com/Ekkh1300/pycourse/releases/latest):

| Download | Internet | Details |
|---|---:|---|
| `PythonTerminal.exe` | No | Windows app; double-click to launch. |
| `PythonTerminal-offline.html` | No | Self-contained HTML app with Pyodide included; can be opened locally. |
| `PythonTerminal.html` | For Python execution | Lightweight online HTML build; Pyodide is loaded from a CDN. |
| `PythonTerminal-v1.2.0.zip` | Depends on selected app | ZIP package of the release assets. |

### Use on a phone or tablet

- **On the same Wi-Fi:** run `PythonTerminal.exe` or `python app.py` on your computer, then open the displayed network address on your phone.
- **From a file:** transfer `PythonTerminal-offline.html` to the device and open it in a browser. On iPhone, use Files → Share → Open in Safari.

### Host the HTML build

Upload `PythonTerminal.html` to GitHub Pages, Netlify, Cloudflare Pages, Vercel, or another static host. No backend is needed. Running Python uses Pyodide from a CDN (about 10 MB on first use); the offline build bundles Pyodide.

## Features

- **8 lessons, 7 exercises, 7 solutions, 3 projects, and a 13-question quiz**
- Browser editor with Python syntax highlighting, line numbers, indentation, and autosaved exercise code
- Run code and check each exercise assertion independently
- Step-by-step exercise hints and solutions unlocked after three attempts
- Beginner-friendly Python error diagnosis in Persian and English
- Search across course documents and a command palette (`Ctrl+K`)
- Responsive desktop, phone, and tablet layouts
- Amber and CRT themes, adjustable font size, progress tracking, and exercise timer
- Online and fully offline HTML builds

## Run from source

Requirements: Python 3.10 or newer. The application server uses only the Python standard library. The UI tests additionally require Playwright.

```bash
git clone https://github.com/Ekkh1300/pycourse.git
cd pycourse
python app.py
```

Open the URL printed by the app (normally <http://127.0.0.1:8765/>). If that port is busy, the app selects another available port.

### Build the release assets

```powershell
python build_exe.py
python build_html.py
python build_html.py --download  # one-time Pyodide download for the offline build
python build_html.py
python build_release.py
```

Build outputs and the downloaded `vendor/` Pyodide files are not committed. Downloaded and generated release assets are published on the [Releases page](https://github.com/Ekkh1300/pycourse/releases).

## Project layout

```text
app.py                 Local HTTP server
build_exe.py           Build the Windows executable
build_html.py          Build online and offline single-file HTML apps
build_release.py       Assemble release assets
pycourse/              Course and application modules
  content.py           Read lessons and exercises
  runner.py            Run user code with a timeout
  tester.py            Run assertions independently
  errors_fa.py         Persian Python error diagnoses
  errors_en.py         English Python error diagnoses
  hints.py             Persian exercise hints
  hints_en.py          English exercise hints
  paths.py             App paths and language preference
web/                   Browser UI and static API
lessons/               8 lessons (en/ and fa/)
exercises/             7 exercises with tests (en/ and fa/)
solutions/             Exercise solutions
projects/              3 projects (en/ and fa/)
practice/quiz.py       Command-line quiz
tests/                 Automated test suites
```

## Tests

```powershell
python tests\_test_diag.py
python tests\_test_solutions.py
python tests\_test_api.py
python tests\_test_ui.py
python tests\_test_static.py
python tests\_test_offline.py
python tests\_test_mobile.py
python tests\_test_recovery.py
```

UI tests require Playwright:

```powershell
pip install playwright
playwright install chromium
```

## Contributing

Issues and pull requests are welcome. Please include steps to reproduce bugs and run the relevant tests before submitting changes.

## فارسی

### معرفی

**ترمینال پایتون** یک محیط محلی و مرورگرمحور برای یادگیری مقدماتی پایتون است. درس بخوانید، کد بنویسید و اجرا کنید و تمرین‌ها را بررسی کنید. تشخیص خطاها و راهنماهای تمرین به فارسی و انگلیسی در دسترس‌اند.

### زبان برنامه

زبان پیش‌فرض رابط **انگلیسی (چپ‌به‌راست)** است. با دکمه‌ی **🌐 Fa ⇄ En** در نوار عنوان، زبان رابط را به **فارسی (راست‌به‌چپ)** تغییر دهید. انتخاب زبان ذخیره می‌شود.

**توجه:** متن درس‌ها، تمرین‌ها، پروژه‌ها و آزمون به **هر دو زبان فارسی و انگلیسی** موجود است و با دکمه‌ی زبان قابل تغییر است.

### دریافت و اجرا

از [صفحه‌ی انتشارها](https://github.com/Ekkh1300/pycourse/releases/latest) یکی از فایل‌ها را دریافت کنید:

- `PythonTerminal.exe` — برنامه‌ی ویندوز، بدون نیاز به نصب پایتون.
- `PythonTerminal-offline.html` — نسخه‌ی HTML کاملاً آفلاین.
- `PythonTerminal.html` — نسخه‌ی سبک آنلاین؛ برای اجرای پایتون به اینترنت نیاز دارد.
- `PythonTerminal-v1.2.0.zip` — بسته‌ی ZIP فایل‌های انتشار.

برای اجرا از سورس، پایتون ۳.۱۰ یا جدیدتر لازم است:

```bash
git clone https://github.com/Ekkh1300/pycourse.git
cd pycourse
python app.py
```

سپس نشانی‌ای را که برنامه چاپ می‌کند در مرورگر باز کنید. برای ساخت فایل‌ها و اجرای تست‌ها، دستورهای بخش‌های انگلیسی بالا را ببینید.

### امکانات

- ۸ درس، ۷ تمرین، ۷ راه‌حل، ۳ پروژه و آزمون ۱۳ سؤالی
- ویرایشگر کد، اجرای پایتون و بررسی جداگانه‌ی تست‌ها
- تشخیص خطا و راهنمای تمرین به فارسی و انگلیسی
- محتوای کامل درس‌ها، تمرین‌ها، پروژه‌ها و آزمون به فارسی و انگلیسی
- ذخیره‌ی پیشرفت و کد تمرین‌ها
- چیدمان واکنش‌گرا برای رایانه، تبلت و گوشی
- نسخه‌ی HTML آنلاین و آفلاین

---

## License

See [LICENSE](LICENSE).
