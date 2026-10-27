"""
تست ترمیم‌پذیری — مطمئن شویم شکستِ بارگذاری موتور، دکمه‌ها را نمی‌کُشد.

این تست بازتولیدکننده‌ی یک باگ واقعی است: اگر barگذاری Pyodide شکست می‌خورد،
`loading` ریست نمی‌شد، ضربه‌ی بعدی `window.__PYODIDE_READY__` (که همیشه null
بود) را برمی‌گرداند، `.then` روی null یک TypeError همزمان می‌داد که از
زنجیره‌ی .catch رد می‌شد → `is-busy` برای همیشه می‌ماند و با
`pointer-events: none` دکمه‌ها برای همیشه از کار می‌افتادند.

اجرا:  python tests\\_test_recovery.py
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright  # noqa: E402

TARGET = ROOT / "dist" / "PythonTerminal-offline.html"
if not TARGET.exists():
    print("❌ نسخه‌ی آفلاین ساخته نشده. اول: python build_html.py")
    sys.exit(1)

URL = TARGET.as_uri()
problems: list[str] = []


def check(condition: bool, message: str) -> None:
    print(("  ✓ " if condition else "  ✗ ") + message)
    if not condition:
        problems.append(message)


# وضعیت دکمه‌ها و پیام‌ها
SNAP = """() => {
  const r = document.getElementById('btnRun');
  const c = document.getElementById('btnCheck');
  const t = document.getElementById('toast');
  return {
    busy: r.classList.contains('is-busy') || c.classList.contains('is-busy'),
    pe: getComputedStyle(r).pointerEvents,
    toast: t && !t.hidden ? t.textContent : '',
    stdout: document.getElementById('stdout').textContent
  };
}"""


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
        )

        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on(
            "console",
            lambda m: errors.append(m.text) if m.type == "error" else None,
        )

        # هیچ درخواست اینترنتی نباید برود
        page.route(
            "**/*",
            lambda route: (
                route.abort()
                if route.request.url.startswith("http")
                and "127.0.0.1" not in route.request.url
                else route.continue_()
            ),
        )

        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(1500)

        # ── شکست عمدی بارگذاری موتور (مثل کمبود حافظه‌ی گوشی) ──
        print("۱) شکست اولین بارگذاری")
        page.evaluate(
            """() => {
              const real = globalThis.loadPyodide;
              let calls = 0;
              window.loadPyodide = function () {
                calls++;
                if (calls === 1) {
                  return Promise.reject(new Error("out of memory"));
                }
                return real.apply(this, arguments);
              };
            }"""
        )

        page.evaluate(
            """() => {
              document.getElementById('code').value = "print('RECOVER')";
              window.__pycourse.runCode('run');
            }"""
        )
        time.sleep(2)
        s = page.evaluate(SNAP)
        check(s["busy"] is False, "بعد از شکست، is-busy برداشته شد")
        check(s["pe"] == "auto", "بعد از شکست، دکمه دوباره قابل کلیک شد")
        check(
            "شکست" in s["toast"] or "ناموفق" in s["toast"],
            f"پیام فارسیِ شکست نمایش داده شد ({s['toast'][:40]})",
        )

        # ── ضربه‌ی دوم نباید TypeError همزمان بدهد ──
        print("\n۲) ضربه‌ی دوم (قبلاً TypeError همزمان می‌داد)")
        threw = page.evaluate(
            """() => {
              try { window.__pycourse.runCode('run'); return null; }
              catch (e) { return String(e); }
            }"""
        )
        check(threw is None, f"بدون خطای همزمان ({threw})")

        # ── باید بارگذاری شود و کد اجرا شود ──
        print("\n۳) تلاش مجدد")
        out = ""
        for _ in range(60):
            time.sleep(1)
            out = page.evaluate(
                "() => document.getElementById('stdout').textContent"
            )
            if "RECOVER" in out:
                break
        check("RECOVER" in out, f"کد بعد از تلاش مجدد اجرا شد ({out.strip()[:30]!r})")

        s = page.evaluate(SNAP)
        check(s["busy"] is False, "دکمه‌ها بعد از موفقیت آزادند")
        check(s["pe"] == "auto", "pointer-events دوباره auto است")

        # ── دکمه‌ی فیزیکی باید واقعاً کلیک شود ──
        print("\n۴) کلیک واقعی روی دکمه")
        try:
            page.click("#btnRun", timeout=4000)
            check(True, "کلیک روی «اجرا» رفت")
        except Exception as exc:  # noqa: BLE001
            check(False, f"کلیک روی «اجرا» نرفت: {str(exc)[:80]}")
        time.sleep(3)
        s = page.evaluate(SNAP)
        check(s["busy"] is False, "بعد از کلیک، is-busy برنگشت (گیر نکرد)")

        # ── دو اجرای همزمان نباید خروجی را گم کند ──
        print("\n۵) دو اجرای همزمان (نشت setStdout)")
        page.evaluate(
            """() => {
              document.getElementById('code').value = "print('AAA')";
              window.__pycourse.runCode('run');
              window.__pycourse.runCode('run');
            }"""
        )
        time.sleep(6)
        out = page.evaluate("() => document.getElementById('stdout').textContent")
        check(
            out.strip() in ("AAA", "AAA\nAAA") or out.count("AAA") >= 1,
            f"خروجی گم نشد ({out.strip()!r})",
        )
        check("(بدون خروجی)" not in out, "دیگر «بدون خروجی» جعل نمی‌شود")

        real_errors = [e for e in errors if "favicon" not in e.lower()]
        check(not real_errors, f"بدون خطای جاوااسکریپت ({real_errors[:2]})")

        browser.close()

    print("=" * 62)
    if problems:
        print(f"❌ {len(problems)} مورد مشکل داشت:")
        for item in problems:
            print("   -", item)
        return 1
    print("✅ شکستِ موتور قابل ترمیم است؛ دکمه‌ها هرگز نمی‌میرند")
    return 0


if __name__ == "__main__":
    sys.exit(main())
