"""
تمرین ۵ — فایل، مدیریت خطا و ماژول
================================================================
اجرا:  python exercises/ex05_files_errors.py

این تمرین از یک پوشه‌ی موقت در سیستم استفاده می‌کند و بعد پاکش می‌کند،
پس هیچ فایلی روی سیستم شما باقی نمی‌ماند.
"""

import json
import sys
import tempfile
from pathlib import Path

# ویندوز: کنسول پیش‌فرض cp1252 است و متن فارسی را خراب می‌کنند — این خط‌ها حلش می‌کنند
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────────────────────
# TODO 1 — نوشتن در فایل
# تابع write_lines(path, lines) بنویس که هر عضو lines را در یک خط جدا بنویسد.
# از with open(..., "w", encoding="utf-8") استفاده کن.
# ─────────────────────────────────────────────────────────────


def write_lines(path, lines):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 2 — خواندن از فایل
# تابع read_lines(path) بنویس که لیست خطوط فایل را برگرداند
# (بدون کاراکتر \n در انتهای هر خط — از strip استفاده کن).
# اگر فایل نبود، لیست خالی [] برگردان (نه خطا!).
# ─────────────────────────────────────────────────────────────


def read_lines(path):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 3 — نوشتن JSON
# تابع save_json(path, data) بنویس که data را به فایل JSON ذخیره کند.
# از json.dump با ensure_ascii=False استفاده کن.
# ─────────────────────────────────────────────────────────────


def save_json(path, data):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 4 — خواندن JSON
# تابع load_json(path) بنویس که JSON را بخواند و برگرداند.
# اگر فایل نبود یا محتوایش JSON معتبر نبود → None برگردان.
# ─────────────────────────────────────────────────────────────


def load_json(path):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 5 — تبدیل امن به عدد
# تابع to_int(text) بنویس که رشته را به int تبدیل کند.
# اگر تبدیل ممکن نبود → None برگردان (بدون کرش کردن برنامه).
# راهنما: از try/except ValueError استفاده کن.
# ─────────────────────────────────────────────────────────────


def to_int(text):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 6 — خطای سفارشی
# تابع parse_age(text) بنویس:
#   - اگر text را نمی‌شود به int تبدیل کرد → ValueError("invalid age") بده
#   - اگر منفی بود → ValueError("negative age") بده
#   - در غیر این صورت عدد صحیح را برگرداند
# ─────────────────────────────────────────────────────────────


def parse_age(text):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 7 — شمارش کلمات یک فایل
# تابع count_words(path) بنویس که تعداد کل کلمات فایل را برگرداند.
# (با split کردن محتوا و شمردن؛ اگر فایل نبود → 0)
# ─────────────────────────────────────────────────────────────


def count_words(path):
    pass


# ═════════════════════════════════════════════════════════════
#  تست‌ها
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("در حال بررسی...\n")

    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        txt = folder / "test.txt"
        js = folder / "test.json"

        # TODO 1
        write_lines(txt, ["سلام", "خداحافظ", "پایتون"])
        assert txt.exists(), "فایل ساخته نشد"
        assert txt.read_text(encoding="utf-8").count("\n") == 3, "تعداد خطوط اشتباه"

        # TODO 2
        lines = read_lines(txt)
        assert lines == ["سلام", "خداحافظ", "پایتون"], f"read_lines اشتباه: {lines!r}"
        missing = read_lines(folder / "nope.txt")
        assert missing == [], f"فایل ناموجود باید [] بدهد: {missing!r}"

        # TODO 3
        save_json(js, {"name": "مریم", "age": 25, "city": "تهران"})
        assert js.exists(), "فایل JSON ساخته نشد"
        raw = js.read_text(encoding="utf-8")
        assert "مریم" in raw, "نام فارسی باید خوانا ذخیره شود (ensure_ascii=False)"

        # TODO 4
        data = load_json(js)
        assert data == {"name": "مریم", "age": 25, "city": "تهران"}, f"load_json اشتباه: {data!r}"
        assert load_json(folder / "nope.json") is None, "فایل ناموجود باید None بدهد"

        bad = folder / "bad.json"
        bad.write_text("این JSON نیست", encoding="utf-8")
        assert load_json(bad) is None, "JSON نامعتبر باید None بدهد"

        # TODO 5
        assert to_int("42") == 42, "to_int اشتباه"
        assert to_int("سلام") is None, "to_int باید None بدهد"
        assert to_int("3.5") is None, "اعشاری نباید پذیرفته شود"

        # TODO 6
        assert parse_age("30") == 30, "parse_age اشتباه"
        for bad_input, msg in [("abc", "invalid age"), ("-5", "negative age")]:
            try:
                parse_age(bad_input)
                raise AssertionError(f"باید برای {bad_input!r} خطا می‌داد!")
            except ValueError as e:
                assert str(e) == msg, f"پیام اشتباه: {e}"

        # TODO 7
        write_lines(txt, ["یک دو سه", "چهار پنج"])
        assert count_words(txt) == 5, f"count_words اشتباه: {count_words(txt)}"
        assert count_words(folder / "nope.txt") == 0, "فایل ناموجود باید 0 بدهد"

    print("✅ همه‌ی تست‌ها پاس شد! حالا کدت را برای من بفرست.")
