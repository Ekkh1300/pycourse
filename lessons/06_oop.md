# درس ۶ — کلاس‌ها و شیءگرایی

> هدف: مدل کردن دنیای واقعی. یک «کلاس» = یک قالب، یک «شیء» = یک نمونه از آن قالب.

> **یادآوری:** در پایتون OOP ابزار است، نه فلسفه. خیلی وقت‌ها یک دیکشنری ساده کافی است.
> اما برای مسیر وب و ML و پروژه‌های بزرگ‌تر، کلاس‌ها ضروری می‌شوند.

---

## ۱. کلاس چیست؟

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} می‌گوید: هاو!")

rex = Dog("رکس", 3)
print(rex.name)      # رکس
rex.bark()           # رکس می‌گوید: هاو!
```

### اجزا:
- `class Dog:` → تعریف کلاس
- `__init__` → **سازنده**؛ وقتی `Dog(...)` صدا زده شود خودکار اجرا می‌شود
- `self` → اشاره به خودِ شیء جاری (پایتون خودش پاس می‌دهد؛ تو نمی‌نویسی)
- `self.name = name` → ساختن صفت روی شیء

⚠️ `self` را فراموش نکن — پرتکرارترین خطای تازه‌کارهاست.

---

## ۲. `__init__` و مقداردهی پیش‌فرض

```python
class Dog:
    def __init__(self, name, age=1, breed=None):
        self.name = name
        self.age = age
        self.breed = breed if breed else "نامشخص"
```

ساخت شیء:
```python
a = Dog("پتی")
b = Dog("شاهو", 4)
c = Dog("بُر", 2, "پولی")
```

---

## ۳. متدها

متد = تابعی که روی شیء کار می‌کند.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name}: هاو!"

    def birthday(self):
        self.age += 1
        return self.age
```

```python
d = Dog("شاهو", 2)
print(d.bark())      # شاهو: هاو!
print(d.birthday())  # 3
```

---

## ۴. `__str__` و `__repr__`

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"سگ {self.name} ({self.age} ساله)"

    def __repr__(self):
        return f"Dog(name={self.name!r}, age={self.age!r})"
```

```python
print(d)            # سگ شاهو (2 ساله)          → __str__
print(repr(d))      # Dog(name='شاهو', age=2)     → __repr__
```

`__repr__` برای دیباگ است و باید «کد-مانند» باشد.

---

## ۵. صفات کلاس در برابر صفات نمونه

```python
class Dog:
    species = "سگ"          # صفت کلاس (مشترک بین همه)

    def __init__(self, name):
        self.name = name     # صفت نمونه (مخصوص این شیء)
```

```python
Dog.species         # "سگ"  → از طریق کلاس
d.species           # "سگ"  → از طریق نمونه هم در دسترس است
d.species = "باز"   # ⚠️ این صفت نمونه می‌سازد، صفت کلاس را تغییر نمی‌دهد
Dog.species         # هنوز "سگ" است
```

---

## ۶. `@property` — متدی که مثل صفت صدا زده می‌شود

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)
```

```python
r = Rectangle(3, 4)
print(r.area)        # 12  ← بدون پرانتز!
```

### setter — وقتی می‌خواهی هنگام تغییر، اعتبارسنجی کنی

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("عرض باید مثبت باشد")
        self._width = value
```

---

## ۷. `@classmethod` و `@staticmethod`

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_birth_year(cls, name, birth_year, current_year=2026):
        """ساخت شیء از روی سال تولد"""
        return cls(name, current_year - birth_year)

    @staticmethod
    def is_adult(age):
        return age >= 18


rex = Dog.from_birth_year("رکس", 2020)   # cls یعنی کلاس
Dog.is_adult(20)
```

- `@classmethod` → `cls` (خودِ کلاس)؛ برای سازنده‌های جایگزین
- `@staticmethod` → هیچ `self`/`cls`؛ صرفاً تابع کمکی مرتبط با کلاس

---

## ۸. وراثت (Inheritance)

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} صدا می‌کند.")

    def __str__(self):
        return f"{type(self).__name__} named {self.name}"


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)      # فراخوانی __init__ پدر
        self.breed = breed

    def speak(self):                # بازنویسی (override)
        print(f"{self.name}: هاو!")


class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name)
        self.indoor = indoor
```

```python
d = Dog("شاهو", "پولی")
d.speak()      # شاهو: هاو!
print(d)        # Dog named شاهو
```

⚠️ `super().__init__(name)` فراموش نشود، وگرنه `self.name` ساخته نمی‌شود.

---

## ۹. ترکیب به‌جای وراثت

**ترکیب (composition)** یعنی «داشتن» به‌جای «بودن».
معمولاً بهتر است:

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        return "روشن شد"


class Car:
    def __init__(self, name, engine):
        self.name = name
        self.engine = engine     # Car یک Engine دارد

    def drive(self):
        return f"{self.name}: {self.engine.start()}"
```

---

## ۱۰. دیت‌کلاس (ساختارهای دادهی آماده)

پایتون ۳.۷+:

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int = 0
    tags: list[str] = field(default_factory=list)

    def birthday(self):
        self.age += 1
        return self
```

`__init__`، `__repr__` و `__eq__` خودکار ساخته می‌شوند. برای مدل‌های داده
(کاربر، سفارش، محصول) **فوق‌العاده** تمیز است.

---

## ۱۱. چه زمانی کلاس بسازم؟

| موقعیت | ابزار |
|---|---|
| داده‌ی ساده‌ی کلید-مقدار | `dict` |
| مجموعه‌ی هم‌نوع با رفتار مشترک | `dataclass` |
| رفتار پیچیده + چند نوع مرتبط | `class` |
| فقط یک تابع کمکی | تابع ساده |

**قانون:** اول با دیکشنری بنویس. اگر بزرگ و کلافه شد → کلاس.

---

## ✍️ تمرین کوتاه (دستی)

۱. فرق `self` و `cls` چیست؟
۲. چرا `@property` روی `area` بدون پرانتز صدا زده می‌شود ولی متد عادی با پرانتز؟
۳. اگر `__init__` را ننویسی، `Dog("x")` چه می‌شود؟ (فقط برای کلاس بدون وراثت)

---

## ۱۲. تمرین‌های این درس

فایل: [`exercises/ex06_oop.py`](../exercises/ex06_oop.py)

```powershell
python exercises/ex06_oop.py
```

---
بعدش برو به [درس ۷](07_advanced_basics.md).
