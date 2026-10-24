"""
خواندن و ساختاردهی‌ی محتوای دوره: درس‌ها، تمرین‌ها و پروژه‌ها.

همه‌چیز از روی دیسک خوانده می‌شود، پس اگر فایلی را ویرایش کنی
بلافاصله در برنامه دیده می‌شود.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from . import paths

ROOT = paths.app_root()
LESSONS_DIR = ROOT / "lessons"
EXERCISES_DIR = ROOT / "exercises"
PROJECTS_DIR = ROOT / "projects"
SOLUTIONS_DIR = ROOT / "solutions"

# مرز تست‌ها در فایل تمرین: از این خط به بعد، تست‌های خودکار شروع می‌شوند
TESTS_MARKER = "if __name__ == \"__main__\":"

_PY_DIGITS = re.compile(r"^(?:ex|EX)(\d+)")


# ─────────────────────────────────────────────────────────────
# درس‌ها
# ─────────────────────────────────────────────────────────────


def _lesson_title(path: Path) -> str:
    """عنوان را از خط اول فایل markdown برمی‌دارد."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return path.stem


def list_lessons() -> list[dict]:
    if not LESSONS_DIR.exists():
        return []
    items = []
    for path in sorted(LESSONS_DIR.glob("*.md")):
        stem = path.stem
        number = stem.split("_", 1)[0]
        items.append(
            {
                "id": stem,
                "number": number,
                "title": _lesson_title(path),
                "filename": path.name,
            }
        )
    return items


def read_lesson(lesson_id: str) -> dict | None:
    path = LESSONS_DIR / f"{lesson_id}.md"
    if not path.exists() or not path.is_file():
        return None
    body = path.read_text(encoding="utf-8")
    return {
        "id": lesson_id,
        "title": _lesson_title(path),
        "body": body,
    }


# ─────────────────────────────────────────────────────────────
# تمرین‌ها
# ─────────────────────────────────────────────────────────────


def _docstring(source: str) -> str:
    """داک‌استرینگ ماژول را با ast بیرون می‌کشد."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ""
    return ast.get_docstring(tree) or ""


def _exercise_title(source: str, fallback: str) -> str:
    """عنوان تمرین: اولین خط معنادار داک‌استرینگ."""
    doc = _docstring(source)
    if doc:
        for line in doc.splitlines():
            line = line.strip()
            if line and not set(line) <= set("=-─═ "):
                return line
    return fallback


def _exercise_description(source: str) -> str:
    """توضیح کوتاه: بقیه‌ی داک‌استرینگ بدون خطوط جداکننده."""
    doc = _docstring(source)
    if not doc:
        return ""
    lines = doc.splitlines()
    kept: list[str] = []
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            kept.append("")
            continue
        if set(stripped) <= set("=-─═ "):
            continue
        kept.append(stripped)
    while kept and not kept[-1]:
        kept.pop()
    return "\n".join(kept).strip()


def list_exercises() -> list[dict]:
    if not EXERCISES_DIR.exists():
        return []
    items = []
    for path in sorted(EXERCISES_DIR.glob("ex*.py")):
        try:
            source = path.read_text(encoding="utf-8")
        except OSError:
            continue
        match = _PY_DIGITS.match(path.stem)
        number = int(match.group(1)) if match else 0
        title = _exercise_title(source, path.stem)
        title = re.sub(r"^تمرین\s*[۰-۹0-9]+\s*[—\-–]\s*", "", title).strip() or title
        items.append(
            {
                "id": path.stem,
                "number": number,
                "title": title,
                "description": _exercise_description(source),
                "filename": path.name,
                "has_solution": (SOLUTIONS_DIR / f"{path.stem}_sol.py").exists(),
            }
        )
    return items


def read_exercise(exercise_id: str) -> dict | None:
    path = EXERCISES_DIR / f"{exercise_id}.py"
    if not path.exists():
        # بعضی تمرین‌ها در پوشه‌ی پروژه‌ها هستند (مثل first_steps)
        path = PROJECTS_DIR / f"{exercise_id}.py"
    if not path.exists() or not path.is_file():
        return None
    source = path.read_text(encoding="utf-8")
    user_part, tests_part = split_tests(source)
    title = _exercise_title(source, exercise_id)
    # پیشوند «تمرین N — » را بردار؛ شماره در نوار کناری نشان داده می‌شود
    title = re.sub(r"^تمرین\s*[۰-۹0-9]+\s*[—\-–]\s*", "", title).strip() or title
    return {
        "id": exercise_id,
        "title": title,
        "description": _exercise_description(source),
        "source": source,
        "user_part": user_part,
        "tests_part": tests_part,
    }


def split_tests(source: str) -> tuple[str, str]:
    """کد را به دو بخش تقسیم می‌کند: (کد کاربر، بخش تست‌ها).

    بخش تست‌ها از `if __name__ == "__main__":` شروع می‌شود.
    """
    idx = source.find(TESTS_MARKER)
    if idx == -1:
        return source, ""
    # به عقب تا ابتدای خط برگرد
    line_start = source.rfind("\n", 0, idx) + 1
    return source[:line_start].rstrip() + "\n", source[line_start:]


def read_solution(exercise_id: str) -> dict | None:
    path = SOLUTIONS_DIR / f"{exercise_id}_sol.py"
    if not path.exists() or not path.is_file():
        return None
    source = path.read_text(encoding="utf-8")
    note = ""
    for line in source.splitlines():
        if line.strip().startswith("#") and ("پاسخ" in line or "راه‌حل" in line):
            note = line.strip().lstrip("# ").strip()
            break
    return {"id": exercise_id, "source": source, "note": note}


# ─────────────────────────────────────────────────────────────
# پروژه‌ها
# ─────────────────────────────────────────────────────────────


def list_projects() -> list[dict]:
    if not PROJECTS_DIR.exists():
        return []
    items = []
    for path in sorted(PROJECTS_DIR.glob("*.md")):
        items.append(
            {
                "id": path.stem,
                "title": _lesson_title(path),
                "filename": path.name,
            }
        )
    return items


def read_project(project_id: str) -> dict | None:
    path = PROJECTS_DIR / f"{project_id}.md"
    if not path.exists() or not path.is_file():
        return None
    return {
        "id": project_id,
        "title": _lesson_title(path),
        "body": path.read_text(encoding="utf-8"),
    }


def read_any(doc_id: str) -> dict | None:
    """هر سندی (درس، پروژه، یا فایل متفرقه) را برمی‌گرداند."""
    if doc_id in ("first_steps",):
        path = PROJECTS_DIR / "first_steps.py"
        if path.exists():
            return {
                "id": doc_id,
                "title": "اولین قدم‌ها",
                "body": path.read_text(encoding="utf-8"),
                "kind": "code",
            }
        return None
    lesson = read_lesson(doc_id)
    if lesson:
        lesson["kind"] = "markdown"
        return lesson
    project = read_project(doc_id)
    if project:
        project["kind"] = "markdown"
        return project
    return None
