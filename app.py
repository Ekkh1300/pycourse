#!/usr/bin/env python3
"""
«ترمینال پایتون» — محیط گرافیکی آموزش مقدماتی پایتون.

سرور محلی با کتابخانه‌ی استاندارد پایتون بالا می‌آید و در مرورگر باز می‌شود.
هیچ وابستگی بیرونی لازم نیست.

اجرا:
    python app.py
"""

from __future__ import annotations

import importlib.util
import json
import mimetypes
import os
import socket
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

# کنسول ویندوز پیش‌فرض cp1252 است و متن فارسی را خراب می‌کند
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

from pycourse import (  # noqa: E402
    content,
    errors_fa,
    errors_en,
    hints as hints_mod,
    hints_en,
    paths,
    progress,
    runner,
    tester,
)

ROOT = paths.app_root()
WEB_DIR = paths.web_dir()

HOST = "0.0.0.0"  # تا گوشی روی همان وای‌فای هم بتواند وصل شود
PORT = int(os.environ.get("PYCOURSE_PORT", "8765"))

# شمارنده‌ی تلاش‌ها برای اینکه راه‌حل زودتر از حد لازم لو نرود
MIN_ATTEMPTS_FOR_SOLUTION = 3


def _lang(query: dict | None = None) -> str:
    """Return a validated request language without changing global preference."""
    if query and query.get("lang"):
        lang = query["lang"][0]
        if lang in ("fa", "en"):
            return lang
    return paths.get_language()


def _diagnose(stderr: str, lang: str | None = None) -> object | None:
    """Diagnose in the current UI language."""
    return errors_fa.diagnose(stderr, lang=lang or paths.get_language())


def _hints(exercise_id: str, lang: str | None = None) -> list[str]:
    """Return the hint pool for an exercise in the current UI language."""
    lang = lang or paths.get_language()
    if lang == "en":
        return hints_en.HINTS.get(exercise_id, hints_en.GENERAL_HINTS)
    return hints_mod.HINTS.get(exercise_id, hints_mod.GENERAL_HINTS)


def _restore_streams() -> None:
    """در حالت windowed، پایتون `sys.stdout` را None می‌گذارد.

    برای اینکه فرزند بتواند خروجی و traceback را بنویسد، دستگیره‌های خام
    ۱ و ۲ را دوباره به stdout/stderr وصل می‌کنیم.
    """
    for name, fd in (("stdout", 1), ("stderr", 2)):
        if getattr(sys, name, None) is not None:
            continue
        try:
            stream = os.fdopen(
                fd, "w", encoding="utf-8", errors="replace", buffering=1, closefd=False
            )
            setattr(sys, name, stream)
        except (OSError, ValueError):
            pass


def _run_script_mode() -> int:
    """حالت «مفسر پایتون»: وقتی exe با متغیر PYCOURSE_RUN_SCRIPT صدا زده شود.

    این حالت لازم است تا کدِ کاربر در نسخه‌ی بسته‌بندی‌شده هم اجرا شود.
    در نسخه‌ی معمولی، `sys.executable` خودِ پایتون است و کافی است.
    """
    script = os.environ.get("PYCOURSE_RUN_SCRIPT")
    if not script:
        return -1
    import runpy

    _restore_streams()
    try:
        runpy.run_path(script, run_name="__main__")
    except SystemExit as exc:
        return int(exc.code or 0)
    except BaseException:  # noqa: BLE001
        traceback.print_exc()
        return 1
    return 0


# ─────────────────────────────────────────────────────────────
# بارگذاری بانک سؤالات آزمون
# ─────────────────────────────────────────────────────────────


def _load_quiz_questions() -> list[dict]:
    path = ROOT / "practice" / "quiz.py"
    if not path.exists():
        return []
    try:
        spec = importlib.util.spec_from_file_location("_quiz_bank", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return list(getattr(module, "QUESTIONS", []))
    except Exception:  # noqa: BLE001
        return []


QUESTIONS = _load_quiz_questions()


# ─────────────────────────────────────────────────────────────
# کمکی‌ها
# ─────────────────────────────────────────────────────────────


def _json_bytes(payload: dict | list) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def _read_body(handler: BaseHTTPRequestHandler) -> dict:
    try:
        length = int(handler.headers.get("Content-Length") or 0)
    except ValueError:
        length = 0
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _find_free_port(preferred: int) -> int:
    for candidate in range(preferred, preferred + 30):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((HOST, candidate))
            except OSError:
                continue
            return candidate
    return preferred


def _local_ips() -> list[str]:
    """آدرس‌های IP این دستگاه روی شبکه‌ی محلی."""
    found: list[str] = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            address = info[4][0]
            if address not in found and not address.startswith("127."):
                found.append(address)
    except OSError:
        pass

    # روش جایگزین: اتصال UDP بی‌واسطه (بدون ارسال داده)
    if not found:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(0.3)
                sock.connect(("8.8.8.8", 80))
                address = sock.getsockname()[0]
                if not address.startswith("127."):
                    found.append(address)
        except OSError:
            pass

    return found


# ─────────────────────────────────────────────────────────────
# مسیرهای API
# ─────────────────────────────────────────────────────────────


def api_network(_query: dict) -> dict:
    """آدرس‌هایی که از آن می‌شود با گوشی یا دستگاه دیگر باز کرد."""
    port = PORT
    ips = _local_ips()
    return {
        "port": port,
        "ips": ips,
        "urls": [f"http://{ip}:{port}/" for ip in ips],
        "local": f"http://127.0.0.1:{port}/",
    }


def api_set_language(body: dict) -> dict:
    """Set and persist the UI language."""
    lang = (body.get("lang") or "").strip()
    if lang not in ("fa", "en"):
        return {"lang": paths.get_language(), "error": "Invalid language"}
    paths.set_language(lang)
    progress.update(lang=lang)
    return {"lang": lang, "ok": True}


def api_curriculum(query: dict) -> dict:
    lang = _lang(query)
    return {
        "lessons": content.list_lessons(lang),
        "exercises": content.list_exercises(lang),
        "projects": content.list_projects(lang),
        "quiz_count": len(QUESTIONS),
        "python_version": sys.version.split()[0],
    }


def api_doc(query: dict) -> dict:
    doc_id = (query.get("id") or [""])[0]
    lang = _lang(query)
    doc = content.read_any(doc_id, lang)
    if doc is None:
        return {"error": "Document not found" if lang == "en" else "سند پیدا نشد"}
    return doc


def api_exercise(query: dict) -> dict:
    exercise_id = (query.get("id") or [""])[0]
    lang = _lang(query)
    exercise = content.read_exercise(exercise_id, lang)
    if exercise is None:
        return {"error": "Exercise not found" if lang == "en" else "تمرین پیدا نشد"}
    exercise["hints"] = _hints(exercise_id, lang)
    exercise["attempts"] = int(progress.get_state().get("attempts", {}).get(exercise_id, 0))
    return exercise


def api_hint(query: dict) -> dict:
    exercise_id = (query.get("exercise") or [""])[0]
    level = int((query.get("level") or ["1"])[0])
    lang = _lang(query)
    pool = _hints(exercise_id, lang)
    level = max(1, min(level, len(pool)))
    return {
        "level": level,
        "total": len(pool),
        "hint": pool[level - 1],
    }


def api_solution(query: dict) -> dict:
    exercise_id = (query.get("id") or [""])[0]
    attempts = int(progress.get_state().get("attempts", {}).get(exercise_id, 0))
    lang = _lang(query)
    if attempts < MIN_ATTEMPTS_FOR_SOLUTION:
        if lang == "en":
            return {
                "locked": True,
                "attempts": attempts,
                "needed": MIN_ATTEMPTS_FOR_SOLUTION,
                "message": (
                    f"To unlock the solution, you need at least {MIN_ATTEMPTS_FOR_SOLUTION} attempts. "
                    f"You've made {attempts} — read the hints first."
                ),
            }
        return {
            "locked": True,
            "attempts": attempts,
            "needed": MIN_ATTEMPTS_FOR_SOLUTION,
            "message": (
                f"برای دیدن راه‌حل باید حداقل {MIN_ATTEMPTS_FOR_SOLUTION} بار تلاش کنی. "
                f"الان {attempts} بار تلاش کرده‌ای — اول راهنماها را بخوان."
            ),
        }
    solution = content.read_solution(exercise_id)
    if solution is None:
        no_sol = ("No solution is available for this exercise." if lang == "en" else "برای این تمرین راه‌حل آماده نشده")
        return {"error": no_sol}
    return {"locked": False, **solution}


def api_progress_get(_query: dict) -> dict:
    return progress.get_state()


def api_progress_post(body: dict) -> dict:
    if "section" in body and "item" in body:
        done = progress.toggle_done(body["section"], body["item"])
        return {"done": done, "state": progress.get_state()}
    changes = {k: v for k, v in body.items() if k != "section" and k != "item"}
    return {"state": progress.update(**changes)}


def api_quiz(body: dict) -> dict:
    answers = body.get("answers") or []
    results = []
    score = 0
    for index, question in enumerate(QUESTIONS):
        chosen = answers[index] if index < len(answers) else None
        correct = chosen == question["answer"]
        if correct:
            score += 1
        results.append(
            {
                "index": index,
                "chosen": chosen,
                "correct_index": question["answer"],
                "is_correct": correct,
                "why": question["why"],
                "question": question["q"],
                "options": question["options"],
            }
        )
    total = len(QUESTIONS)
    percent = round(score / total * 100) if total else 0
    state = progress.get_state()
    best = state.get("quiz_best")
    if best is None or percent > best:
        progress.update(quiz_best=percent)
    return {
        "score": score,
        "total": total,
        "percent": percent,
        "results": results,
    }


def api_quiz_questions(_query: dict) -> dict:
    """بانک سؤالات آزمون (بدون پاسخ‌ها) برای نمایش در مرورگر."""
    safe = [
        {
            "q": item.get("q", ""),
            "options": item.get("options", []),
        }
        for item in QUESTIONS
    ]
    return {"questions": safe, "total": len(safe)}


def api_run(body: dict) -> dict:
    """Run user code and return output plus a localized diagnosis."""
    code = body.get("code") or ""
    mode = body.get("mode") or "run"
    exercise_id = body.get("exercise_id") or ""
    lang = body.get("lang") if body.get("lang") in ("en", "fa") else paths.get_language()

    if mode == "check":
        original = content.read_exercise(exercise_id, lang)
        tests = original["tests_part"] if original else ""
        # هر تست جداگانه اجرا می‌شود تا دقیقاً بدانیم کدام‌ها پاس شده‌اند
        script = tester.build_check_script(code, tests) if tests else None
        source = script if script else code
    else:
        source = code

    if not source.strip():
        return {"stdout": "", "stderr": "", "diagnosis": None, "returncode": None,
                "duration_ms": 0, "timed_out": False, "mode": mode, "tests": []}

    result = runner.run_source(source, timeout=int(body.get("timeout") or 10))

    # نتایج جداگانه‌ی تست‌ها
    test_results = None
    if mode == "check":
        test_results = tester.parse_results(result["stdout"])
        # خط مخصوص نتایج را از خروجی نمایشی بردار
        result["stdout"] = "\n".join(
            line
            for line in result["stdout"].splitlines()
            if not line.strip().startswith(tester.RESULTS_MARKER)
        ).strip()

    diagnosis = None
    if result["stderr"].strip():
        diagnosis = _diagnose(result["stderr"], lang)
        # اگر خطا از تست‌های خودمان آمده، پیام فارسی تست را نشان بده
        if diagnosis and diagnosis.kind == "AssertionError":
            diagnosis = errors_fa.diagnose_assertion(
                diagnosis.message, diagnosis.line, diagnosis.source
            )

    payload = {
        "stdout": result["stdout"],
        "stderr": result["stderr"] if result["stderr"] and not diagnosis else "",
        "raw_stderr": result["stderr"],
        "diagnosis": diagnosis.to_dict() if diagnosis else None,
        "returncode": result["returncode"],
        "duration_ms": result["duration_ms"],
        "timed_out": result["timed_out"],
        "mode": mode,
        "tests": test_results or [],
    }

    if mode == "check" and exercise_id:
        payload["attempts"] = progress.bump_attempt(exercise_id)

    return payload


# ─────────────────────────────────────────────────────────────
# هندلر HTTP
# ─────────────────────────────────────────────────────────────


class Handler(BaseHTTPRequestHandler):
    server_version = "PyCourse/1.0"
    protocol_version = "HTTP/1.1"

    # ── کمکی‌ها ──
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _send_json(self, payload: dict | list, status: int = 200) -> None:
        self._send(status, _json_bytes(payload), "application/json; charset=utf-8")

    def _send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self._send(404, b"not found", "text/plain; charset=utf-8")
            return
        ctype, _ = mimetypes.guess_type(path.name)
        if path.suffix == ".js":
            ctype = "text/javascript; charset=utf-8"
        elif path.suffix == ".css":
            ctype = "text/css; charset=utf-8"
        elif path.suffix == ".html":
            ctype = "text/html; charset=utf-8"
        elif path.suffix in (".md", ".py", ".txt", ".json"):
            ctype = "text/plain; charset=utf-8"
        self._send(200, path.read_bytes(), ctype or "application/octet-stream")

    def _send_index(self) -> None:
        """صفحه‌ی اصلی را با داده‌های اولیه تزریق‌شده می‌فرستد.

        این کار باعث می‌شود رابط کاربری از همان اولین رندر آماده باشد و
        صفحه‌ی «در حال اتصال» دیده نشود.
        """
        path = WEB_DIR / "index.html"
        if not path.exists():
            self._send(404, b"not found", "text/plain; charset=utf-8")
            return
        html = path.read_text(encoding="utf-8")
        saved_progress = progress.get_state()
        saved_lang = saved_progress.get("lang")
        if saved_lang not in ("fa", "en"):
            saved_lang = paths.get_language()
        payload = {
            "curriculum": api_curriculum({"lang": [saved_lang]}),
            "progress": saved_progress,
            "lang": saved_lang,
        }
        blob = json.dumps(payload, ensure_ascii=False)
        # کل عبارت «/*__BOOTSTRAP__*/ null» جایگزین می‌شود، نه فقط کامنت
        html = html.replace("/*__BOOTSTRAP__*/ null", blob)
        self._send(200, html.encode("utf-8"), "text/html; charset=utf-8")

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        if os.environ.get("PYCOURSE_VERBOSE"):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def handle_one_request(self) -> None:
        """قطع شدن ناگهانی مرورگر نباید پیام خطای طولانی چاپ کند."""
        try:
            super().handle_one_request()
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            self.close_connection = True

    def handle_error(self, request, client_address) -> None:  # noqa: A003
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionResetError, BrokenPipeError, ConnectionAbortedError)):
            return
        traceback.print_exc()

    # ── مسیریابی ──
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        try:
            # Set language from query param if present (lang=fa or lang=en)
            _lang(query)
            if path in ("/", "/index.html"):
                self._send_index()
                return

            if path.startswith("/static/"):
                name = path[len("/static/"):]
                target = (WEB_DIR / name).resolve()
                if WEB_DIR.resolve() in target.parents or target.parent == WEB_DIR.resolve():
                    self._send_file(target)
                else:
                    self._send(404, b"forbidden", "text/plain; charset=utf-8")
                return

            if path == "/api/curriculum":
                self._send_json(api_curriculum(query))
                return
            if path == "/api/network":
                self._send_json(api_network(query))
                return
            if path == "/api/set-language":
                self._send_json(api_set_language(body))
                return
            if path == "/api/doc":
                self._send_json(api_doc(query))
                return
            if path == "/api/exercise":
                self._send_json(api_exercise(query))
                return
            if path == "/api/hint":
                self._send_json(api_hint(query))
                return
            if path == "/api/solution":
                self._send_json(api_solution(query))
                return
            if path == "/api/progress":
                self._send_json(api_progress_get(query))
                return
            if path == "/api/quiz_questions":
                self._send_json(api_quiz_questions(query))
                return
            if path == "/api/health":
                self._send_json({"ok": True, "python": sys.version.split()[0], "lang": paths.get_language()})
                return

            self._send(404, b"not found", "text/plain; charset=utf-8")
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            self._send_json(
                {
                    "error": "خطای داخلی سرور",
                    "detail": traceback.format_exc(limit=6),
                },
                500,
            )

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        body = _read_body(self)

        try:
            if path == "/api/run":
                self._send_json(api_run(body))
                return
            if path == "/api/progress":
                self._send_json(api_progress_post(body))
                return
            if path == "/api/quiz":
                self._send_json(api_quiz(body))
                return
            if path == "/api/set-language":
                self._send_json(api_set_language(body))
                return
            self._send(404, b"not found", "text/plain; charset=utf-8")
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            self._send_json(
                {
                    "error": "خطای داخلی سرور",
                    "detail": traceback.format_exc(limit=6),
                },
                500,
            )


# ─────────────────────────────────────────────────────────────
# راه‌اندازی
# ─────────────────────────────────────────────────────────────


def main() -> int:
    global PORT
    saved_lang = progress.get_state().get("lang", "en")
    if saved_lang in ("fa", "en"):
        paths.set_language(saved_lang)
    PORT = _find_free_port(PORT)

    runner.cleanup_run_dir()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    port = httpd.server_address[1]
    url = f"http://127.0.0.1:{port}/"

    print("=" * 62, flush=True)
    print("  ترمینال پایتون — محیط آموزش مقدماتی")
    print("=" * 62)
    print(f"  روی این کامپیوتر :  http://127.0.0.1:{port}/")
    for ip in _local_ips():
        print(f"  از گوشی (وای‌فای) :  http://{ip}:{port}/")
    print()
    print(f"  پایتون    : {sys.version.split()[0]}")
    print(f"  پوشه      : {ROOT}")
    print(f"  درس‌ها    : {len(content.list_lessons())} | "
          f"تمرین‌ها: {len(content.list_exercises())} | "
          f"سؤالات آزمون: {len(QUESTIONS)}")
    print("=" * 62)
    print("  برای بستن برنامه این پنجره را ببند یا Ctrl+C بزن.")
    print("=" * 62, flush=True)

    if os.environ.get("PYCOURSE_NO_BROWSER") != "1":
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  در حال بستن...")
    finally:
        httpd.server_close()
        runner.cleanup_run_dir()
    return 0


if __name__ == "__main__":
    _script_code = _run_script_mode()
    if _script_code >= 0:
        sys.exit(_script_code)
    sys.exit(main())
