"""
آزمون سریع پایتون — ۲۰ سوال چهارگزینه‌ای
================================================================
اجرا:  python practice/quiz.py

هدف: بعد از هر ۲-۳ درس، یک بار این آزمون را بده تا ببینی چقدر بلدی.
نمره‌ی کمتر از ۷۰٪ یعنی باید برگردی و درس را دوباره بخوانی.
"""

import os
import sys

# ویندوز: کنسول پیش‌فرض cp1252 است و متن فارسی را خراب می‌کنند — این خط‌ها حلش می‌کنند
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

QUESTIONS = [
    {
        "q": "خروجی `5 / 2` چیست؟",
        "options": ["2", "2.5", "2.0", "خطا"],
        "answer": 1,
        "why": "`/` همیشه نتیجه‌ی float می‌دهد. برای تقسیم صحیح از `//` استفاده کن.",
    },
    {
        "q": "خروجی `bool(\"False\")` چیست؟",
        "options": ["False", "True", "خطا", "None"],
        "answer": 1,
        "why": "هر رشته‌ی غیرخالی (حتی \"False\") در پایتون True است.",
    },
    {
        "q": "خروجی `10 / 2 == 5` چیست؟",
        "options": ["True", "False", "خطا", "5.0"],
        "answer": 0,
        "why": "‎10/2 می‌شود 5.0 و مقدار 5.0 == 5 برابر است.",
    },
    {
        "q": "کدام‌یک مقدار `None` برمی‌گرداند؟",
        "options": [
            "def f(): return 0",
            "def f(): print(0)",
            "def f(): return None",
            "همه‌ی موارد بالا",
        ],
        "answer": 3,
        "why": "تابعی که `return` ندارد همیشه None برمی‌گرداند.",
    },
    {
        "q": "خروجی `nums[1:3]` برای `nums = [0,1,2,3,4]` چیست؟",
        "options": ["[1, 2]", "[1, 2, 3]", "[0, 1, 2]", "[2, 3]"],
        "answer": 0,
        "why": "برش شامل اندیس دوم نیست: از ۱ تا قبل از ۳.",
    },
    {
        "q": "برای خواندن امن کلید دیکشنری از کدام استفاده می‌کنیم؟",
        "options": ["d[k]", "d.get(k)", "d[k:]", "d.pop(k)"],
        "answer": 1,
        "why": "`.get()` وقتی کلید نبود None برمی‌گرداند به‌جای KeyError.",
    },
    {
        "q": "خروجی `list(range(2, 10, 3))` چیست؟",
        "options": ["[2,3,4,5,6,7,8,9]", "[2,5,8]", "[3,6,9]", "[2,10]"],
        "answer": 1,
        "why": "range(شروع، پایان، گام) — پایان شامل نمی‌شود.",
    },
    {
        "q": "اگر تابعی `return` نداشته باشد، چه برمی‌گرداند؟",
        "options": ["0", "None", "False", "خطا"],
        "answer": 1,
        "why": "پایتون به‌صورت خودکار None برمی‌گرداند.",
    },
    {
        "q": "کدام ساختار برای «کلید → مقدار» مناسب است؟",
        "options": ["list", "tuple", "dict", "set"],
        "answer": 2,
        "why": "dict نگاشت کلید به مقدار است.",
    },
    {
        "q": "خروجی `len(\"سلام\")` چیست؟",
        "options": ["3", "4", "5", "خطا"],
        "answer": 1,
        "why": "len روی رشته تعداد کاراکترها (کدپوینت‌ها) را می‌دهد، نه حروف.",
    },
    {
        "q": "کدام روش برای افزودن به **آخر** لیست است؟",
        "options": ["insert(0, x)", "append(x)", "extend_end(x)", "push(x)"],
        "answer": 1,
        "why": "`append` اضافه می‌کند، `insert` در اندیس دلخواه جا می‌دهد.",
    },
    {
        "q": "خروجی این کد چیست؟\n```\na = [1,2]\nb = a\nb.append(3)\nprint(a)\n```",
        "options": ["[1, 2]", "[1, 2, 3]", "[3]", "خطا"],
        "answer": 1,
        "why": "b همان لیست a است (نه کپی). برای کپی از `a.copy()` استفاده کن.",
    },
    {
        "q": "کدام روش فایل را حتی در صورت خطا می‌بندد؟",
        "options": ["open(f).read()", "with open(f) as g:", "f = open(f)", "read(f)"],
        "answer": 1,
        "why": "بلوک `with` مدیر زمینه است و فایل را تضمینی می‌بندد.",
    },
    {
        "q": "برای گرفتن ورودی عددی از کاربر چه می‌نویسیم؟",
        "options": [
            "number = input()",
            "number = int(input())",
            "number = float(input())",
            "number = input(int())",
        ],
        "answer": 1,
        "why": "input همیشه رشته می‌دهد، پس باید تبدیل کنی.",
    },
    {
        "q": "خروجی این کد چیست؟\n```\nfor i in range(3):\n    if i == 1:\n        continue\n    print(i)\n```",
        "options": ["0 1 2", "0 2", "1", "0"],
        "answer": 1,
        "why": "`continue` آن دور را رد می‌کند، پس ۱ چاپ نمی‌شود.",
    },
    {
        "q": "کدام گزینه برای مقدار پیش‌فرض یک تابع **اشتباه** است؟",
        "options": [
            "def f(x=0): ...",
            "def f(x=None): ...",
            "def f(x=[]): ...",
            "def f(x='hi'): ...",
        ],
        "answer": 2,
        "why": "لیست پیش‌فرض بین فراخوانی‌ها مشترک می‌ماند — تله‌ی کلاسیک.",
    },
    {
        "q": "در کلاس، `self` به چه اشاره دارد؟",
        "options": ["کلاس", "خودِ شیء جاری", "ماژول", "تابع"],
        "answer": 1,
        "why": "`self` یعنی همین نمونه. `cls` یعنی خودِ کلاس.",
    },
    {
        "q": "خروجی `[i*i for i in range(5) if i % 2 == 0]` چیست؟",
        "options": ["[0, 4, 16]", "[0, 1, 4, 9, 16]", "[0, 2, 4]", "[1, 3]"],
        "answer": 0,
        "why": "Comprehension با شرط: فقط اعداد زوج، مربع‌شان.",
    },
    {
        "q": "برای حذف تکراری‌ها از یک لیست، بهترین گزینه چیست؟",
        "options": ["set(list)", "list(set(lst))", "lst.unique()", "remove_duplicates(lst)"],
        "answer": 1,
        "why": "`set` یکتا می‌کند؛ برای برگرداندن لیست باید دوباره به لیست تبدیل شود (ترتیب تضمین نمی‌شود).",
    },
    {
        "q": "کدام کد درست یک فایل را با انکدینگ مناسب می‌خواند؟",
        "options": [
            'open("f.txt", "r")',
            'open("f.txt", "r", encoding="utf-8")',
            'open("f.txt", "rb")',
            'read_file("f.txt")',
        ],
        "answer": 1,
        "why": "برای متن فارسی حتماً `encoding=\"utf-8\"` را بنویس.",
    },
]

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def main() -> int:
    # اگر خروجی در ترمینال واقعی نبود، رنگ‌ها را خاموش کن
    use_color = sys.stdout.isatty() and (
        os.name != "nt" or "WT_SESSION" in os.environ or "ANSICON" in os.environ
    )

    def c(color: str, text: str) -> str:
        return f"{color}{text}{RESET}" if use_color else text

    print("=" * 60)
    print("  آزمون سریع پایتون — ۲۰ سوال")
    print("=" * 60)
    print("  برای هر سوال یکی از حروف‌های a/b/c/d را وارد کن (یا شماره).\n")

    score = 0
    wrong_questions = []

    for i, item in enumerate(QUESTIONS, start=1):
        print(c(CYAN, f"سوال {i}:") + f" {item['q']}")
        for j, opt in enumerate(item["options"]):
            print(f"   {chr(97 + j)}) {opt}")

        while True:
            raw = input("پاسخ: ").strip().lower()
            if raw in "abcd" and len(raw) == 1:
                choice = "abcd".index(raw)
                break
            if raw.isdigit() and 1 <= int(raw) <= len(item["options"]):
                choice = int(raw) - 1
                break
            print(c(YELLOW, "  ورودی نامعتبر — دوباره تلاش کن."))

        if choice == item["answer"]:
            score += 1
            print(c(GREEN, "  ✓ درست\n"))
        else:
            wrong_questions.append((i, item))
            correct = chr(97 + item["answer"])
            print(c(RED, f"  ✗ نادرست. پاسخ درست: {correct}) {item['options'][item['answer']]}"))
            print(c(YELLOW, f"    💡 {item['why']}\n"))

    total = len(QUESTIONS)
    percent = round(score / total * 100)

    print("=" * 60)
    if percent >= 90:
        grade = "عالی! 🎉 آماده‌ی مسیر تخصصی هستی."
    elif percent >= 70:
        grade = "خوب 👍 فقط مرور کن و ادامه بده."
    else:
        grade = "نیاز به مرور داری — درس‌های ۱ تا ۴ را دوباره بخوان."
    print(f"  نمره: {score} از {total}  ({percent}٪)")
    print(f"  نتیجه: {grade}")

    if wrong_questions:
        print("\n  سوال‌هایی که اشتباه زدی:")
        for num, item in wrong_questions:
            print(f"   - سوال {num}: {item['q'].splitlines()[0]}")

    print("=" * 60)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\n  آزمون لغو شد. هر وقت خواستی دوباره اجرا کن.")
        sys.exit(0)
