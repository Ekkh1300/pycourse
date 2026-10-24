"""
تست سریع موتور تشخیص خطا.

اجرا:  python tests\\_test_diag.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pycourse import errors_fa  # noqa: E402

NL = "\n"

CASES = [
    (
        "NameError",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 3, in <module>' + NL
        + "    print(nam)" + NL
        + "NameError: name 'nam' is not defined",
    ),
    (
        "NameError با پیشنهاد",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 3, in <module>' + NL
        + "    print(nme)" + NL
        + "NameError: name 'nme' is not defined. Did you mean: 'name'?",
    ),
    (
        "ValueError",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 2, in <module>' + NL
        + '    x = int("abc")' + NL
        + "ValueError: invalid literal for int() with base 10: 'abc'",
    ),
    (
        "SyntaxError",
        '  File "x.py", line 4' + NL
        + "    if x > 1" + NL
        + "         ^" + NL
        + "SyntaxError: invalid syntax",
    ),
    (
        "ZeroDivisionError",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 5, in <module>' + NL
        + "    print(1/0)" + NL
        + "ZeroDivisionError: division by zero",
    ),
    (
        "AttributeError",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 7, in f' + NL
        + "    x.append(3)" + NL
        + "AttributeError: 'int' object has no attribute 'append'",
    ),
    (
        "TypeError-concat",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 2, in <module>' + NL
        + '    x = "5" + 5' + NL
        + 'TypeError: can only concatenate str (not "int") to str',
    ),
    (
        "IndentationError",
        '  File "x.py", line 3' + NL
        + "    if True:" + NL
        + "    print(1)" + NL
        + "IndentationError: expected an indented block",
    ),
    (
        "ModuleNotFoundError",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 1, in <module>' + NL
        + "    import requests" + NL
        + "ModuleNotFoundError: No module named 'requests'",
    ),
    (
        "KeyError",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 2, in <module>' + NL
        + "    d['k']" + NL
        + "KeyError: 'k'",
    ),
    (
        "IndexError",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 2, in <module>' + NL
        + "    x[9]" + NL
        + "IndexError: list index out of range",
    ),
    (
        "Unknown",
        "Traceback (most recent call last):" + NL
        + '  File "x.py", line 2, in <module>' + NL
        + "    boom()" + NL
        + "RuntimeError: چیزی عجیب",
    ),
]


def main() -> int:
    failures = 0
    for label, tb in CASES:
        d = errors_fa.diagnose(tb)
        if d is None:
            print(f"✗ {label}: هیچ تشخیصی برنگشت")
            failures += 1
            continue
        ok = bool(d.title and d.what and d.why and d.fix)
        if not ok:
            failures += 1
        print(
            f"{'✓' if ok else '✗'} {label:<26} → {d.kind:<20} خط {d.line}  |  {d.title}"
        )
        print(f"    چه شد: {d.what[:74]}")
        print(f"    چرا  : {d.why[:74]}")
        print(f"    راه  : {d.fix[0][:74] if d.fix else '—'}")
        print()

    print("=" * 62)
    if failures:
        print(f"{failures} مورد ناقص بود.")
        return 1
    print("همه‌ی تشخیص‌ها کامل بودند.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
