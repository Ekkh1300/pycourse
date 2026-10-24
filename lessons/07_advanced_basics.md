# درس ۷ — ابزارهای حرفه‌ای پایتون

> هدف: ابزارهایی که کد پایتون را از «کارآمد» به «خوانا و حرفه‌ای» تبدیل می‌کنند.

---

## ۱. List Comprehension — کاری که با حلقه می‌کنی، در یک خط

```python
# کلاسیک
squares = []
for i in range(10):
    squares.append(i ** 2)

# حرفه‌ای
squares = [i ** 2 for i in range(10)]
```

### با شرط

```python
evens = [i for i in range(20) if i % 2 == 0]
```

### با `if/else` داخلی

```python
labels = ["짝" if n % 2 == 0 else "فرد" for n in range(6)]
```

### Dict و Set Comprehension

```python
squares_dict = {n: n ** 2 for n in range(5)}
unique_initials = {name[0] for name in ["علی", "امیر", "سارا", "سینا"]}
```

### دو حلقه

```python
pairs = [(x, y) for x in range(3) for y in range(2)]
```

⚠️ قاعده: comprehension برای **یک مقدار محاسبه** خوب است. اگر داخلش
`if`/`for`/`await` پیچیده شد، حلقه‌ی معمولی بنویس.

---

## ۲. `lambda` — تابع بی‌نام

```python
square = lambda x: x ** 2
square(4)      # 16
```

```python
# مرتب‌سازی بر اساس کلید دوم
people = [("مریم", 25), ("علی", 30), ("سارا", 22)]
people.sort(key=lambda p: p[1])
```

⚠️ اگر تابع بیشتر از یک خط شد، `def` بنویس. `lambda` فقط برای
**یک عبارت کوتاه** است.

---

## ۳. `map`، `filter`، `reduce`

```python
numbers = [1, 2, 3, 4, 5]

doubled = list(map(lambda x: x * 2, numbers))      # [2, 4, 6, 8, 10]
evens  = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

from functools import reduce
total = reduce(lambda a, b: a + b, numbers, 0)    # 15
```

در پایتون مدرن، comprehension معمولاً خواناتر از `map`/`filter` است.

---

## ۴. `enumerate` و `zip`

```python
fruits = ["سیب", "موز", "پرتقال"]

for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
# 1 سیب
# 2 موز
# 3 پرتقال
```

```python
names = ["علی", "سارا"]
ages  = [25, 30]

for name, age in zip(names, ages):
    print(name, age)
```

⚠️ `zip` کوتاه‌ترین لیست را مبنا می‌گیرد — اگر طول‌ها فرق کند، داده گم می‌شود.
اگر می‌خواهی مطمئن شوی: `zip(names, ages, strict=True)` (پایتون ۳.۱۰+).

---

## ۵. `sorted` با `key`

```python
users = [
    {"name": "مریم", "age": 25},
    {"name": "علی", "age": 30},
    {"name": "سارا", "age": 22},
]

users.sort(key=lambda u: u["age"])
users.sort(key=lambda u: u["name"], reverse=True)
```

### مرتب‌سازی چندکلیدی

```python
users.sort(key=lambda u: (u["age"], u["name"]))
```

---

## ۶. دکوریتور (`@decorator`)

دکوریتور = تابعی که تابع دیگر را می‌پوشاند.

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


@timer
def slow_work(n):
    return sum(range(n))


slow_work(1000000)
```

```python
@timer
@other_decorator
def f(): ...
```

ترتیب از پایین به بالا اجرا می‌شود.

### دکوریتور با آرگومان

```python
def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator
```

---

## ۷. فایل `__main__.py` و ساختار پروژه

```python
def main():
    print("برنامه شروع شد")

if __name__ == "__main__":
    main()
```

چرا؟ وقتی فایل را **import** می‌کنی، `main()` اجرا نمی‌شود — فقط تعریف می‌شود.
این استاندارد واقعی پایتون است.

ساختار پروژه‌ی تمیز:

```
my_project/
├── main.py
├── requirements.txt
├── .venv/
└── src/
    ├── __init__.py
    ├── models.py
    └── utils.py
```

---

## ۸. `pathlib` و کار با فایل (تکمیل درس ۵)

```python
from pathlib import Path

folder = Path("data")
folder.mkdir(exist_ok=True)

for txt in folder.glob("*.txt"):
    print(txt.name, txt.stat().st_size)
```

---

## ۹. مدیر زمینه (`context manager`)

```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.perf_counter()
    yield
    print(f"{name}: {time.perf_counter() - start:.3f}s")

with timer("work"):
    do_something()
```

---

## ۱۰. ابزارهای خط فرمان

```python
import argparse

parser = argparse.ArgumentParser(description="ابزار من")
parser.add_argument("--count", type=int, default=5, help="تعداد تکرار")
parser.add_argument("--name", required=True, help="نام")
args = parser.parse_args()

print(args.count, args.name)
```

```powershell
python tool.py --name مریم --count 3
```

---

## ۱۱. محیط مجازی و `requirements.txt`

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install requests pandas
pip freeze > requirements.txt
```

---

## ۱۲. تست با `pytest` (نگاهی سریع)

```python
# test_math.py
def test_add():
    from mymodule import add
    assert add(2, 3) == 5
```

```powershell
pip install pytest
pytest -v
```

فعلاً لازم نیست، ولی بدان که وجود دارد.

---

## ✍️ تمرین کوتاه (دستی)

۱. `[i*i for i in range(5) if i % 2 == 0]` چه می‌دهد؟
۲. `list(map(str, [1,2]))` چه می‌دهد؟
۳. فرق `sort` و `sorted` چیست؟

---

## ۱۳. تمرین‌های این درس

فایل: [`exercises/ex07_advanced.py`](../exercises/ex07_advanced.py)

```powershell
python exercises/ex07_advanced.py
```

---

## 🎉 پایان مسیر مقدماتی

بعد از این، یکی از چهار مسیر تخصصی را انتخاب کن:

| مسیر | قدم بعدی |
|---|---|
| **اتوماسیون** | `pathlib` + `openpyxl` + `requests` + `BeautifulSoup` |
| **وب و بک‌اند** | `FastAPI` + `uvicorn` + `SQLite` + `pydantic` |
| **هوش مصنوعی** | `NumPy` + `Pandas` + `matplotlib` + `scikit-learn` |
| **مبانی/الگوریتم** | `pytest` + `mypy` + تمرین‌های LeetCode |
