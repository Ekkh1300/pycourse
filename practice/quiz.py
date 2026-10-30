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