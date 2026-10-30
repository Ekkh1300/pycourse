"""
تمرین ۳ — لیست، تاپل، دیکشنری و ست
================================================================
اجرا:  python exercises/ex03_collections.py
"""

import sys

# ویندوز: کنسول پیش‌فرض cp1252 است و متن فارسی را خراب می‌کنند — این خط‌ها حلش می‌کنند
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — کار با لیست
# لیست numbers را بساز: [12, 7, 25, 3, 18]
# سپس:
#   biggest      = بزرگ‌ترین عدد
#   smallest     = کوچک‌ترین عدد
#   total        = مجموع همه
#   evens        = تعداد اعداد زوج
#   doubled      = لیستی از مضرب‌های ۲ (بدون تغییر در لیست اصلی)
# ─────────────────────────────────────────────────────────────
numbers = [12, 7, 25, 3, 18]
biggest = None
smallest = None
total = None
evens = None
doubled = None

# ─────────────────────────────────────────────────────────────
# TODO 2 — برش
# برای لیست numbers این‌ها را بساز:
#   first_two   = دو تای اول
#   last_two    = دو تای آخر
#   reversed_list = نسخه‌ی برعکس (بدون تغییر در لیست اصلی)
# ─────────────────────────────────────────────────────────────
first_two = None
last_two = None
reversed_list = None

# ─────────────────────────────────────────────────────────────
# TODO 3 — دیکشنری
# دیکشنری student بساز:
#   {"name": "سارا", "age": 21, "grades": [85, 90, 78]}
# سپس:
#   average = میانگین نمره‌ها (به float تقسیم کن)
#   highest = بیشترین نمره
#   info    = رشته‌ای مثل "سارا: 21"
#   summary = دیکشنری کوچک‌تر فقط با name و average
# ─────────────────────────────────────────────────────────────
student = {"name": "سارا", "age": 21, "grades": [85, 90, 78]}
average = None
highest = None
info = None
summary = None

# ─────────────────────────────────────────────────────────────
# TODO 4 — ست
# با دو ست زیر کار کن:
#   a = {1, 2, 3, 4, 5}
#   b = {4, 5, 6, 7}
# و این‌ها را بساز:
#   union        = اتحاد (a | b)
#   intersection = اشتراک (a & b)
#   difference   = تفاضل (a - b)
#   duplicates   = لیست عناصر تکراری در لیست زیر
# ─────────────────────────────────────────────────────────────
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7}
union = None
intersection = None
difference = None

raw = [1, 2, 2, 3, 3, 3, 4, 4, 5]
duplicates = None

# ─────────────────────────────────────────────────────────────
# TODO 5 — تابع با دیکشنری
# تابع word_count(text) بنویس که یک dict برگرداند:
#   {"سلام": 2, "خداحافظ": 1}
# یعنی تعداد تکرار هر کلمه.
# نکته: کلمات را با split جدا کن.
# ─────────────────────────────────────────────────────────────


def word_count(text):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 6 — تابع با لیست (فیلتر)
# تابع even_squares(numbers) بنویس که لیستی از مربع اعداد زوج برگرداند.
# مثال: even_squares([1,2,3,4]) → [4, 16]
# ─────────────────────────────────────────────────────────────


def even_squares(numbers):
    pass


# ═════════════════════════════════════════════════════════════
#  تست‌ها
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("در حال بررسی...\n")

    # TODO 1
    assert biggest == 25, f"biggest باید 25 باشد، هست: {biggest!r}"
    assert smallest == 3, f"smallest باید 3 باشد، هست: {smallest!r}"
    assert total == 65, f"total باید 65 باشد، هست: {total!r}"
    assert evens == 2, f"evens باید 2 باشد، هست: {evens!r}"
    assert doubled == [24, 14, 50, 6, 36], f"doubled اشتباه: {doubled!r}"
    assert numbers == [12, 7, 25, 3, 18], "لیست اصلی نباید تغییر کند!"

    # TODO 2
    assert first_two == [12, 7], f"first_two اشتباه: {first_two!r}"
    assert last_two == [3, 18], f"last_two اشتباه: {last_two!r}"
    assert reversed_list == [18, 3, 25, 7, 12], f"reversed_list اشتباه: {reversed_list!r}"
    assert numbers == [12, 7, 25, 3, 18], "لیست اصلی نباید تغییر کند!"

    # TODO 3
    assert average == 84.33333333333333, f"average اشتباه: {average!r}"
    assert highest == 90, f"highest اشتباه: {highest!r}"
    assert info == "سارا: 21", f"info اشتباه: {info!r}"
    assert summary == {"name": "سارا", "average": average}, f"summary اشتباه: {summary!r}"

    # TODO 4
    assert union == {1, 2, 3, 4, 5, 6, 7}, f"union اشتباه: {union!r}"
    assert intersection == {4, 5}, f"intersection اشتباه: {intersection!r}"
    assert difference == {1, 2, 3}, f"difference اشتباه: {difference!r}"
    assert sorted(duplicates) == [2, 3, 4], f"duplicates اشتباه: {duplicates!r}"
    assert len(duplicates) == 3, f"تکراری‌ها نباید دوباره تکرار شوند: {duplicates!r}"

    # TODO 5
    wc = word_count("سلام دنیا، خداحافظ دنیا")
    assert wc == {"سلام": 1, "دنیا،": 1, "خداحافظ": 1, "دنیا": 1}, f"wc اشتباه: {wc!r}"
    wc2 = word_count("a b a")
    assert wc2 == {"a": 2, "b": 1}, f"wc2 اشتباه: {wc2!r}"

    # TODO 6
    assert even_squares([1, 2, 3, 4]) == [4, 16], "even_squares اشتباه"
    assert even_squares([5, 7]) == [], "باید لیست خالی برگرداند"
    assert even_squares([2, 4, 6]) == [4, 16, 36], "even_squares اشتباه"

    print("✅ همه‌ی تست‌ها پاس شد! حالا کدت را برای من بفرست.")
