"""
تست کامل: هر راه‌حل باید همه‌ی تست‌های تمرین متناظرش را پاس کند.

اجرا:  python tests\\_test_solutions.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pycourse import content, runner, tester  # noqa: E402

EXERCISES = [
    "ex01_basics",
    "ex02_control_flow",
    "ex03_collections",
    "ex04_functions",
    "ex05_files_errors",
    "ex06_oop",
    "ex07_advanced",
]


def main() -> int:
    total_pass = 0
    total_tests = 0
    failed = 0

    for ex_id in EXERCISES:
        ex = content.read_exercise(ex_id)
        sol_path = ROOT / "solutions" / f"{ex_id}_sol.py"
        if not sol_path.exists():
            print(f"✗ {ex_id}: راه‌حل موجود نیست")
            failed += 1
            continue

        user = sol_path.read_text(encoding="utf-8")
        script = tester.build_check_script(user, ex["tests_part"])
        if not script:
            print(f"✗ {ex_id}: اسکریپت ساخته نشد")
            failed += 1
            continue

        res = runner.run_source(script, timeout=25)
        results = tester.parse_results(res["stdout"]) or []
        passed = sum(1 for t in results if t["status"] == "PASS")

        total_pass += passed
        total_tests += len(results)

        status = "✓" if results and passed == len(results) else "✗"
        print(f"{status} {ex_id:<20} {passed}/{len(results)} تست پاس شد")

        for t in results:
            if t["status"] != "PASS":
                print(f"     [{t['status']}] {t['message'][:90]}")
        if res["stderr"].strip():
            print("     STDERR:", res["stderr"].strip()[:200])

    print("=" * 62)
    print(f"مجموع: {total_pass}/{total_tests} تست پاس شد")
    if failed or total_pass != total_tests:
        print("❌ مشکل وجود دارد")
        return 1
    print("✅ همه‌ی راه‌حل‌ها همه‌ی تست‌ها را پاس کردند")
    return 0


if __name__ == "__main__":
    sys.exit(main())
