# درس ۲ — شرط‌ها و حلقه‌ها

> هدف: برنامه‌ات را «زنده» کنی — بر اساس داده تصمیم بگیرد و کار تکراری را با حلقه
> کوتاه کنی.

---

## ۱. `if` — شرط ساده

```python
age = 20

if age >= 18:
    print("می‌توانی رانندگی کنی")
```

اگر شرط درست نباشد، هیچ اتفاقی نمی‌افتد (برنامه رد می‌شود).

### `if / else`

```python
age = 15

if age >= 18:
    print("بزرگسال")
else:
    print("نوجوان")
```

### `if / elif / else` — زنجیره‌ی شرط

```python
grade = 85

if grade >= 90:
    print("عالی")
elif grade >= 75:
    print("خیلی خوب")
elif grade >= 60:
    print("قبول")
else:
    print("مردود")
```

⚠️ پایتون **فقط اولین شرطِ درست** را اجرا می‌کند و بقیه را رد می‌کند.
پس ترتیب شرط‌ها مهم است: از سخت‌گیرانه‌ترین (بزرگ‌ترین عدد) به ساده‌ترین.

---

## ۲. عملگرهای ترکیبی

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("ورود مجاز")
elif age >= 18 or has_ticket:
    print("فقط یکی از شرط‌ها درست است")
else:
    print("ورود ممنوع")
```

| الگو | معنی |
|---|---|
| `a and b` | هر دو درست |
| `a or b` | حداقل یکی درست |
| `not a` | معکوس |
| `a != b` | نابرابر |

**نکته‌ی مهم:** در پایتون `and`/`or` نتیجه‌شان یک **مقدار** است، نه فقط `True/False`:

```python
value = 5
print(value and 10)    # 10   (چون value غیرصفر است → نتیجه دوم)
value = 0
print(value and 10)    # 0    (چون value صفر است → همان 0 برمی‌گردد)
```

این ویژگی در درس ۷ (حالت‌های کوتاه‌نویسی) به کارت می‌آید.

---

## ۳. حلقه‌ی `while` — «تا وقتی که»

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

⚠️ **خطر گرفتارشدن در حلقه‌ی بی‌پایان:** اگر `count += 1` را فراموش کنی، حلقه هیچ‌وقت
تمام نمی‌شود. اگر برنامه‌ات هنگ کرد، اول همین را چک کن.

---

## ۴. حلقه‌ی `for` — «به تعداد مشخص»

```python
for i in range(5):
    print(i)
# 0 1 2 3 4
```

### `range` — سه شکل مهم

```python
range(5)          # 0, 1, 2, 3, 4              → ۵ عدد از ۰
range(2, 6)       # 2, 3, 4, 5                 → از ۲ تا ۵
range(0, 10, 2)   # 0, 2, 4, 6, 8              → گام ۲
range(5, 0, -1)   # 5, 4, 3, 2, 1              → شمارش معکوس
```

### پیمایش روی رشته و لیست

```python
for ch in "hello":
    print(ch)

for item in [10, 20, 30]:
    print(item)
```

---

## ۵. `break` و `continue`

```python
for i in range(10):
    if i == 5:
        break        # از حلقه بیرون بیا
    print(i)
# 0 1 2 3 4

for i in range(10):
    if i % 2 == 0:
        continue     # این دور را رد کن، برو دور بعد
    print(i)
# 1 3 5 7 9
```

---

## ۶. `else` روی حلقه (نکته‌ی ظریف)

در پایتون، `else` بعد از حلقه وقتی اجرا می‌شود که حلقه **بدون `break`** تمام شود:

```python
for n in range(2, 10):
    if n == 7:
        print("پیدا شد!")
        break
else:
    print("پیدا نشد")
```

این یک الگوی تمیز برای جست‌وجو است.

---

## ۷. الگوهای کاربردی

### ۷.۱ شمارش معکوس

```python
for i in range(10, 0, -1):
    print(i)
```

### ۷.۲ تا وقتی کاربر عدد نادرست وارد نکند (این را حفظ کن)

```python
while True:
    raw = input("یک عدد وارد کن: ")
    try:
        number = int(raw)
        break
    except ValueError:
        print("❌ این عدد نیست، دوباره تلاش کن.")

print(f"گرفتیم: {number}")
```

### ۷.۳ انباشت (accumulator)

```python
total = 0
for i in range(1, 6):
    total += i
print(total)   # 15
```

این الگو (یک متغیر بیرون حلقه + جمع/ضرب داخل حلقه) **بسیار** پرتکرار است.

---

## ۸. تله‌های رایج

| تله | نشانه | راه‌حل |
|---|---|---|
| `=` به‌جای `==` | `if x = 5:` → `SyntaxError` | `==` برای مقایسه |
| شرط بدون `==` | `if x:` همیشه درست است برای عدد غیرصفر | `if x == 0:` |
| تورفتگی اشتباه | `IndentationError` | تب را بزن، ۴ فاصله |
| حلقه‌ی بی‌پایان | برنامه هنگ می‌کند | متغیر حلقه را حتماً تغییر بده |
| `or`/`and` به‌جای `||`/`&&` | `SyntaxError` | در پایتون `||` وجود ندارد |

---

## ✍️ تمرین کوتاه (دستی)

۱. خروجی این کد چیست؟
```python
x = 5
if x > 10:
    print("A")
elif x > 3:
    print("B")
else:
    print("C")
```
۲. خروجی این کد چیست؟
```python
for i in range(1, 10, 3):
    print(i, end=" ")
```
۳. خروجی این کد چیست؟
```python
n = 0
while n < 3:
    print(n)
    n += 1
else:
    print("done")
```

---

## ۹. تمرین‌های این درس

فایل: [`exercises/ex02_control_flow.py`](../exercises/ex02_control_flow.py)

```powershell
python exercises/ex02_control_flow.py
```

---
بعدش برو به [درس ۳](03_collections.md).
