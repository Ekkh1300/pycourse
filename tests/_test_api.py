"""
تست APIهای سرور.

اجرا:  python tests\\_test_api.py
(سرور باید در حال اجرا باشد: python app.py)
"""

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = "http://127.0.0.1:8765"

problems: list[str] = []


def get(path: str):
    with urllib.request.urlopen(BASE + path, timeout=20) as res:
        return json.loads(res.read().decode("utf-8"))


def post(path: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def check(condition: bool, message: str) -> None:
    print(("  ✓ " if condition else "  ✗ ") + message)
    if not condition:
        problems.append(message)


def main() -> int:
    print("۱) سلامت و فهرست دوره")
    health = get("/api/health")
    check(health.get("ok") is True, "سرور سالم است")
    cur = get("/api/curriculum")
    check(len(cur["lessons"]) == 8, "۸ درس")
    check(len(cur["exercises"]) == 7, "۷ تمرین")
    check(cur["quiz_count"] == 20, "۲۰ سؤال آزمون")

    print("\n۲) اجرای کد با خطای NameError")
    r = post("/api/run", {"code": "print(nam)\n", "mode": "run"})
    d = r["diagnosis"]
    check(d["kind"] == "NameError", "نوع خطا تشخیص داده شد")
    check(d["line"] == 1, f"شماره‌ی خط درست است ({d['line']})")
    check(d["title"] == "متغیر تعریف نشده", "عنوان فارسی درست است")
    check(len(d["fix"]) >= 2, "راه‌حل‌های پیشنهادی آمدند")

    print("\n۳) بررسی با راه‌حل درست ex01")
    sol = (ROOT / "solutions" / "ex01_basics_sol.py").read_text(encoding="utf-8")
    r = post("/api/run", {"code": sol, "mode": "check", "exercise_id": "ex01_basics"})
    tests = r["tests"]
    passed = sum(1 for t in tests if t["status"] == "PASS")
    check(passed == len(tests) and tests, f"همه‌ی تست‌ها پاس شدند ({passed}/{len(tests)})")

    print("\n۴) بررسی با کد خالی (همه باید ناموفق باشند)")
    r = post("/api/run", {"code": "", "mode": "check", "exercise_id": "ex02_control_flow"})
    tests = r["tests"]
    passed = sum(1 for t in tests if t["status"] == "PASS")
    check(len(tests) > 10, f"تست‌ها جداگانه اجرا شدند ({len(tests)} تست)")
    check(passed == 0, "هیچ‌کدام پاس نشدند")

    print("\n۵) محتوای تمرین")
    ex = get("/api/exercise?id=ex03_collections")
    check(bool(ex["title"]), f"عنوان: {ex['title']}")
    check(len(ex["user_part"].splitlines()) > 40, "بخش کد کاربر جدا شد")
    check(len(ex["tests_part"].splitlines()) > 10, "بخش تست جدا شد")
    check(len(ex["hints"]) == 3, "سه سطح راهنما دارد")

    print("\n۶) راه‌حل قفل است؟")
    s = get("/api/solution?id=ex07_advanced")
    check(s.get("locked") is True, "قبل از ۳ تلاش قفل است")
    check(s.get("needed") == 3, "باید ۳ تلاش لازم باشد")

    print("\n۷) آزمون")
    q = get("/api/quiz_questions")
    check(len(q["questions"]) == 20, "۲۰ سؤال برای مرورگر")
    result = post("/api/quiz", {"answers": [0] * 20})
    check(result["total"] == 20, "نمره‌دهی کار می‌کند")

    print("\n۸) پیشرفت")
    p = get("/api/progress")
    for key in ("lessons_done", "exercises_done", "attempts", "quiz_best", "theme"):
        check(key in p, f"کلید {key} موجود است")

    print("\n" + "=" * 62)
    if problems:
        print(f"❌ {len(problems)} مورد مشکل داشت")
        return 1
    print("✅ همه‌ی تست‌های API موفق بود")
    return 0


if __name__ == "__main__":
    sys.exit(main())
