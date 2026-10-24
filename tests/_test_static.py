"""
تست نسخه‌ی استاتیک (HTML تک‌فایلی) با Playwright.

اجرا:  python tests\\_test_static.py

نیاز: اینترنت برای بارگذاری Pyodide از CDN
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "_shots"
SHOTS.mkdir(exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright  # noqa: E402

STATIC = "file:///" + str(ROOT / "dist" / "PythonTerminal.html").replace("\\", "/")
# اگر فایل در پوشه‌ی release هم هست، همان را تست می‌کنیم
RELEASE_STATIC = "file:///" + str(ROOT / "release" / "PythonTerminal.html").replace("\\", "/")
if (ROOT / "release" / "PythonTerminal.html").exists():
    STATIC = RELEASE_STATIC
problems: list[str] = []


def check(condition: bool, message: str) -> None:
    print(("  ✓ " if condition else "  ✗ ") + message)
    if not condition:
        problems.append(message)


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 950})

        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append("PAGEERROR: " + str(e)))
        page.on(
            "console",
            lambda m: errors.append("CONSOLE: " + m.text) if m.type == "error" else None,
        )
        page.on("dialog", lambda d: d.accept())

        print("۱) بارگذاری نسخه‌ی استاتیک")
        page.goto(STATIC)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1500)

        check(page.locator("#app").is_visible(), "رابط نمایش داده شد")
        check(page.locator("#navLessons li").count() == 8, "۸ درس")
        check(page.locator("#navExercises li").count() == 7, "۷ تمرین")
        check(page.locator("#docBody .doc p").count() > 2, "جزوه رندر شد")
        page.screenshot(path=str(SHOTS / "10-static-lesson.png"))

        print("\n۲) باز کردن تمرین")
        page.click("#navExercises li:nth-child(1) button")
        page.wait_for_timeout(800)
        check(
            page.locator("#fileName").inner_text() == "ex01_basics.py",
            "کد تمرین بارگذاری شد",
        )
        check(page.locator("#gutter .gl").count() > 10, "شماره‌ی خط‌ها ساخته شد")

        print("\n۳) اجرای کد (Pyodide)")
        page.click("#code")
        page.keyboard.press("Control+Home")
        page.keyboard.type("print('سلام دنیا')\n")
        page.click("#btnRun")
        try:
            page.wait_for_function(
                "() => document.getElementById('stdout').textContent.includes('سلام')",
                timeout=120000,
            )
            check(True, "کد در مرورگر اجرا شد")
        except Exception:
            check(False, "کد در مرورگر اجرا نشد")
        check("سلام" in page.locator("#stdout").inner_text(), "خروجی درست بود")
        page.screenshot(path=str(SHOTS / "11-static-run.png"))

        print("\n۴) تشخیص خطا به فارسی")
        page.click("#code")
        page.keyboard.press("Control+Home")
        page.keyboard.type("print(nam)\n")
        page.click("#btnRun")
        try:
            page.wait_for_selector("#diag .card__title", timeout=120000)
            check(True, "کارت خطای فارسی ظاهر شد")
        except Exception:
            check(False, "کارت خطای فارسی ظاهر نشد")
        diag = page.locator("#diag").inner_text()
        check("متغیر تعریف نشده" in diag, "تشخیص فارسی درست است")
        check("چه شد؟" in diag, "بخش «چه شد» هست")
        check("چرا؟" in diag, "بخش «چرا» هست")
        page.screenshot(path=str(SHOTS / "12-static-error.png"))

        print("\n۵) بررسی با تست‌ها")
        page.click("#btnCheck")
        try:
            page.wait_for_selector("#tests .testlist li", timeout=180000)
            check(True, "نتایج تست نمایش داده شد")
        except Exception:
            check(False, "نتایج تست نمایش داده نشد")
        check(page.locator("#tests .testlist li").count() > 5, "تک‌تک تست‌ها فهرست شدند")
        page.screenshot(path=str(SHOTS / "13-static-tests.png"))

        print("\n۶) آزمون و جست‌وجو")
        page.click("#navQuiz")
        page.wait_for_selector(".quiz__q", timeout=15000)
        check(page.locator(".quiz__q").count() == 20, "۲۰ سؤال آزمون")

        page.fill("#searchInput", "حلقه")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        check("نتایج" in page.locator("#docTitle").inner_text(), "جست‌وجو کار کرد")

        print("\n۷) راهنما")
        page.click("#navExercises li:nth-child(2) button")
        page.wait_for_timeout(700)
        page.click("#btnHint")
        page.wait_for_selector("#briefExtra .hintlist li", timeout=10000)
        check(page.locator("#briefExtra .hintlist li").count() >= 1, "راهنما نمایش داده شد")

        real_errors = [
            e
            for e in errors
            if "favicon" not in e.lower() and "cdn.jsdelivr" not in e.lower()
        ]
        check(not real_errors, f"بدون خطای جاوااسکریپت ({real_errors[:2]})")

        browser.close()

    print("=" * 62)
    if problems:
        print(f"❌ {len(problems)} مورد مشکل داشت:")
        for item in problems:
            print("   -", item)
        return 1
    print("✅ نسخه‌ی استاتیک کامل کار می‌کند")
    return 0


if __name__ == "__main__":
    sys.exit(main())
