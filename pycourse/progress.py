"""
ذخیره‌ی پیشرفت یادگیرنده روی دیسک (یک فایل JSON کنار برنامه).
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

from . import paths

ROOT = paths.app_root()
STORE_PATH = paths.progress_file()

_lock = threading.Lock()

DEFAULT_STATE = {
    "lessons_done": [],
    "exercises_done": [],
    "attempts": {},  # {"ex01_basics": 3}
    "quiz_best": None,
    "font_size": 15,
    "theme": "amber",
    "notes": {},  # {"ex01_basics": "یادداشت من"}
}


def _read() -> dict:
    if not STORE_PATH.exists():
        return dict(DEFAULT_STATE)
    try:
        data = json.loads(STORE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT_STATE)
    merged = dict(DEFAULT_STATE)
    if isinstance(data, dict):
        merged.update(data)
    return merged


def _write(state: dict) -> None:
    STORE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def get_state() -> dict:
    with _lock:
        return _read()


def update(**changes) -> dict:
    """مقدارها را به‌روز می‌کند و وضعیت جدید را برمی‌گرداند."""
    with _lock:
        state = _read()
        for key, value in changes.items():
            if key not in DEFAULT_STATE:
                continue
            if key in ("lessons_done", "exercises_done"):
                current = set(state.get(key) or [])
                if isinstance(value, list):
                    current.update(value)
                state[key] = sorted(current)
            elif key in ("attempts", "notes"):
                current = dict(state.get(key) or {})
                if isinstance(value, dict):
                    current.update(value)
                state[key] = current
            else:
                state[key] = value
        _write(state)
        return state


def bump_attempt(exercise_id: str) -> int:
    """تعداد تلاش‌های یک تمرین را یکی زیاد می‌کند و مقدار جدید را برمی‌گرداند."""
    with _lock:
        state = _read()
        attempts = dict(state.get("attempts") or {})
        attempts[exercise_id] = int(attempts.get(exercise_id, 0)) + 1
        state["attempts"] = attempts
        _write(state)
        return attempts[exercise_id]


def toggle_done(section: str, item_id: str) -> bool:
    """علامت‌گذاری «انجام شد» و برگرداندن وضعیت جدید."""
    key = "lessons_done" if section == "lessons" else "exercises_done"
    with _lock:
        state = _read()
        items = set(state.get(key) or [])
        if item_id in items:
            items.discard(item_id)
            done = False
        else:
            items.add(item_id)
            done = True
        state[key] = sorted(items)
        _write(state)
        return done
