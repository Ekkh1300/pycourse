"""
تست موبایل — شبیه‌سازی گوشی واقعی با Playwright.

اجرا:  python tests\\_test_mobile.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "_shots"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright  # noqa: E402

BASE = "http://127.0.0.1:8765/"
problems: list[str] = []


def check(condition: bool, message: str) -> None:
    print(("  ✓ " if condition else "  ✗ ") + message)
    if not condition:
        problems.append(message)


def run_device(
    browser,
    name: str,
    viewport: dict,
    is_mobile: bool,
    shot: str,
    expects_mobile_nav: bool = True,
    base: str = BASE,
) -> None:
    print(f"\n═══ {name} @ {base} ═══")
    context = browser.new_context(
        viewport=viewport,
        is_mobile=is_mobile,
        has_touch=is_mobile,
        device_scale_factor=2 if is_mobile else 1,
        user_agent=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            if "iPhone" in name
            else "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
        ),
    )
    page = context.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("dialog", lambda d: d.accept())

    page.goto(base)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(900)

    # ── نباید هیچ خطای اولیه‌ای نمایش داده شود ──
    # (این قبلاً باگ داشت: درس ۰ تمرین first_steps را می‌خواست که در
    #  نسخه‌ی استاتیک پیدا نمی‌شد و یک توست قرمز می‌ماند.)
    check(
        not page.locator("#toast").is_visible(),
        "هیچ توست خطای اولیه‌ای نمایش داده نشده",
    )

    # ── چیدمان ──
    check(page.locator("#sidebar").is_visible(), "فهرست قابل دسترسی است")
    check(page.locator("#fileName").is_visible(), "نوار ابزار کد دیده می‌شود")

    layout = page.evaluate(
        """() => {
            const nav = document.getElementById('mobileNav').getBoundingClientRect();
            const code = document.getElementById('paneCode').getBoundingClientRect();
            const btn = document.querySelector('.mobilenav__btn[data-view="code"]');
            const r = btn.getBoundingClientRect();
            const side = document.getElementById('sidebar').getBoundingClientRect();
            return {
                navH: nav.height,
                codeWidth: code.width,
                codeTop: code.top,
                sideRight: Math.round(side.right),
                btnH: r.height,
                vw: window.innerWidth,
                overflowX: document.documentElement.scrollWidth > window.innerWidth,
            };
        }"""
    )
    check(not layout["overflowX"], "اسکرول افقی ندارد")
    check(layout["codeWidth"] <= layout["vw"], "پنل کد از عرض صفحه بیرون نمی‌زند")
    if expects_mobile_nav:
        check(
            layout["sideRight"] <= 0,
            f"کشوی فهرست در حالت عادی کاملاً پنهان است (لبه: {layout['sideRight']}px)",
        )

    if expects_mobile_nav:
        # ── چیدمان موبایل: نوار ناوبری پایین + تک‌پنل ──
        check(layout["navH"] > 0, "نوار ناوبری پایین دیده می‌شود")
        check(layout["btnH"] >= 44, f"هدف لمسی ناوبری ≥۴۴ پیکسل ({layout['btnH']:.0f})")

        page.click('.mobilenav__btn[data-view="doc"]')
        page.wait_for_timeout(400)
        check(page.locator("#paneDoc").is_visible(), "تب جزوه باز می‌شود")
        check(not page.locator("#paneCode").is_visible(), "تب کد پنهان می‌شود")
        page.screenshot(path=str(SHOTS / (shot + "-doc.png")))

        page.click('.mobilenav__btn[data-view="menu"]')
        page.wait_for_timeout(450)
        check(page.locator("#sidebar").is_visible(), "کشوی فهرست باز می‌شود")
        check(page.locator(".navitem").count() > 10, "فهرست پر است")
        page.screenshot(path=str(SHOTS / (shot + "-menu.png")))

        page.click('.mobilenav__btn[data-view="code"]')
        page.wait_for_timeout(400)
        check(page.locator("#paneCode").is_visible(), "تب کد برمی‌گردد")
    else:
        # ── چیدمان تبلت: سه بخش روی‌هم (فهرست بالا، کد، جزوه) ──
        check(layout["navH"] == 0, "نوار ناوبری موبایل در عرض تبلت پنهان است")
        stacked = page.evaluate(
            """() => {
                const s = document.getElementById('sidebar').getBoundingClientRect();
                const c = document.getElementById('paneCode').getBoundingClientRect();
                const d = document.getElementById('paneDoc').getBoundingClientRect();
                return { stackOk: s.bottom <= c.top + 1 && c.bottom <= d.top + 1,
                         sideH: s.height, codeH: c.height, docH: d.height };
            }"""
        )
        check(stacked["stackOk"], "چیدمان روی‌همی فهرست/کد/جزوه درست است")
        check(stacked["codeH"] >= 220, f"پنل کد ارتفاع کافی دارد ({stacked['codeH']:.0f}px)")
        check(stacked["docH"] >= 220, f"پنل جزوه ارتفاع کافی دارد ({stacked['docH']:.0f}px)")
        page.screenshot(path=str(SHOTS / (shot + "-stack.png")))

    # ── لمس در ویرایشگر ──
    page.click("#navExercises li:nth-child(1) button")
    page.wait_for_timeout(800)
    check(page.locator("#gutter .gl").count() > 10, "شماره‌ی خط‌ها هست")

    # فوکوس روی textarea: مستقیماً روی خود textarea لمس/کلیک می‌کنیم
    editor = page.locator("#code")
    editor.scroll_into_view_if_needed()
    page.wait_for_timeout(250)
    eb = editor.bounding_box()
    if eb and is_mobile:
        page.touchscreen.tap(eb["x"] + eb["width"] / 2, eb["y"] + min(60, eb["height"] / 2))
    else:
        editor.click()
    page.wait_for_timeout(300)

    focused = page.evaluate("document.activeElement ? document.activeElement.id : ''")
    check(focused == "code", f"ویرایشگر فوکوس شد (فعال: {focused or 'هیچ'})")

    before = page.evaluate("document.getElementById('code').value.length")
    page.keyboard.type("x = 1\n")
    page.wait_for_timeout(300)
    after = page.evaluate("document.getElementById('code').value.length")
    check(after > before, "تایپ کردن در ویرایشگر کار می‌کند")

    # ── اجرا ──
    page.click("#btnRun")
    try:
        page.wait_for_function(
            "() => document.getElementById('stdout').textContent.length > 0", timeout=30000
        )
        check(True, "اجرای کد کار می‌کند")
    except Exception:
        check(False, "اجرای کد کار نکرد")
    page.screenshot(path=str(SHOTS / (shot + "-code.png")))

    # ── کنسول قابل استفاده ──
    box = page.evaluate(
        """() => {
            const c = document.getElementById('console').getBoundingClientRect();
            const t = document.getElementById('tabOutput').getBoundingClientRect();
            return { ch: c.height, th: t.height, w: c.width };
        }"""
    )
    check(box["ch"] >= 100, f"ارتفاع کنسول مناسب است ({box['ch']:.0f}px)")

    real_errors = [e for e in errors if "favicon" not in e.lower()]
    check(not real_errors, f"بدون خطای جاوااسکریپت ({real_errors[:2]})")

    context.close()


def main() -> int:
    # هدف‌ها: سرور محلی + هر دو فایلی که روی گوشی می‌روند
    html_online = (ROOT / "dist" / "PythonTerminal.html").resolve()
    html_offline = (ROOT / "dist" / "PythonTerminal-offline.html").resolve()

    targets: list[tuple[str, str, str]] = [("سرور", BASE, "srv")]
    if html_online.exists():
        targets.append(("HTML آنلاین", html_online.as_uri(), "on"))
    if html_offline.exists():
        targets.append(("HTML آفلاین", html_offline.as_uri(), "off"))

    devices = [
        ("iPhone 13", {"width": 390, "height": 844}, True, True),
        ("Pixel 7", {"width": 412, "height": 915}, True, True),
        # عرض تبلت → چیدمان سه‌بخشی روی‌هم (ناوبری موبایل پنهان)
        ("iPad", {"width": 820, "height": 1180}, True, False),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for target_name, base, tag in targets:
            print("\n" + "▓" * 62)
            print(f"  هدف: {target_name}")
            print("▓" * 62)
            for device_name, viewport, is_mobile, mobile_nav in devices:
                run_device(
                    browser,
                    device_name,
                    viewport,
                    is_mobile,
                    shot=f"{tag}-{device_name.split()[0].lower()}",
                    expects_mobile_nav=mobile_nav,
                    base=base,
                )

        browser.close()

    print("=" * 62)
    if problems:
        print(f"❌ {len(problems)} مورد مشکل داشت:")
        for item in problems:
            print("   -", item)
        return 1
    print("✅ موبایل روی همه‌ی اهداف کامل کار می‌کند")
    return 0


if __name__ == "__main__":
    sys.exit(main())
