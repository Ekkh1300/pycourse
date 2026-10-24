"""
تست نسخه‌ی آفلاین — با اینترنت کاملاً قطع‌شده.

اجرا:  python tests\\_test_offline.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "_shots"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright  # noqa: E402

TARGET = ROOT / "dist" / "PythonTerminal-offline.html"
if not TARGET.exists():
    print("❌ نسخه‌ی آفلاین ساخته نشده. اول: python build_html.py")
    sys.exit(1)

URL = "file:///" + str(TARGET).replace("\\", "/")
problems: list[str] = []


def check(condition: bool, message: str) -> None:
    print(("  ✓ " if condition else "  ✗ ") + message)
    if not condition:
        problems.append(message)


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 950})

        # ── هر درخواستی به اینترنت کاملاً بلاک می‌شود ──
        blocked: list[str] = []

        def block(route):
            blocked.append(route.request.url)
            route.abort()

        page.route("**/*", lambda route: block(route) if route.request.url.startswith("http") else route.continue_())

        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append("PAGEERROR: " + str(e)))
        page.on("console", lambda m: errors.append("CONSOLE: " + m.text) if m.type == "error" else None)
        page.on("dialog", lambda d: d.accept())

        print("۱) بارگذاری بدون اینترنت")
        page.goto(URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1500)

        check(page.locator("#app").is_visible(), "رابط نمایش داده شد")
        check(page.locator("#navLessons li").count() == 8, "۸ درس")
        check(page.locator("#navExercises li").count() == 7, "۷ تمرین")
        check(page.locator("#docBody .doc p").count() > 2, "جزوه رندر شد")
        check(not blocked, f"هیچ درخواستی به اینترنت رفت ({blocked[:2]})")

        print("\n۲) اجرای کد بدون اینترنت")
        page.click("#navExercises li:nth-child(1) button")
        page.wait_for_timeout(800)
        page.click("#code")
        page.keyboard.press("Control+Home")
        page.keyboard.type("print('سلام دنیا')\n")
        page.click("#btnRun")
        try:
            page.wait_for_function(
                "() => document.getElementById('stdout').textContent.includes('سلام')",
                timeout=180000,
            )
            check(True, "Pyodide بدون اینترنت بالا آمد و کد را اجرا کرد")
        except Exception:
            check(False, "Pyodide بالا نیامد")
        check(not blocked, f"باز هم درخواست اینترنتی نرفت ({blocked[:2]})")
        page.screenshot(path=str(SHOTS / "14-offline-run.png"))

        print("\n۳) تشخیص خطا به فارسی بدون اینترنت")
        page.click("#code")
        page.keyboard.press("Control+Home")
        page.keyboard.type("print(nam)\n")
        page.click("#btnRun")
        try:
            page.wait_for_selector("#diag .card__title", timeout=180000)
            check(True, "کارت خطای فارسی ظاهر شد")
        except Exception:
            check(False, "کارت خطا ظاهر نشد")
        diag = page.locator("#diag").inner_text()
        check("متغیر تعریف نشده" in diag, "تشخیص فارسی درست است")
        check("چه شد؟" in diag and "چرا؟" in diag, "بخش‌های توضیح پر شدند")
        page.screenshot(path=str(SHOTS / "15-offline-error.png"))

        print("\n۴) بررسی با تست‌ها بدون اینترنت")
        page.click("#btnCheck")
        try:
            page.wait_for_selector("#tests .testlist li", timeout=240000)
            check(True, "نتایج تست نمایش داده شد")
        except Exception:
            check(False, "نتایج تست نمایش داده نشد")
        check(page.locator("#tests .testlist li").count() > 5, "تک‌تک تست‌ها فهرست شدند")
        page.screenshot(path=str(SHOTS / "16-offline-tests.png"))

        print("\n۵) آزمون و جست‌وجو")
        page.click("#navQuiz")
        page.wait_for_selector(".quiz__q", timeout=15000)
        check(page.locator(".quiz__q").count() == 20, "۲۰ سؤال آزمون")
        page.fill("#searchInput", "حلقه")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        check("نتایج" in page.locator("#docTitle").inner_text(), "جست‌وجو کار کرد")

        real_errors = [e for e in errors if "favicon" not in e.lower()]
        check(not real_errors, f"بدون خطای جاوااسکریپت ({real_errors[:2]})")
        check(not blocked, f"در کل تست هیچ درخواست اینترنتی نبود ({len(blocked)})")

        browser.close()

    print("=" * 62)
    if problems:
        print(f"❌ {len(problems)} مورد مشکل داشت:")
        for item in problems:
            print("   -", item)
        return 1
    print("✅ نسخه‌ی آفلاین بدون هیچ اینترنتی کامل کار می‌کند")
    return 0


if __name__ == "__main__":
    sys.exit(main())
