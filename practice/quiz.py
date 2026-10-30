"""
Python Course — Practice Quiz
===============================================
Run: python practice/quiz.py

A multiple-choice quiz to test your Python knowledge.
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

QUESTIONS = [
    {
        "q": "What is the result of `5 / 2`?",
        "options": ["2", "2.5", "2.0", "Undefined"],
        "answer": 1,
        "why": "`/` always returns a float in Python. `5 / 2` → `2.5`. "
                "Use `//` for floor division (integer division).",
    },
    {
        "q": "What does `bool(\"False\")` return?",
        "options": ["False", "True", "Undefined", "None"],
        "answer": 1,
        "why": "Any non-empty string is truthy in Python, including \"False\". "
                "Only empty string `\"\"` evaluates to `False`.",
    },
    {
        "q": "Which of the following is the correct way to define a function?",
        "options": [
            "def my_func(): ...",
            "function my_func(): ...",
            "def my_func { ... }",
            "func my_func(): ...",
        ],
        "answer": 0,
        "why": "Python uses the `def` keyword to define functions.",
    },
    {
        "q": "What is the output of `print(10 // 3)`?",
        "options": ["3", "3.33", "3.0", "Error"],
        "answer": 0,
        "why": "`//` is floor division, which returns the integer part: `10 // 3` → `3`.",
    },
    {
        "q": "How do you create a list with items 1, 2, 3?",
        "options": ["list(1, 2, 3)", "[1, 2, 3]", "(1, 2, 3)", "{1, 2, 3}"],
        "answer": 1,
        "why": "Square brackets `[]` create a list in Python.",
    },
    {
        "q": "What does the following code output?\n\n```python\nx = 5\nif x > 3:\n    print(\"A\")\nelif x > 10:\n    print(\"B\")\nelse:\n    print(\"C\")\n```",
        "options": ["A", "B", "C", "Nothing"],
        "answer": 0,
        "why": "Since `x = 5` and `5 > 3` is True, the first branch prints \"A\". "
                "`elif` and `else` are skipped.",
    },
    {
        "q": "Which method adds an item to the END of a list?",
        "options": ["append()", "insert()", "push()", "add()"],
        "answer": 0,
        "why": "`list.append(x)` adds `x` to the end of the list. "
                "`list.insert(i, x)` adds at position `i`.",
    },
    {
        "q": "What is the result of `fruits[::-1]` where `fruits = [\"apple\", \"banana\", \"cherry\"]`?",
        "options": ["[\"apple\", \"banana\", \"cherry\"]", "[\"cherry\", \"banana\", \"apple\"]", "[\"banana\", \"apple\", \"cherry\"]", "Error"],
        "answer": 1,
        "why": "`[::-1]` is a slice that reverses the list.",
    },
    {
        "q": "What does `dict.get(key)` return if the key doesn't exist?",
        "options": ["KeyError", "None", "0", "Undefined"],
        "answer": 1,
        "why": "`dict.get(key)` returns `None` by default if key is missing, "
                "unlike `dict[key]` which raises `KeyError`.",
    },
    {
        "q": "Which of the following creates a set (not a list)?",
        "options": ["[1, 2, 3]", "{1, 2, 3}", "(1, 2, 3)", "<1, 2, 3>"],
        "answer": 1,
        "why": "Curly braces `{1, 2, 3}` create a set. Square brackets create a list.",
    },
    {
        "q": "What is the output of `sum(range(5))`?",
        "options": ["0", "5", "10", "15"],
        "answer": 2,
        "why": "`range(5)` produces 0, 1, 2, 3, 4. Their sum is 0+1+2+3+4 = 10.",
    },
    {
        "q": "Which keyword is used to import a specific function from a module?",
        "options": ["import", "from ... import", "include", "require"],
        "answer": 1,
        "why": "Python uses `from module import function` to import specific functions.",
    },
    {
        "q": "What does `len(\"hello\")` return?",
        "options": ["4", "5", "6", "Error"],
        "answer": 1,
        "why": "`len()` returns the number of items. A string of 5 characters returns 5.",
    },
]

# ─────────────────────────────────────────────────────────────
# Persian version of the same bank (same answer indices)
# ─────────────────────────────────────────────────────────────

QUESTIONS_FA = [
    {
        "q": "نتیجهٔ `5 / 2` چیست؟",
        "options": ["2", "2.5", "2.0", "نامشخص"],
        "answer": 1,
        "why": "`/` در پایتون همیشه عدد اعشاری برمی‌گرداند. `5 / 2` → `2.5`. "
               "برای تقسیم صحیح از `//` استفاده کن.",
    },
    {
        "q": "`bool(\"False\")` چه چیزی برمی‌گرداند؟",
        "options": ["False", "True", "نامشخص", "None"],
        "answer": 1,
        "why": "در پایتون هر رشتهٔ خالی‌نشده درست (truthy) است، حتی \"False\". "
               "فقط رشتهٔ خالی `\"\"` برابر `False` می‌شود.",
    },
    {
        "q": "کدام‌یک روش درست تعریف تابع است؟",
        "options": [
            "def my_func(): ...",
            "function my_func(): ...",
            "def my_func { ... }",
            "func my_func(): ...",
        ],
        "answer": 0,
        "why": "پایتون برای تعریف تابع از کلیدواژهٔ `def` استفاده می‌کند.",
    },
    {
        "q": "خروجی `print(10 // 3)` چیست؟",
        "options": ["3", "3.33", "3.0", "خطا"],
        "answer": 0,
        "why": "`//` تقسیم صحیح است و بخش صحیح را برمی‌گرداند: `10 // 3` → `3`.",
    },
    {
        "q": "چطور لیستی با اعضای ۱، ۲، ۳ می‌سازی؟",
        "options": ["list(1, 2, 3)", "[1, 2, 3]", "(1, 2, 3)", "{1, 2, 3}"],
        "answer": 1,
        "why": "در پایتون آرایهٔ مربعی `[]` یک لیست می‌سازد.",
    },
    {
        "q": "خروجی این کد چیست؟\n\n```python\nx = 5\nif x > 3:\n    print(\"A\")\nelif x > 10:\n    print(\"B\")\nelse:\n    print(\"C\")\n```",
        "options": ["A", "B", "C", "هیچ‌چیز"],
        "answer": 0,
        "why": "چون `x = 5` و `5 > 3` درست است، شاخهٔ اول `A` را چاپ می‌کند. "
               "`elif` و `else` اجرا نمی‌شوند.",
    },
    {
        "q": "کدام متد آیتم را به **انتهای** لیست اضافه می‌کند؟",
        "options": ["append()", "insert()", "push()", "add()"],
        "answer": 0,
        "why": "`list.append(x)` مقدار `x` را به انتهای لیست می‌افزاید. "
               "`list.insert(i, x)` در موقعیت `i` درج می‌کند.",
    },
    {
        "q": "نتیجهٔ `fruits[::-1]` چیست، اگر `fruits = [\"apple\", \"banana\", \"cherry\"]` باشد؟",
        "options": ["[\"سیب\", \"موز\", \"گیلاس\"]", "[\"گیلاس\", \"موز\", \"سیب\"]", "[\"موز\", \"سیب\", \"گیلاس\"]", "خطا"],
        "answer": 1,
        "why": "`[::-1]` یک برش (slice) است که لیست را معکوس می‌کند.",
    },
    {
        "q": "اگر کلید موجود نباشد، `dict.get(key)` چه چیزی برمی‌گرداند؟",
        "options": ["KeyError", "None", "0", "نامشخص"],
        "answer": 1,
        "why": "`dict.get(key)` اگر کلید موجود نباشد به‌طور پیش‌فرض `None` برمی‌گرداند، "
               "برخلاف `dict[key]` که `KeyError` می‌دهد.",
    },
    {
        "q": "کدام‌یک یک ست (set) می‌سازد (نه لیست)؟",
        "options": ["[1, 2, 3]", "{1, 2, 3}", "(1, 2, 3)", "<1, 2, 3>"],
        "answer": 1,
        "why": "آرایهٔ آکولاد `{1, 2, 3}` یک ست می‌سازد. آرایهٔ مربعی لیست می‌سازد.",
    },
    {
        "q": "خروجی `sum(range(5))` چیست؟",
        "options": ["0", "5", "10", "15"],
        "answer": 2,
        "why": "`range(5)` اعداد ۰، ۱، ۲، ۳، ۴ را تولید می‌کند. جمعشان ۰+۱+۲+۳+۴ = ۱۰ است.",
    },
    {
        "q": "برای وارد کردن یک تابع مشخص از یک ماژول از کدام کلیدواژه استفاده می‌شود؟",
        "options": ["import", "from ... import", "include", "require"],
        "answer": 1,
        "why": "پایتون برای وارد کردن توابع مشخص از `from module import function` استفاده می‌کند.",
    },
    {
        "q": "`len(\"hello\")` چه چیزی برمی‌گرداند؟",
        "options": ["4", "5", "6", "خطا"],
        "answer": 1,
        "why": "`len()` تعداد اعضا را برمی‌گرداند. رشتهٔ ۵ حرفی مقدار ۵ می‌دهد.",
    },
]


# ═════════════════════════════════════════════════════════════
#  Run the quiz
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Python Practice Quiz")
    print("=" * 40)
    print(f"Total questions: {len(QUESTIONS)}")
    print()

    score = 0
    for i, q in enumerate(QUESTIONS):
        print(f"Q{i+1}. {q['q']}")
        for j, opt in enumerate(q["options"]):
            print(f"   {j}) {opt}")
        print()

        while True:
            try:
                choice = int(input("Your answer (number): "))
                if 0 <= choice < len(q["options"]):
                    break
                print(f"Please enter 0-{len(q['options']) - 1}.")
            except ValueError:
                print("Please enter a number.")

        if choice == q["answer"]:
            print("✅ Correct!")
            score += 1
        else:
            correct_opt = q["options"][q["answer"]]
            print(f"❌ Wrong. The correct answer was: {q['answer']}) {correct_opt}")
        print(f"   Why: {q['why']}")
        print()

    print("=" * 40)
    print(f"Your score: {score}/{len(QUESTIONS)}")
    percentage = (score / len(QUESTIONS)) * 100
    print(f"Percentage: {percentage:.1f}%")
    if percentage >= 80:
        print("🎉 Excellent!")
    elif percentage >= 60:
        print("👍 Good job!")
    else:
        print("Keep practicing! You'll get there.")