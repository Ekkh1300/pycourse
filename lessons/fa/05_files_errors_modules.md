# درس ۵ — فایل، مدیریت خطا و ماژول

> هدف: برنامه‌ات از حافظه‌ی موقت خارج شود (فایل)، در برابر ورودی‌های بد زنده بماند
> (مدیریت خطا)، و از کدهای آماده استفاده کند (ماژول).

---

## ۱. کار با فایل

### الگوی استاندارد: `with`

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

print(content)
```

`with` یعنی: فایل را باز کن، بدنه را اجرا کن، **حتی اگر خطا داد** فایل را ببند.
همیشه از `with` استفاده کن.

### حالت‌های باز کردن

| حالت | معنی | نکته |
|---|---|---|
| `"r"` | خواندن (پیش‌فرض) | فایل باید وجود داشته باشد |
| `"w"` | نوشتن | ⚠️ محتوای قبلی **پاک می‌شود** |
| `"a"` | اضافه کردن به آخر | محتوای قبلی می‌ماند |
| `"x"` | ساختن جدید | اگر وجود داشته باشد خطا می‌دهد |

### خواندن خط‌به‌خط

```python
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

⚠️ هر خطی که از فایل می‌خوانی **در انتها `\n` دارد**. برای حذفش از `.strip()`
استفاده کن.

### نوشتن در فایل

```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("خط اول\n")
    f.write("خط دوم\n")

# چند خط یکجا:
lines = ["a\n", "b\n"]
with open("out.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
```

### خواندن همه به‌صورت لیست

```python
with open("data.txt", encoding="utf-8") as f:
    lines = f.readlines()      # لیستی از خطوط
```

### کار با مسیرها — `pathlib` (روش حرفه‌ای)

```python
from pathlib import Path

p = Path("data") / "sub" / "file.txt"
p.parent.mkdir(parents=True, exist_ok=True)

if p.exists():
    text = p.read_text(encoding="utf-8")
    p.write_text("محتوا", encoding="utf-8")

for item in Path(".").glob("*.txt"):
    print(item)
```

⚠️ همیشه `encoding="utf-8"` را بنویس. بدون آن، روی ویندوز فایل‌های فارسی خراب می‌شوند.

---

## ۲. مدیریت خطا

### ۲.۱ `try / except`

```python
try:
    number = int(input("عدد: "))
except ValueError:
    print("این عدد نبود!")
    number = 0
```

### ۲.۲ چند خطا

```python
try:
    value = int(user_input)
except ValueError:
    print("عدد نیست")
except KeyError:
    print("کلید پیدا نشد")
except Exception as e:
    print(f"خطای ناشناخته: {e}")
```

⚠️ **قانون طلایی:** `except Exception` را فقط برای لاگ‌کردن یا در مرز بالای برنامه
استفاده کن. مدیریت خطای دقیق (`ValueError`, `KeyError`, ...) بهتر است.

### ۲.۳ `else` و `finally`

```python
try:
    f = open("data.txt", encoding="utf-8")
except FileNotFoundError:
    print("فایل پیدا نشد")
else:
    print("فایل باز شد")     # فقط وقتی خطایی نبود
finally:
    print("این همیشه اجرا می‌شود")
```

### ۲.۴ بالا بردن خطای خودت

```python
def parse_age(text):
    if not text.isdigit():
        raise ValueError(f"ورودی نامعتبر: {text!r}")
    return int(text)
```

```python
try:
    parse_age("بیست")
except ValueError as e:
    print(e)     # ورودی نامعتبر: 'بیست'
```

### ۲.۵ خطاهایی که باید بشناسی

| خطا | وقتی رخ می‌دهد |
|---|---|
| `NameError` | نام تعریف‌نشده |
| `TypeError` | نوع نامناسب (`"5" + 5`) |
| `ValueError` | نوع درست، مقدار غلط (`int("abc")`) |
| `IndexError` | اندیس خارج از محدوده |
| `KeyError` | کلید دیکشنری پیدا نشد |
| `AttributeError` | صفت/متد وجود ندارد |
| `ZeroDivisionError` | تقسیم بر صفر |
| `FileNotFoundError` | فایل نیست |
| `IndentationError` | تورفتگی اشتباه |

---

## ۳. ماژول و `pip`

### ماژول‌های استاندارد

```python
import math
print(math.sqrt(16))          # 4.0
print(math.pi)

from math import sqrt         # فقط این یکی
print(sqrt(25))

import random
print(random.randint(1, 6))   # عدد تصادفی ۱ تا ۶
print(random.choice(["a", "b", "c"]))

from datetime import datetime
print(datetime.now())

import os
print(os.getcwd())
```

### ماژول‌های شخصی

اگر `helpers.py` در کنار `main.py` باشد:

```python
import helpers
# یا
from helpers import my_function
```

### نصب پکیج با `pip`

```powershell
pip install requests
pip list
pip uninstall requests
```

⚠️ همیشه در محیط مجازی (virtual environment) نصب کن:

```powershell
python -m venv .venv
.venv\Scripts\activate        # ویندوز
source .venv/bin/activate     # مک/لینوکس
```

چرا؟ تا پکیج‌های پروژه‌ات با بقیه‌ی سیستم قاطی نشوند.

---

## ۴. خط فرمان (argv)

```python
import sys
print(sys.argv)
```

اجرا: `python script.py hello world` → `['script.py', 'hello', 'world']`

---

## ۵. کار با JSON

```python
import json

data = {"name": "مریم", "age": 25}

text = json.dumps(data, ensure_ascii=False)      # ذخیره به صورت متن
print(text)

back = json.loads(text)                          # خواندن از متن
print(back["name"])
```

⚠️ `ensure_ascii=False` برای فارسی لازم است، وگرنه به `\u06f1...` تبدیل می‌شود.

---

## ۶. چک‌لیست کیفیت کد

- [ ] `with` برای فایل
- [ ] `encoding="utf-8"` برای فایل‌های متنی
- [ ] مدیریت خطای مشخص، نه `except Exception` کور
- [ ] توابع کوچک و تک‌وظیفه‌ای
- [ ] نام متغیرها گویا (`total_price` بهتر از `tp`)
- [ ] `main` با `if __name__ == "__main__":`

---

## ✍️ تمرین کوتاه (دستی)

۱. فرق `except:` و `except Exception:` چیست؟
۲. چرا `open(f, "w")` خطرناک است؟
۳. خروجی `json.dumps({"نام": "علی"})` بدون `ensure_ascii=False` چه شکلی است؟

---

## ۷. تمرین‌های این درس

فایل: [`exercises/ex05_files_errors.py`](../exercises/ex05_files_errors.py)

```powershell
python exercises/ex05_files_errors.py
```

---
بعدش برو به [درس ۶](06_oop.md).
