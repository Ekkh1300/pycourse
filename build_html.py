"""
ساخت نسخه‌ی وب (HTML) — دو حالت:

  • آنلاین  (پیش‌فرض)  : dist\\PythonTerminal.html         ~۳۰۰ کیلوبایت
  • آفلاین            : dist\\PythonTerminal-offline.html  ~۱۸ مگابایت

اجرا:  python build_html.py [--offline]

نسخه‌ی آفلاین کل Pyodide را داخل خودِ فایل دارد؛ هیچ اینترنتی لازم
نیست و حتی با file:// هم کار می‌کند.
"""

from __future__ import annotations

import base64
import json
import shutil
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
DIST = ROOT / "dist"
VENDOR = ROOT / "vendor" / "pyodide"

PYODIDE_VERSION = "0.26.4"
PYODIDE_CDN = f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/"

# نام فایل‌هایی که باید داخل HTML بروند (نسخه‌ی آفلاین)
OFFLINE_FILES = {
    "loader": "pyodide.js",
    "asm": "pyodide.asm.js",
    "wasm": "pyodide.asm.wasm",
    "stdlib": "python_stdlib.zip",
    "lock": "pyodide-lock.json",
}


# ─────────────────────────────────────────────────────────────
# جمع‌آوری محتوای دوره
# ─────────────────────────────────────────────────────────────


def build_course_data() -> dict:
    sys.path.insert(0, str(ROOT))
    from pycourse import content
    from pycourse import hints as hints_mod

    lessons = []
    for item in content.list_lessons():
        doc = content.read_lesson(item["id"])
        if doc:
            lessons.append({"id": doc["id"], "title": doc["title"], "body": doc["body"]})

    exercises = []
    for item in content.list_exercises():
        doc = content.read_exercise(item["id"])
        if not doc:
            continue
        exercises.append(
            {
                "id": doc["id"],
                "number": item["number"],
                "title": doc["title"],
                "description": doc["description"],
                "user_part": doc["user_part"],
                "tests_part": doc["tests_part"],
                "has_solution": item["has_solution"],
            }
        )

    projects = []
    for item in content.list_projects():
        doc = content.read_project(item["id"])
        if doc:
            projects.append({"id": doc["id"], "title": doc["title"], "body": doc["body"]})

    quiz_questions, answers, quiz_whys = [], [], []
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "_quiz_bank", ROOT / "practice" / "quiz.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for item in getattr(module, "QUESTIONS", []):
            quiz_questions.append({"q": item["q"], "options": item["options"]})
            answers.append(item["answer"])
            quiz_whys.append(item["why"])
    except Exception as exc:  # noqa: BLE001
        print(f"هشدار: بانک آزمون خوانده نشد ({exc})")

    solutions = {}
    for path in sorted((ROOT / "solutions").glob("*.py")):
        solutions[path.stem.replace("_sol", "")] = path.read_text(encoding="utf-8")

    # بعضی تمرین‌ها سمت سرور از پوشه‌ی پروژه‌ها خوانده می‌شوند
    # (مثلاً first_steps که درس ۰ به آن وصل است). اینجا همان را از قبل
    # می‌شکافیم تا نسخه‌ی HTML هم دقیقاً همان پاسخ را بدهد.
    extra_exercises = {}
    projects_py = ROOT / "projects"
    if projects_py.is_dir():
        for path in sorted(projects_py.glob("*.py")):
            doc = content.read_exercise(path.stem)
            if doc:
                extra_exercises[doc["id"]] = doc

    return {
        "lessons": lessons,
        "exercises": exercises,
        "projects": projects,
        "solutions": solutions,
        "extraExercises": extra_exercises,
        "hints": hints_mod.HINTS,
        "generalHints": hints_mod.GENERAL_HINTS,
        "quiz": {"questions": quiz_questions, "answers": answers},
        "quizWhys": quiz_whys,
    }


# ─────────────────────────────────────────────────────────────
# ساخت HTML
# ─────────────────────────────────────────────────────────────


def assemble(course: dict, *, offline: bool) -> str:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    css = (WEB / "style.css").read_text(encoding="utf-8")
    md_js = (WEB / "md.js").read_text(encoding="utf-8")
    highlight_js = (WEB / "highlight.js").read_text(encoding="utf-8")
    app_js = (WEB / "app.js").read_text(encoding="utf-8")
    static_api_js = (WEB / "static-api.js").read_text(encoding="utf-8")
    tester_src = (ROOT / "pycourse" / "tester.py").read_text(encoding="utf-8")
    errors_src = (ROOT / "pycourse" / "errors_fa.py").read_text(encoding="utf-8")

    data_blob = json.dumps(course, ensure_ascii=False)

    html = html.replace(
        "<script>window.__BOOTSTRAP__ = /*__BOOTSTRAP__*/ null;</script>",
        f"<script>window.__COURSE__ = {data_blob};</script>",
    )
    html = html.replace('<link rel="stylesheet" href="/static/style.css">', f"<style>\n{css}\n</style>")
    html = html.replace('<script src="/static/md.js"></script>', f"<script>\n{md_js}\n</script>")
    html = html.replace(
        '<script src="/static/highlight.js"></script>', f"<script>\n{highlight_js}\n</script>"
    )
    # لایه‌ی API محلی باید قبل از app.js بیاید
    html = html.replace(
        '<script src="/static/app.js"></script>',
        f"<script>\n{static_api_js}\n</script>\n<script>\n{app_js}\n</script>",
    )

    common = f"""
  window.PYODIDE_CDN = "{PYODIDE_CDN}";
  window.__TESTER_SRC__ = {json.dumps(tester_src, ensure_ascii=False)};
  window.__ERRORS_SRC__ = {json.dumps(errors_src, ensure_ascii=False)};
"""

    if offline:
        loader_src = (VENDOR / OFFLINE_FILES["loader"]).read_text(encoding="utf-8")
        asm_src = (VENDOR / OFFLINE_FILES["asm"]).read_text(encoding="utf-8")
        wasm_b64 = base64.b64encode((VENDOR / OFFLINE_FILES["wasm"]).read_bytes()).decode("ascii")
        stdlib_b64 = base64.b64encode((VENDOR / OFFLINE_FILES["stdlib"]).read_bytes()).decode("ascii")
        lock_src = (VENDOR / OFFLINE_FILES["lock"]).read_text(encoding="utf-8")

        bootstrap = f"""
<script>
{common}
  window.__PYODIDE_OFFLINE__ = true;
  window.__PYODIDE_INDEX__ = "https://pyodide.local/";
</script>

<!-- ═══ Pyodide: بارگذار (کلاسیک) ═══ -->
<script>
{loader_src}
</script>

<!-- ═══ Pyodide: چسب wasm (خودش globalThis می‌گذارد) ═══ -->
<script>
{asm_src}
</script>

<!-- ═══ Pyodide: داده‌های باینری (base64) ═══ -->
<script id="pyodide-wasm-b64" type="application/octet-stream;base64">{wasm_b64}</script>
<script id="pyodide-stdlib-b64" type="application/octet-stream;base64">{stdlib_b64}</script>
<script id="pyodide-lock" type="application/json">{json.dumps(lock_src)}</script>

<script>
{common}
  (function () {{
    "use strict";

    function b64ToBytes(id) {{
      var bin = atob(document.getElementById(id).textContent.trim());
      var len = bin.length;
      var bytes = new Uint8Array(len);
      for (var i = 0; i < len; i++) bytes[i] = bin.charCodeAt(i);
      return bytes;
    }}

    var WASM = null;
    var STDLIB = null;

    function wasmBytes() {{
      if (!WASM) WASM = b64ToBytes("pyodide-wasm-b64");
      return WASM;
    }}
    function stdlibBytes() {{
      if (!STDLIB) STDLIB = b64ToBytes("pyodide-stdlib-b64");
      return STDLIB;
    }}

    // همه‌ی درخواست‌های Pyodide را به داده‌های داخلی وصل می‌کنیم
    var realFetch = window.fetch ? window.fetch.bind(window) : null;
    window.fetch = function (input, init) {{
      // Pyodide با شیء URL هم fetch می‌کند (نه فقط رشته)
      var url = "";
      if (typeof input === "string") {{
        url = input;
      }} else if (input && typeof input.href === "string") {{
        url = input.href;
      }} else if (input && typeof input.url === "string") {{
        url = input.url;
      }}

      if (url.indexOf("pyodide.asm.wasm") !== -1) {{
        return Promise.resolve(new Response(wasmBytes(), {{
          headers: {{ "Content-Type": "application/wasm" }},
        }}));
      }}
      if (url.indexOf("python_stdlib.zip") !== -1) {{
        return Promise.resolve(new Response(stdlibBytes(), {{
          headers: {{ "Content-Type": "application/zip" }},
        }}));
      }}
      if (url.indexOf("pyodide-lock.json") !== -1) {{
        return Promise.resolve(new Response(
          JSON.parse(document.getElementById("pyodide-lock").textContent),
          {{ headers: {{ "Content-Type": "application/json" }} }}
        ));
      }}
      if (!realFetch) {{
        return Promise.reject(new Error("اینترنت در دسترس نیست و این فایل داخل نسخه‌ی آفلاین نیست."));
      }}
      return realFetch(input, init);
    }};

    window.__PYODIDE_READY__ = null;
    function loadPyodide() {{
      if (window.__PYODIDE_READY__) return window.__PYODIDE_READY__;
      window.__PYODIDE_READY__ = Promise.resolve(
        globalThis.loadPyodide({{ indexURL: window.__PYODIDE_INDEX__ }})
      );
      return window.__PYODIDE_READY__;
    }}
  }})();
</script>
"""
    else:
        bootstrap = f"""
<script>
{common}
  window.__PYODIDE_OFFLINE__ = false;
  window.__PYODIDE_INDEX__ = window.PYODIDE_CDN;
  window.__PYODIDE_READY__ = null;
  function loadPyodide() {{
    if (window.__PYODIDE_READY__) return window.__PYODIDE_READY__;
    window.__PYODIDE_READY__ = new Promise((resolve, reject) => {{
      var script = document.createElement("script");
      script.src = window.PYODIDE_CDN + "pyodide.js";
      script.onload = function () {{
        (async function () {{
          try {{
            resolve(await globalThis.loadPyodide({{ indexURL: window.PYODIDE_CDN }}));
          }} catch (e) {{ reject(e); }}
        }})();
      }};
      script.onerror = function () {{
        reject(new Error("بارگذاری Pyodide از اینترنت ممکن نشد"));
      }};
      document.head.appendChild(script);
    }});
    return window.__PYODIDE_READY__;
  }}
</script>
"""

    return html.replace("</body>", bootstrap + "</body>")


def main() -> int:
    DIST.mkdir(exist_ok=True)
    course = build_course_data()

    # ── نسخه‌ی آنلاین ──
    online = assemble(course, offline=False)
    out_online = DIST / "PythonTerminal.html"
    out_online.write_text(online, encoding="utf-8")

    # ── نسخه‌ی آفلاین ──
    missing = [f for f in OFFLINE_FILES.values() if not (VENDOR / f).exists()]
    out_offline = DIST / "PythonTerminal-offline.html"
    if missing:
        print(f"⚠ فایل‌های Pyodide موجود نیستند ({', '.join(missing)}) — نسخه‌ی آفلاین ساخته نشد.")
        print("  برای ساختش یک‌بار اجرا کن:  python build_html.py --download")
    else:
        offline = assemble(course, offline=True)
        out_offline.write_text(offline, encoding="utf-8")

    print("=" * 62)
    print(f"✅ نسخه‌ی آنلاین : {out_online.name}  ({out_online.stat().st_size/1024:.0f} KB)")
    if out_offline.exists():
        print(f"✅ نسخه‌ی آفلاین : {out_offline.name}  ({out_offline.stat().st_size/1024/1024:.1f} MB)")
        print("   → بدون اینترنت و حتی از روی فایل محلی (file://) کار می‌کند")
    print("=" * 62)
    return 0


def download() -> int:
    """دانلود فایل‌های Pyodide برای ساخت نسخه‌ی آفلاین."""
    import urllib.request

    VENDOR.mkdir(parents=True, exist_ok=True)
    for name in OFFLINE_FILES.values():
        target = VENDOR / name
        if target.exists():
            print(f"  ✓ {name} (از قبل هست)")
            continue
        url = PYODIDE_CDN + name
        print(f"  ↓ دانلود {name} …")
        with urllib.request.urlopen(url, timeout=300) as res:
            target.write_bytes(res.read())
        print(f"    → {target.stat().st_size/1024/1024:.2f} MB")
    return 0


if __name__ == "__main__":
    if "--download" in sys.argv:
        sys.exit(download())
    sys.exit(main())
