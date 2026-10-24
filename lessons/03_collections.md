# درس ۳ — لیست، تاپل، دیکشنری و ست

> هدف: با مجموعه‌های داده کار کنی. این درس پایه‌ی همه‌ی مسیرهای تخصصی بعدی است
> (اتوماسیون، وب، ML) — همه‌شان با همین ساختارهای داده کار می‌کنند.

---

## ۱. لیست (`list`) — مجموعه‌ای **مرتب و تغییرپذیر**

```python
fruits = ["سیب", "موز", "پرتقال"]
numbers = [1, 2, 3]
mixed = [1, "hello", 3.5, True]     # مجاز است، ولی معمولاً خوب نیست
empty = []
```

### ۱.۱ اندیس (شماره‌ی خانه)

اندیس‌گذاری در پایتون **از صفر شروع می‌شود**:

```
fruits = ["سیب", "موز", "پرتقال"]
          [0]   [1]     [2]
```

```python
print(fruits[0])      # سیب
print(fruits[2])      # پرتقال
print(fruits[-1])     # پرتقال  ← اندیس منفی = از آخر
print(fruits[-2])     # موز
```

⚠️ اندیس خارج از محدوده → `IndexError`.

### ۱.۲ برش (slicing)

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

numbers[2:5]     # [2, 3, 4]        ← از ۲ تا قبل از ۵
numbers[:3]      # [0, 1, 2]
numbers[7:]      # [7, 8, 9]
numbers[::2]     # [0, 2, 4, 6, 8]  ← گام ۲
numbers[::-1]    # معکوس
```

قانون مهم: **اندیسِ دوم شامل نمی‌شود** (`[a:b]` یعنی از `a` تا `b-1`).

### ۱.۳ متدهای پرکاربرد

```python
numbers = [5, 3, 8, 1]

numbers.append(10)      # [5, 3, 8, 1, 10]   ← اضافه کردن به آخر
numbers.insert(0, 99)  # [99, 5, 3, 8, 1, 10] ← در اندیس ۰
numbers.remove(99)      # حذف اولین مقدار 99
last = numbers.pop()    # حذف از آخر + برگرداندن مقدارش
numbers.sort()          # مرتب‌سازی (در جا)
numbers.reverse()       # برعکس کردن (در جا)

len(numbers)            # طول
numbers.count(3)        # چند تا 3 دارد
3 in numbers            # آیا هست؟ → True/False
```

⚠️ متدهای `sort`, `reverse`, `append` لیست را **در جا** تغییر می‌دهند و `None` برمی‌گردانند.
برای نسخه‌ی بدون تغییر: `sorted(numbers)` و `numbers[::-1]`.

### ۱.۴ پیمایش

```python
for fruit in fruits:
    print(fruit)
```

با اندیس:

```python
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

(در درس ۷ بیشتر درباره‌ی `enumerate` می‌خوانیم.)

---

## ۲. تاپل (`tuple`) — مثل لیست، ولی **تغییرناپذیر**

```python
point = (3, 5)
point[0]      # 3
point[0] = 10 # ❌ TypeError: 'tuple' object does not support item assignment
```

**چرا مهم است؟**
- سریع‌تر از لیست
- به‌عنوان کلید دیکشنری قابل استفاده است (لیست نیست)
- «تغییرناپذیری» یعنی نمی‌شود به‌اشتباه خرابش کرد

```python
x, y = (3, 5)        # تجزیه (unpacking)
a, b, c = 1, 2, 3    # بدون پرانتز هم می‌شود
```

تاپل تک‌عضوی: `(5,)` — کاما لازم است.

---

## ۳. دیکشنری (`dict`) — کلید → مقدار

```python
user = {
    "name": "مریم",
    "age": 25,
    "city": "تهران",
}
```

```python
user["name"]            # "مریم"
user["age"] = 26        # تغییر مقدار
user["job"] = "برنامه‌نویس"  # افزودن کلید جدید
del user["city"]        # حذف
"age" in user           # True
```

### ۳.۱ `.get()` — راه امن خواندن

```python
user["name"]      # اگر نبود → KeyError
user.get("name")  # اگر نبود → None
user.get("name", "نامشخص")  # اگر نبود → "نامشخص"
```

### ۳.۲ پیمایش روی دیکشنری

```python
for key in user:
    print(key)

for key, value in user.items():
    print(key, "=>", value)

for key in user.keys():
    ...
for value in user.values():
    ...
```

### ۳.۳ دیکشنری تودرتو

```python
users = {
    "ali":  {"age": 30, "city": "تهران"},
    "sara": {"age": 25, "city": "شیراز"},
}

print(users["ali"]["city"])          # تهران
print(users.get("sara", {}).get("age"))  # 25

# ایمن‌تر برای داده‌های تودرتو:
age = users.get("sara", {}).get("age", 0)
```

### ۳.۴ `setdefault` و `Counter`-گونه

```python
d = {}
d.setdefault("count", 0)
d["count"] += 1
```

---

## ۴. ست (`set`) — مجموعه‌ی **تکراری‌نبودنی**

```python
nums = {1, 2, 3, 3, 2}
print(nums)      # {1, 2, 3}
```

```python
a = {1, 2, 3}
b = {3, 4, 5}

a | b      # {1,2,3,4,5}   اتحاد
a & b      # {3}           اشتراک
a - b      # {1,2}         تفاضل
a ^ b      # {1,2,4,5}     تفاضل متقارن
```

### ۴.۱ کاربرد مهم: حذف تکراری

```python
numbers = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(numbers))    # ترتیب تضمین‌شده نیست!
```

### ۴.۲ کاربرد مهم: تست عضویت سریع

```python
allowed = {"ali", "sara", "reza"}
if "ali" in allowed:      # سریع‌تر از لیست
    ...
```

---

## ۵. تبدیل بین آن‌ها

```python
list(("a", "b"))          # ['a', 'b']
tuple([1, 2])             # (1, 2)
set([1, 2, 2])            # {1, 2}
dict([("a", 1), ("b", 2)]) # {'a': 1, 'b': 2}
list("abc")               # ['a', 'b', 'c']
```

---

## ۶. کدام را انتخاب کنم؟

| ساختار | وقتی استفاده کن |
|---|---|
| `list` | مجموعه‌ی مرتب که تغییر می‌کند |
| `tuple` | مجموعه‌ی ثابت (مثل رنگ RGB یا مختصات) |
| `dict` | داده‌ی کلید-مقدار (مثل رکورد کاربر) |
| `set` | یکتا کردن و تست عضویت سریع |

---

## ۷. کپی سطحی — تله‌ی مهم!

```python
a = [1, 2, 3]
b = a            # ❌ هر دو به یک لیست اشاره دارند!
b.append(4)
print(a)         # [1, 2, 3, 4]  ← a هم عوض شد!

b = a.copy()     # ✅ کپی واقعی (سطحی)
```

برای لیست‌های تودرتو، `copy.deepcopy()` لازم است (از `copy` import می‌کنیم).

---

## ✍️ تمرین کوتاه (دستی)

۱. خروجی `nums[1:3]` و `nums[::2]` برای `nums = [0,1,2,3,4,5]` چیست؟
۲. چرا `users["ali"]["city"]` می‌تواند خطا بدهد و `users.get("ali", {}).get("city")` نه؟
۳. `a = [1,2]; b = a; b += [3]; print(a)` چه می‌دهد؟

---

## ۹. تمرین‌های این درس

فایل: [`exercises/ex03_collections.py`](../exercises/ex03_collections.py)

```powershell
python exercises/ex03_collections.py
```

---
بعدش برو به [درس ۴](04_functions.md).
