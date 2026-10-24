"""
تست رابط کاربری با Playwright.

اجرا:  python tests\\_test_ui.py
خروجی: تصویرها در پوشه‌ی _shots/
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "_shots"
SHOTS.mkdir(exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright  # noqa: E402

BASE = "http://127.0.0.1:8765/"
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

        print("۱) بارگذاری اولیه")
        page.goto(BASE)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(500)

        check(page.locator("#app").is_visible(), "رابط اصلی نمایش داده شد")
        check(page.locator("#boot").is_hidden(), "صفحه‌ی بوت پنهان شد")
        check(page.locator("#navLessons li").count() == 8, "۸ درس در نوار کناری")
        check(page.locator("#navExercises li").count() == 7, "۷ تمرین در نوار کناری")
        check(page.locator("#docBody .doc p").count() > 2, "محتوای جزوه رندر شد")
        check(page.locator("#docTitle").inner_text().strip() != "", "عنوان سند در نوار بالا هست")
        check(page.locator("#docBody pre").count() > 0, "بلوک‌های کد مارک‌داون رندر شدند")
        page.screenshot(path=str(SHOTS / "01-lesson.png"))

        print("\n۱-ب) درسی که جدول و فهرست دارد")
        page.click("#navLessons li:nth-child(2) button")
        page.wait_for_timeout(700)
        check(page.locator("#docBody table").count() > 0, "جدول‌های مارک‌داون رندر شدند")
        check(page.locator("#docBody ul li").count() > 0, "فهرست‌ها رندر شدند")
        check(page.locator("#docBody blockquote").count() > 0, "نقل‌قول‌ها رندر شدند")
        page.screenshot(path=str(SHOTS / "01b-lesson2.png"))
        page.click("#navLessons li:nth-child(1) button")
        page.wait_for_timeout(600)

        print("\n۲) اجرای کدی با خطا")
        page.click("#navExercises li:nth-child(1) button")
        page.wait_for_timeout(800)
        check(
            page.locator("#fileName").inner_text() == "ex01_basics.py",
            "فایل تمرین بارگذاری شد",
        )
        check(page.locator("#gutter .gl").count() > 10, "شماره‌ی خط‌ها ساخته شد")

        page.click("#code")
        page.keyboard.press("Control+Home")
        page.keyboard.type("print(nam)\n")
        page.click("#btnRun")
        page.wait_for_selector("#diag .card__title", timeout=20000)
        page.wait_for_selector("#gutter .gl.is-error", timeout=20000)

        check(page.locator("#stMode").inner_text() == "NameError", "نوار وضعیت NameError را نشان داد")
        diag_text = page.locator("#diag").inner_text()
        check("متغیر تعریف نشده" in diag_text, "کارت خطای فارسی نمایش داده شد")
        check("چه شد؟" in diag_text and "چرا؟" in diag_text, "بخش‌های «چه شد/چرا» پر شدند")
        check("چه کنم؟" in diag_text, "بخش «چه کنم» پر شد")
        check(page.locator("#gutter .gl.is-error").count() == 1, "خطا روی شماره‌ی خط علامت خورد")
        check(
            page.locator("#highlightCode .hl-line-error").count() == 1,
            "خط کد در ویرایشگر قرمز شد",
        )
        page.screenshot(path=str(SHOTS / "02-error.png"))

        print("\n۳) اجرای کد درست")
        page.click("#btnReset")
        page.wait_for_timeout(500)
        page.click("#code")
        page.keyboard.press("Control+End")
        page.keyboard.type('\nprint("سلام")\n')
        page.click("#btnRun")
        page.wait_for_function(
            "() => document.getElementById('stdout').textContent.includes('سلام')",
            timeout=20000,
        )
        check("سلام" in page.locator("#stdout").inner_text(), "خروجی استاندارد چاپ شد")
        check(page.locator("#stMode").inner_text() == "NORMAL", "نوار وضعیت به حالت عادی برگشت")
        page.screenshot(path=str(SHOTS / "03-run.png"))

        print("\n۴) بررسی با تست‌ها")
        page.click("#btnCheck")
        page.wait_for_selector("#tests .testlist li", timeout=30000)
        tests_text = page.locator("#tests").inner_text()
        check("تست" in tests_text, "نتایج تست نمایش داده شد")
        check(page.locator("#tests .testlist li").count() > 5, "تک‌تک تست‌ها فهرست شدند")
        check(page.locator("#stTests").inner_text() != "—", "شمارنده‌ی تست در نوار وضعیت پر شد")
        page.screenshot(path=str(SHOTS / "04-tests.png"))

        print("\n۵) راهنمای مرحله‌ای")
        page.click("#btnHint")
        page.wait_for_selector("#briefExtra .hintlist li", timeout=10000)
        check(page.locator("#briefExtra .hintlist li").count() >= 1, "راهنمای مرحله‌ای نمایش داده شد")
        page.screenshot(path=str(SHOTS / "05-hint.png"))

        print("\n۶) حالت دو‌ستونه: جزوه راست، کد چپ")
        boxes = page.evaluate(
            """() => {
                const code = document.getElementById('paneCode').getBoundingClientRect();
                const doc = document.getElementById('paneDoc').getBoundingClientRect();
                return { codeLeft: code.left, docLeft: doc.left, vw: window.innerWidth };
            }"""
        )
        check(
            boxes["codeLeft"] < boxes["docLeft"] and boxes["docLeft"] > boxes["vw"] * 0.5,
            f"کد سمت چپ ({boxes['codeLeft']:.0f}) و جزوه سمت راست ({boxes['docLeft']:.0f})",
        )

        print("\n۷) پالت دستورها")
        page.keyboard.press("Control+k")
        page.wait_for_selector("#palette:not([hidden])", timeout=5000)
        check(page.locator("#palette").is_visible(), "پالت باز شد")
        page.fill("#paletteInput", "پوسته")
        page.wait_for_timeout(300)
        check(page.locator("#paletteList li").count() >= 1, "فیلتر دستورها کار کرد")
        page.screenshot(path=str(SHOTS / "06-palette.png"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.locator("#palette").is_hidden(), "پالت با Escape بسته شد")

        print("\n۸) تغییر پوسته")
        page.click("#btnTheme")
        page.wait_for_timeout(400)
        theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
        check(theme == "crt", "پوسته‌ی سبز CRT فعال شد")
        page.screenshot(path=str(SHOTS / "07-crt.png"))
        page.click("#btnTheme")
        page.wait_for_timeout(300)

        print("\n۹) بستن پنل جزوه")
        page.keyboard.press("Control+d")
        page.wait_for_timeout(400)
        check(page.locator("#paneDoc").is_hidden(), "پنل جزوه بسته شد")
        page.keyboard.press("Control+d")
        page.wait_for_timeout(400)
        check(page.locator("#paneDoc").is_visible(), "پنل جزوه باز شد")

        print("\n۱۰) آزمون سریع")
        page.click("#navQuiz")
        page.wait_for_selector(".quiz__q", timeout=10000)
        check(page.locator(".quiz__q").count() == 20, "۲۰ سؤال آزمون نمایش داده شد")
        page.locator(".quiz__q").first.locator(".quiz__opt").first.click()
        page.screenshot(path=str(SHOTS / "08-quiz.png"))

        print("\n۱۱) جست‌وجو")
        page.fill("#searchInput", "حلقه")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        check("نتایج" in page.locator("#docTitle").inner_text(), "جست‌وجو نتیجه داد")

        print("\n۱۲) وضعیت پایانی")
        page.click("#navLessons li:nth-child(3) button")
        page.wait_for_timeout(800)
        page.screenshot(path=str(SHOTS / "09-lesson3.png"))

        real_errors = [e for e in errors if "favicon" not in e.lower()]
        check(not real_errors, f"بدون خطای جاوااسکریپت ({real_errors[:2]})")

        browser.close()

    print("=" * 62)
    if problems:
        print(f"❌ {len(problems)} مورد مشکل داشت:")
        for item in problems:
            print("   -", item)
        return 1
    print("✅ همه‌ی بررسی‌های رابط کاربری موفق بود")
    return 0


if __name__ == "__main__":
    sys.exit(main())
