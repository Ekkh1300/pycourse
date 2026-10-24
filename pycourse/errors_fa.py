"""
ترجمه و توضیح خطاهای پایتون به فارسی.

این ماژول یک traceback خام پایتون را می‌گیرد و آن را به یک «تشخیص» خوانا
تبدیل می‌کند: چه شد؟ چرا؟ چه کنم؟

هیچ وابستگی بیرونی ندارد.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

# ─────────────────────────────────────────────────────────────
# مدل خروجی
# ─────────────────────────────────────────────────────────────


@dataclass
class Diagnosis:
    """تشخیص یک خطا، به زبان فارسی."""

    kind: str = ""  # نام خطای پایتون، مثل NameError
    message: str = ""  # پیام اصلی پایتون
    line: int | None = None  # شماره‌ی خط
    source: str = ""  # متن همان خط
    title: str = ""  # عنوان فارسی کوتاه
    what: str = ""  # چه اتفاقی افتاد؟
    why: str = ""  # چرا این اتفاق افتاد؟
    fix: list[str] = field(default_factory=list)  # چه باید کرد؟
    category: str = "error"  # error | warning | info

    def to_dict(self) -> dict:
        return asdict(self)


# ─────────────────────────────────────────────────────────────
# تجزیه‌ی traceback
# ─────────────────────────────────────────────────────────────

_FRAME_RE = re.compile(r'^\s*File "(?P<file>.+?)", line (?P<line>\d+)(?:, in (?P<func>.+))?\s*$')
_EXC_RE = re.compile(r"^(?P<kind>[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Warning|Exit|Interrupt))(?::\s*(?P<msg>.*))?$")
_CARET_RE = re.compile(r"^\s*\^\s*$")


def _clean_source(line: str) -> str:
    """خط کد را از تورفتگی traceback جدا می‌کند."""
    return line.strip()


def parse_traceback(stderr: str) -> tuple[str, str, int | None, str]:
    """خروجی stderr پایتون را تجزیه می‌کند.

    برمی‌گرداند: (نوع خطا، پیام، شماره خط، متن خط)
    """
    if not stderr:
        return "", "", None, ""

    lines = stderr.replace("\r\n", "\n").split("\n")

    # --- پیدا کردن آخرین فریم traceback ---
    last_frame_line: int | None = None
    last_func = ""
    for i, raw in enumerate(lines):
        m = _FRAME_RE.match(raw)
        if m:
            last_frame_line = int(m.group("line"))
            last_func = (m.group("func") or "").strip()
            # خط بعدی، متن کد است
            if i + 1 < len(lines):
                source_candidate = lines[i + 1]
                if not _CARET_RE.match(source_candidate) and not _FRAME_RE.match(source_candidate):
                    source = _clean_source(source_candidate)
                else:
                    source = ""
            else:
                source = ""

    # --- پیدا کردن خط آخر که نوع خطا را اعلام می‌کند ---
    kind = ""
    message = ""
    for raw in reversed(lines):
        raw = raw.strip()
        if not raw:
            continue
        m = _EXC_RE.match(raw)
        if m:
            kind = m.group("kind")
            message = (m.group("msg") or "").strip()
            break
        # اگر خط آخر یک ExceptionInfo باشد (مثل SyntaxError با جزئیات بیشتر)
        if raw.startswith(("SyntaxError:", "IndentationError:")):
            kind, _, message = raw.partition(":")
            kind = kind.strip()
            message = message.strip()
            break

    # خطای SyntaxError گاهی چند خط پیام دارد
    if kind in ("SyntaxError", "IndentationError", "TabError") and "was never closed" not in message:
        # پیام چندخطی: بخش‌های بعدی را هم بگیر
        pass

    return kind, message, last_frame_line, source


def split_suggestion(message: str) -> tuple[str, str]:
    """پایتون ۳.۱۲+ به پیام خطا «Did you mean ...?» اضافه می‌کند.

    این پیشنهاد را جدا می‌کنیم تا بتوانیم پیام اصلی را با الگوها تطبیق دهیم
    و در عین حال خودِ پیشنهاد را به یادگیرنده نشان دهیم.
    """
    for marker in (". Did you mean", ". Or did you forget"):
        if marker in message:
            head, _, tail = message.partition(marker)
            return head.strip(), (marker + tail).strip()
    return message.strip(), ""


# ─────────────────────────────────────────────────────────────
# جدول قوانین تشخیص
# ─────────────────────────────────────────────────────────────
# هر قانون: (الگوی regex روی پیام خطا، عنوان، چه شد، چرا، لیست راه‌حل)

Rule = tuple[re.Pattern, str, str, str, list[str]]

RULES: list[Rule] = [
    # ── NameError ───────────────────────────────────────────
    (
        re.compile(r"^name '(?P<name>[^']+)' is not defined$"),
        "متغیر تعریف نشده",
        "پایتون نامی را که در کدت استفاده کردی پیدا نکرد.",
        "قبل از استفاده‌ی هر متغیر باید آن را بسازی (مثلاً `x = 5`). "
        "شاید املایش را اشتباه نوشته‌ای یا اصلاً تعریفش نکرده‌ای.",
        [
            "نام را دقیقاً با تعریفی که نوشته‌ای مقایسه کن — حروف بزرگ/کوچک مهم است.",
            "قبل از این خط، متغیر را مقداردهی کن: `{name} = ...`",
            "اگر داخل تابعی هستی، یادت باشد متغیر بیرونی در آن در دسترس نیست "
            "(یا آن را `global` کن یا به‌عنوان آرگومان بگیر).",
        ],
    ),
    # ── IndentationError / TabError ─────────────────────────
    (
        re.compile(r"expected an indented block"),
        "تورفتگی جا افتاده",
        "بعد از این خط باید یک بلوک با تورفتگی بیاید، ولی نیامده.",
        "در پایتون بلوک‌ها با تورفتگی مشخص می‌شوند. هر خط داخل `if` یا حلقه "
        "باید ۴ فاصله جلوتر برود.",
        [
            "خط بعد از `if`/`for`/`while`/`def` را ۴ فاصله جلوتر ببر.",
            "می‌توانی کل فایل را انتخاب کنی و در VS Code با `Shift+Alt+F` فرمتش کنی.",
        ],
    ),
    (
        re.compile(r"unindent does not match|unexpected indent"),
        "تورفتگی ناهماهنگ",
        "تورفتگی یک خط با خط قبلش جور در نمی‌آید.",
        "همه‌ی بلوک‌ها باید دقیقاً ۴ فاصله (یا همه‌ی tab) داشته باشند. "
        "پایتون tab و space را با هم قاطی نمی‌کند.",
        [
            "همه‌ی فاصله‌ها را یکدست کن: ۴ فاصله برای هر سطح.",
            "دکمه‌ی «تبدیل indentation به tab» یا برعکس در VS Code را بزن.",
        ],
    ),
    (
        re.compile(r"inconsistent use of tabs and spaces"),
        "ترکیب tab و space",
        "در فایل، بعضی خط‌ها با tab و بعضی با space تورفتگی دارند.",
        "پایتون نمی‌داند کدام‌یک را معادل ۴ فاصله بگیرد.",
        ["کل فایل را با ۴ فاصله‌ی یکدست فرمت کن."],
    ),
    # ── SyntaxError ─────────────────────────────────────────
    (
        re.compile(r"invalid syntax"),
        "خطای نگارشی",
        "کدی که نوشتی از نظر دستور زبان پایتون معتبر نیست.",
        "رایج‌ترین علت‌ها: `=` به‌جای `==` در شرط، جا افتادن `:`، "
        "یا نوشتن `print` بدون پرانتز.",
        [
            "اگر داخل `if` یا حلقه‌ای، انتهای خط باید `:` باشد.",
            "در شرط‌ها `=` را با `==` عوض کن.",
            "پیام کامل خطا معمولاً دقیقاً می‌گوید مشکل کجاست — همان خط را نگاه کن.",
        ],
    ),
    (
        re.compile(r"was never closed"),
        "پرانتز یا کوتیشن بسته نشده",
        "یک `(` یا `[` یا `\"` باز کرده‌ای ولی نبسته‌ای.",
        "هر پرانتز باز باید یک پرانتز بسته داشته باشد.",
        ["تعداد پرانتزها را بشمار: `(` و `)` باید برابر باشند.",
         "همین کار برای `[` `]` و `{` `}` هم صدق می‌کند."],
    ),
    (
        re.compile(r"cannot assign to"),
        "تغییر نامعتبر",
        "پایتون اجازه‌ی این نوع انتساب را نمی‌دهد.",
        "مثلا نمی‌شود به یک تابع یا یک مقدار ثابت دوباره مقدار داد.",
        ["مطمئن شو متغیر یک اسم معتبر است و کلیدواژه نیست.",
         "اگر می‌خواهی در حلقه مقدار جدید بگذاری، از `+=` یا `=` استفاده کن."],
    ),
    # ── TypeError ───────────────────────────────────────────
    (
        re.compile(r"can only concatenate str \(not \"(?P<t>[^\"]+)\"\) to str"),
        "جمع رشته با عدد",
        "خواستی یک رشته را با یک عدد جمع کنی، ولی پایتون این کار را نمی‌کند.",
        "در پایتون نمی‌توان `str` و `int` را مستقیم به هم چسباند. "
        "مهم‌ترین علت: `input()` همیشه **رشته** برمی‌گرداند.",
        [
            "خروجی `input()` را تبدیل کن: `int(input(...))`",
            "یا عدد را به رشته تبدیل کن: `str(number)`",
            "برای چسباندن متن از f-string استفاده کن: `f\"مقدار: {x}\"`",
        ],
    ),
    (
        re.compile(r"unsupported operand type\(s\) for (?P<op>[^:]+): '(?P<a>[^']+)' and '(?P<b>[']+)"),
        "عملگر روی نوع نامناسب",
        "این عملگر را روی این نوع داده‌ها نمی‌شود استفاده کرد.",
        "مثلاً `+` روی `str` و `int` کار نمی‌کند. معمولاً یکی از دو طرف "
        "اشتباهی رشته شده.",
        [
            "نوع هر دو طرف را با `print(type(x))` چک کن.",
            "اگر یکی از آن‌ها از `input()` آمده، آن را تبدیل کن.",
        ],
    ),
    (
        re.compile(r"'(?P<t>[^']+)' object is not callable"),
        "تابع نیست",
        "چیزی را صدا زدی که تابع نیست.",
        "یا اسم یک متغیر را مثل تابع صدا زده‌ای، یا پرانتز را جا انداخته‌ای.",
        [
            "اگر می‌خواستی مقدار یک تابع را صدا بزنی، پرانتز بگذار: `f()`",
            "اگر متدی روی یک شیء صدا می‌زنی، مطمئن شو آن شیء از آن متد پشتیبانی می‌کند.",
        ],
    ),
    (
        re.compile(r"takes (?P<n>\d+) positional arguments? but (?P<m>\d+) (?:was|were) given"),
        "تعداد آرگومان اشتباه",
        "تابع را با تعداد آرگومان متفاوتی صدا زدی.",
        "امضای تابع مشخص می‌کند چند آرگومان می‌خواهد. "
        "آرگومان‌های پیش‌فرض هم حساب می‌شوند.",
        ["امضای تابع را در تعریفش نگاه کن: `def f(a, b=2)` یعنی ۱ تا ۲ آرگومان."],
    ),
    (
        re.compile(r"missing (?P<n>\d+) required positional argument"),
        "آرگومان کم است",
        "تابعی که صدا زدی به آرگومان بیشتری نیاز دارد.",
        "تابع‌هایی که خودت تعریف کردی هم ممکن است آرگومان اجباری داشته باشند.",
        ["تعداد و ترتیب آرگومان‌ها را با امضای تابع چک کن."],
    ),
    (
        re.compile(r"not iterable"),
        "چیزی قابل پیمایش نیست",
        "روی چیزی `for` یا حلقه گذاشتی که مجموعه نیست.",
        "فقط رشته، لیست، تاپل، دیکشنری و ست قابل پیمایش‌اند. "
        "عدد (`int`) و شیءهای دیگر این‌طور نیستند.",
        ["مطمئن شو قبلش چیزی را به لیست تبدیل کرده‌ای: `list(...)`"],
    ),
    # ── ValueError ──────────────────────────────────────────
    (
        re.compile(r"invalid literal for int\(\) with base 10: '(?P<v>[^']*)'"),
        "تبدیل به عدد نشد",
        "خواستی یک رشته را به عدد صحیح تبدیل کنی ولی محتوایش عدد نبود.",
        "تابع `int()` فقط رشته‌هایی را می‌پذیرد که خودش عدد صحیح باشند.",
        [
            "اگر ممکن است ورودی عدد نباشد، از `try/except ValueError` استفاده کن.",
            "برای اعشاری از `float()` استفاده کن نه `int()`.",
            "برای حذف فاصله‌های اضافه: `int(text.strip())`",
        ],
    ),
    (
        re.compile(r"invalid literal for int\(\)"),
        "تبدیل به عدد نشد",
        "رشته‌ای که خواستی عدد شود، عدد نبود.",
        "`int()` فقط عدد صحیح می‌پذیرد.",
        ["از `try/except ValueError` استفاده کن.",
         "اگر اعشاری است `float()` و اگر می‌خواهی صفر شود `int(float(x))`."],
    ),
    (
        re.compile(r"not enough values to unpack"),
        "تعداد مقادیر کم است",
        "خواستی یک تاپل را به چند متغیر باز کنی ولی مقدارها کم بودند.",
        "مثلا `a, b = [1]` خطا می‌دهد چون فقط یک مقدار هست.",
        ["تعداد متغیرها را با تعداد عناصر برابر کن."],
    ),
    (
        re.compile(r"too many values to unpack"),
        "تعداد مقادیر زیاد است",
        "تعداد متغیرهای سمت چپ از تعداد عناصر بیشتر است.",
        "مثلا `a, b = [1, 2, 3]` خطا می‌دهد.",
        ["از `*rest` استفاده کن: `a, b, *rest = [1, 2, 3]`"],
    ),
    # ── IndexError / KeyError ────────────────────────────────
    (
        re.compile(r"list index out of range|index out of range"),
        "اندیس خارج از محدوده",
        "به خانه‌ای از لیست اشاره کردی که وجود ندارد.",
        "اندیس لیست از صفر شروع می‌شود و آخرین اندیس `len(list) - 1` است. "
        "اندیس منفی هم یعنی از آخر شمردن.",
        [
            "برای پیمایش امن از `for` استفاده کن، نه `while i < len(x)`.",
            "اندیس منفی `-1` آخرین عضو است.",
        ],
    ),
    (
        re.compile(r"^'(?P<k>[^']+)'$"),
        "کلید پیدا نشد",
        "کلیدی که در دیکشنری خواستی وجود ندارد.",
        "دیکشنری فقط کلیدهایی را دارد که قبلاً اضافه شده‌اند.",
        [
            "از `d.get(key)` استفاده کن که به‌جای خطا `None` برمی‌گرداند.",
            "برای داده‌ی تودرتو: `d.get(\"a\", {}).get(\"b\")`",
        ],
    ),
    # ── ZeroDivisionError ───────────────────────────────────
    (
        re.compile(r"division by zero"),
        "تقسیم بر صفر",
        "مخرج صفر شده است.",
        "پایتون تقسیم بر صفر را مجاز نمی‌داند.",
        [
            "قبل از تقسیم چک کن مخرج صفر نباشد.",
            "برای کلیدهای دیکشنری، `d.get(k, 0)` بهتر از `d[k]` است.",
        ],
    ),
    # ── AttributeError ──────────────────────────────────────
    (
        re.compile(r"'(?P<t>[^']+)' object has no attribute '(?P<a>[^']+)'"),
        "متد یا صفت وجود ندارد",
        "روی این شیء، چنین صفت یا متدی تعریف نشده.",
        "هر نوع داده متدهای مخصوص خودش را دارد. مثلاً `str` متد `append` ندارد "
        "و `list` متد `upper` ندارد.",
        [
            "مطمئن شو نوع متغیرت همانی است که فکر می‌کنی: `print(type(x))`",
            "برای متن از `str.strip()` و `str.upper()` استفاده کن، "
            "برای لیست از `list.append()`.",
        ],
    ),
    # ── FileNotFoundError ───────────────────────────────────
    (
        re.compile(r"No such file or directory"),
        "فایل پیدا نشد",
        "فایلی که می‌خواستی باز کنی روی دیسک نیست.",
        "مسیر نسبی نسبت به **پوشه‌ای که فایل را اجرا می‌کنی** سنجیده می‌شود، "
        "نه پوشه‌ی ترمینال.",
        [
            "مسیر را چاپ کن: `print(Path('data.txt').absolute())`",
            "اگر فایل ممکن است نباشد: `if path.exists():`",
            "مسیر را با `pathlib` بساز: `Path(\"data\") / \"f.txt\"`",
        ],
    ),
    (
        re.compile(r"No module named '(?P<m>[^']+)'"),
        "کتابخانه نصب نیست",
        "ماژولی که `import` کردی روی این پایتون نصب نشده.",
        "بعضی کتابخانه‌ها باید جداگانه نصب شوند.",
        [
            "با `pip install <نام‌ماژول>` نصبش کن.",
            "مطمئن شو در همان محیطی نصب می‌کنی که پایتون را اجرا می‌کنی: `python -m pip install ...`",
        ],
    ),
    # ── AssertionError (از تست‌های تمرین) ───────────────────
    (
        re.compile(r"^$"),
        "تست شکست خورد",
        "کدت اجرا شد و خطا نداد، ولی نتیجه‌اش با چیزی که باید می‌بود فرق دارد.",
        "تست‌ها مقدار مشخصی انتظار دارند. پیام بالای خطا می‌گوید کدام مقدار "
        "به‌جای مقدار درست برگشته.",
        [
            "مقدار واقعی را با چاپ کردن ببین: `print(type(x), repr(x))`",
            "حواست به نوع باشد: `3` با `3.0` فرق دارد.",
            "توجه کن `None` با `0` فرق دارد.",
        ],
    ),
    # ── سایر ────────────────────────────────────────────────
    (
        re.compile(r"maximum recursion depth exceeded"),
        "بازگشت بی‌نهایت",
        "تابعی که خودش را صدا می‌زند هیچ‌وقت به شرط پایان نمی‌رسد.",
        "معمولاً شرط پایه‌ی بازگشت (base case) جا افتاده یا اشتباه است.",
        ["یک شرط پایه بگذار که بازگشت را متوقف کند."],
    ),
    (
        re.compile(r"local variable '([^']+)' referenced before assignment"),
        "متغیر قبل از مقداردهی استفاده شده",
        "متغیری که داخل تابع ساخته‌ای، قبل از اینکه مقدار بگیرد استفاده شده.",
        "اگر داخل تابع به نامی انتساب بدهی، آن نام **محلی** می‌شود — حتی اگر "
        "بیرون از تابع هم وجود داشته باشد.",
        ["قبل از استفاده، مقداردهی کن.",
         "اگر می‌خواهی متغیر بیرونی را تغییر دهی: `global x` — ولی بهتر است "
         "آن را به‌عنوان آرگومان بگیری و برگردانی."],
    ),
    (
        re.compile(r"unhashable type"),
        "کلید دیکشنری نامعتبر",
        "چیزی که به‌عنوان کلید دادی قابل استفاده نیست.",
        "کلید دیکشنری باید `hash` شودنی باشد: عدد، رشته یا تاپل. لیست و دیکشنری نه.",
        ["به‌جای لیست، از تاپل استفاده کن: `(1, 2)` به‌جای `[1, 2]`"],
    ),
    (
        re.compile(r"list object is not iterable|is not iterable"),
        "قابل پیمایش نیست",
        "روی این شیء حلقه گذاشتی ولی مجموعه نیست.",
        "عدد یا `None` قابل پیمایش نیست.",
        ["اول بررسی کن `None` نباشد، بعد تبدیل به لیست کن."],
    ),
]


# ─────────────────────────────────────────────────────────────
# تشخیص نهایی
# ─────────────────────────────────────────────────────────────


def _fallback(kind: str, message: str, line: int | None = None, source: str = "") -> Diagnosis:
    """وقتی هیچ قانون خاصی نبود."""
    pretty = {
        "NameError": "نام تعریف نشده",
        "TypeError": "نوع داده نامناسب",
        "ValueError": "مقدار نامعتبر",
        "IndexError": "اندیس خارج از محدوده",
        "KeyError": "کلید پیدا نشد",
        "AttributeError": "صفت یا متد وجود ندارد",
        "ZeroDivisionError": "تقسیم بر صفر",
        "FileNotFoundError": "فایل پیدا نشد",
        "ModuleNotFoundError": "کتابخانه نصب نیست",
        "IndentationError": "تورفتگی اشتباه",
        "TabError": "ترکیب tab و space",
        "SyntaxError": "خطای نگارشی",
        "RecursionError": "بازگشت بی‌نهایت",
        "UnboundLocalError": "متغیر قبل از مقداردهی استفاده شده",
        "AssertionError": "تست شکست خورد",
        "MemoryError": "حافظه پر شد",
        "KeyboardInterrupt": "اجرا توسط کاربر قطع شد",
        "StopIteration": "توقف بی‌دلیل",
        "SystemExit": "خروج از برنامه",
    }.get(kind, "خطای ناشناخته")

    return Diagnosis(
        kind=kind,
        message=message,
        line=line,
        source=source,
        title=pretty,
        what=f"برنامه با خطای `{kind}` متوقف شد.",
        why=message or "پیام دقیقی در دسترس نبود.",
        fix=[
            "آخرین خط پیام خطا را بخوان — معمولاً خودش مشکل را می‌گوید.",
            "شماره‌ی خطی که در traceback آمده را در کدت پیدا کن.",
        ],
    )


def diagnose(stderr: str) -> Diagnosis | None:
    """traceback خام را به تشخیص فارسی تبدیل می‌کند."""
    kind, message, line, source = parse_traceback(stderr)
    if not kind:
        return None

    base, suggestion = split_suggestion(message)

    for pattern, title, what, why, fix in RULES:
        m = pattern.search(base)
        if not m:
            continue

        # اصلاح ویژه: NameError مربوط به self
        if kind == "NameError":
            g = m.groupdict()
            if g.get("name") == "self":
                return Diagnosis(
                    kind=kind,
                    message=message,
                    line=line,
                    source=source,
                    title="`self` تعریف نشده",
                    what="داخل متد به `self` اشاره کرده‌ای ولی آن را به‌عنوان "
                    "آرگومان نگرفته‌ای.",
                    why="روش‌های کلاس همیشه `self` را به‌عنوان اولین آرگومان "
                    "می‌گیرند. اگر خودت صدا بزنی، باید دستی بدهیش.",
                    fix=[
                        "تعریف متد: `def method(self):` — نه `def method():`",
                        "موقع فراخوانی: `obj.method()` خودش self را می‌دهد.",
                    ],
                )

        # اصلاح ویژه: ModuleNotFoundError — نام ماژول را در راه‌حل بیاور
        if kind == "ModuleNotFoundError":
            module = m.groupdict().get("m", "")
            return Diagnosis(
                kind=kind,
                message=message,
                line=line,
                source=source,
                title="کتابخانه نصب نیست",
                what=f"ماژول `{module}` روی این پایتون نصب نیست.",
                why="کتابخانه‌های بیرونی جزو پایتون نیستند و باید جداگانه نصب شوند.",
                fix=[
                    f"با `pip install {module}` نصبش کن.",
                    "اگر محیط مجازی داری، اول آن را فعال کن.",
                    "برای نصب در همان پایتون: `python -m pip install " + module + "`",
                ],
            )

        return Diagnosis(
            kind=kind,
            message=message,
            line=line,
            source=source,
            title=title,
            what=what,
            why=why,
            fix=list(fix) + ([suggestion] if suggestion else []),
        )

    return _fallback(kind, message, line, source)


def diagnose_assertion(message: str, line: int | None = None, source: str = "") -> Diagnosis:
    """برای AssertionError که از تست‌های خودمان می‌آید (پیام فارسی دارند)."""
    return Diagnosis(
        kind="AssertionError",
        message=message,
        line=line,
        source=source,
        title="تست شکست خورد",
        what=message or "نتیجه‌ی کد با مقدار مورد انتظار فرق دارد.",
        why="کد اجرا شد و خطا نداد، اما خروجی‌اش اشتباه است. "
        "پیام بالا می‌گوید چه مقداری به‌جای چه مقداری برگشته.",
        fix=[
            "مقدار واقعی را ببین: `print(repr(x))` — چون `3` و `3.0` فرق دارند.",
            "تست‌های پایینِ فایل را بخوان؛ دقیقاً می‌گویند چه چیزی لازم است.",
            "اگر نوع داده اشتباه است، از `int()` یا `float()` برای تبدیل استفاده کن.",
        ],
    )
