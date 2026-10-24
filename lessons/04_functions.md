# درس ۴ — توابع

> هدف: کد را به **قطعه‌های قابل استفاده‌ی مجدد** بشکنی. این مهم‌ترین مهارتی است که
> کدت را از «اسکریپت» به «برنامه» تبدیل می‌کند.

---

## ۱. تعریف تابع

```python
def greet():
    print("سلام!")

greet()      # فراخوانی
```

### تابع با آرگومان

```python
def greet(name):
    print(f"سلام {name}!")

greet("مریم")
```

### تابع با مقدار بازگشتی

```python
def add(a, b):
    return a + b

result = add(3, 5)    # result = 8
```

⚠️ فرق مهم:
```python
def f1():  return 5
def f2():  print(5)      # این None برمی‌گرداند!
```

تابعی که `return` ندارد، **همیشه `None`** برمی‌گرداند.

---

## ۲. آرگومان‌ها

### ۲.۱ پیش‌فرض (default)

```python
def greet(name, greeting="سلام"):
    print(f"{greeting} {name}!")

greet("مریم")                 # سلام مریم!
greet("مریم", "درود")         # درود مریم!
```

### ۲.۲ فقط کلیدی (keyword)

```python
def greet(name, greeting="سلام"):
    ...

greet(greeting="درود", name="مریم")   # ترتیب مهم نیست
```

### ۲.۳ فقط موقعیتی (positional-only)

```python
def greet(name, /, greeting="سلام"):
    ...
greet("مریم", "درود")    # ✅
greet(name="مریم")       # ❌ TypeError
```

### ۲.۴ ستاره: `*args` و `**kwargs`

```python
def total(*args):
    return sum(args)

total(1, 2, 3)      # 6

def profile(name, **kwargs):
    print(name, kwargs)

profile("مریم", age=25, city="تهران")
# مریم {'age': 25, 'city': 'تهران'}
```

### ۲.۵ ترتیب امضا

```python
def f(a, b=2, *args, c, **kwargs):
    ...
```
ترتیب اجباری: پارامترهای معمولی → پیش‌فرض → `*args` → فقط-کلیدی → `**kwargs`

---

## ۳. انواع داده (type hints) — پیشنهاد می‌کنم از همین امروز

```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str, excited: bool = False) -> str:
    return f"Hi {name}!"

def items() -> list[str]:
    return ["a", "b"]
```

type hint ها **اجباری نیستند** و پایتون آن‌ها را در زمان اجرا چک نمی‌کند،
ولی:
- خودت را مجبور می‌کنی فکر کنی
- خطاها را زودتر پیدا می‌کنی
- ادیتور بهتر راهنمایی می‌کند

---

## ۴. Scope — دامنه‌ی دسترسی

```python
x = "بیرون"

def show():
    print(x)          # ✅ خواندن از بیرون مشکلی ندارد

def change():
    x = "داخل"       # این یک متغیر جدیدِ محلی است!
    print(x)          # داخل

change()
print(x)              # هنوز "بیرون" است
```

قانون: اگر داخل تابع به نامی **-assign** کنی، آن نام در تمام آن تابع **محلی** می‌شود.

### `global` — با احتیاط!

```python
counter = 0

def increment():
    global counter
    counter += 1
```

⚠️ `global` معمولاً نشانه‌ی طراحی بد است. اگر زیاد لازم شد، احتمالاً بهتر است
نتیجه را `return` کنی یا از یک دیکشنری/کلاس استفاده کنی.

---

## ۵. پیش‌فرض‌های **mutable** — تله‌ی کلاسیک

```python
def add_item(item, bucket=[]):     # ❌ هر بار همان لیست!
    bucket.append(item)
    return bucket

add_item(1)   # [1]
add_item(2)   # [1, 2]  ← انتظار داشتی [2] باشد؟
```

راه‌حل:

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

قاعده: **هرگز** `[]` یا `{}` را به‌عنوان مقدار پیش‌فرض نگذار.

---

## ۶. چند تابع داخل یک فایل — ترتیب مهم

```python
def a():
    b()      # ✅ می‌شود، چون b موقع اجرا تعریف شده

def b():
    print("b")

a()
```

تابع باید **قبل از زمان فراخوانی** تعریف شده باشد، نه لزوماً قبل از فراخوانی
خط‌بالایی.

---

## ۷. توابع به‌عنوان مقدار (کاربردی)

```python
def double(x):  return x * 2
def triple(x):  return x * 3

ops = {"double": double, "triple": triple}
print(ops["double"](5))    # 10
```

```python
numbers = [1, 2, 3, 4]
doubled = list(map(double, numbers))     # [2, 4, 6, 8]
```

در درس ۷ `lambda` و حالت‌های کوتاه را یاد می‌گیریم.

---

## ۸. Docstring — مستندسازی

```python
def area(width, height):
    """مساحت مستطیل را برمی‌گرداند.

    Args:
        width: عرض مستطیل
        height: ارتفاع مستطیل

    Returns:
        عددی برابر با مساحت
    """
    return width * height
```

`help(area)` یا `area.__doc__` آن را نشان می‌دهد.
**در کدهای واقعی همیشه برای توابع غیربدیه بنویس.**

---

## ۹. تست سریع دستی

```python
def greet(name, greeting="سلام"):
    return f"{greeting} {name}"

greet("مریم")                # ?
greet("مریم", "درود")        # ?
greet(greeting="Hi", name="Ali")  # ?
```

---

## ۱۰. تمرین‌های این درس

فایل: [`exercises/ex04_functions.py`](../exercises/ex04_functions.py)

```powershell
python exercises/ex04_functions.py
```

---
بعدش برو به [درس ۵](05_files_errors_modules.md).
