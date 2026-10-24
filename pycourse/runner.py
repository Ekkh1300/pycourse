"""
اجرای امن کد کاربر.

کد در یک پروسه‌ی جداگانه اجرا می‌شود تا:
  - اگر بی‌نهایت حلقه زد، بیشتر از N ثانیه کشته شود
  - اگر برنامه را بست، سرور ما هم نبندد
  - stdout/stderr تمیز و جدا باشند
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from . import paths

RUN_DIR = paths.run_dir()
DEFAULT_TIMEOUT = 10


def _child_env(script_path: Path | None = None) -> dict:
    env = os.environ.copy()
    # تضمین اینکه خروجی فارسی و یونیکد خراب نشود
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOBUF"] = "1"
    env["PYTHONUNBUFFERED"] = "1"
    env.pop("PYTHONSTARTUP", None)
    if script_path is not None:
        env["PYCOURSE_RUN_SCRIPT"] = str(script_path)
    return env


def _command(script_path: Path) -> tuple[list[str], dict]:
    """دستور اجرای کد را می‌سازد.

    در حالت معمولی: پایتون واقعی اجرا می‌شود.
    در حالت بسته‌بندی‌شده (exe): خودِ exe نقش مفسر را بازی می‌کند، چون
    `sys.executable` آن‌جا خودِ exe است و پایتونی روی سیستم نیست.
    """
    if paths.FROZEN:
        return [sys.executable], _child_env(script_path)
    return [sys.executable, "-u", str(script_path)], _child_env()


def run_source(source: str, *, timeout: int = DEFAULT_TIMEOUT, filename: str = "user_code.py") -> dict:
    """کد را اجرا می‌کند و نتیجه را برمی‌گرداند.

    خروجی:
        {
          "stdout": str,
          "stderr": str,
          "returncode": int | None,
          "timed_out": bool,
          "duration_ms": int,
          "error_line": int | None,
        }
    """
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(suffix=".py", prefix="run_", dir=str(RUN_DIR))
    os.close(fd)
    path = Path(tmp_path)
    path.write_text(source, encoding="utf-8")

    start = time.perf_counter()
    timed_out = False
    command, env = _command(path)
    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            timeout=timeout,
            cwd=str(RUN_DIR),
            env=env,
            encoding="utf-8",
            errors="replace",
        )
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        returncode: int | None = proc.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        stderr += (
            f"\n[Timeout] برنامه بیشتر از {timeout} ثانیه طول کشید و متوقف شد.\n"
            "[Timeout] احتمالاً یک حلقه‌ی بی‌پایان داری؛ مطمئن شو متغیر حلقه تغییر می‌کند."
        )
        returncode = None
    finally:
        duration_ms = int((time.perf_counter() - start) * 1000)
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass

    return {
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode,
        "timed_out": timed_out,
        "duration_ms": duration_ms,
    }


def cleanup_run_dir() -> None:
    """پوشه‌ی اجرا را خالی می‌کند (بدون پاک کردن خود پوشه)."""
    if not RUN_DIR.exists():
        return
    for item in RUN_DIR.iterdir():
        try:
            if item.is_file():
                item.unlink()
            else:
                item.rmdir()
        except OSError:
            pass
