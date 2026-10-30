"""
Read and structure course content: lessons, exercises, and projects.

All content is read from disk, so editing a file immediately reflects in the app.
Supports bilingual content (English/Persian) via language-specific directories.
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

# Test marker in exercise files: everything from this line onwards is tests
TESTS_MARKER = 'if __name__ == "__main__":'

_PY_DIGITS = re.compile(r"^(?:ex|EX)(\d+)")

# ─────────────────────────────────────────────────────────────
# Language-aware paths
# ─────────────────────────────────────────────────────────────

def _lessons_dir_for_lang(lang: str) -> Path:
    """Return the lessons directory for the given language."""
    if lang == "en":
        return LESSONS_DIR / "en"
    return LESSONS_DIR / "fa"

def _exercises_dir_for_lang(lang: str) -> Path:
    """Return the exercises directory for the given language."""
    if lang == "en":
        return EXERCISES_DIR / "en"
    return EXERCISES_DIR / "fa"

def _projects_dir_for_lang(lang: str) -> Path:
    """Return the projects directory for the given language."""
    if lang == "en":
        return PROJECTS_DIR / "en"
    return PROJECTS_DIR / "fa"

def _fallback_dir(base: Path, lang: str) -> Path:
    """Return fallback directory (legacy flat structure)."""
    return base


# ─────────────────────────────────────────────────────────────
# Lessons
# ─────────────────────────────────────────────────────────────


def _lesson_title(path: Path) -> str:
    """Extract title from first # heading in markdown file."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return path.stem


def list_lessons(lang: str | None = None) -> list[dict]:
    """List all lessons for the given language."""
    if lang is None:
        lang = paths.get_language()
    
    lang_dir = _lessons_dir_for_lang(lang)
    fallback_dir = _fallback_dir(LESSONS_DIR, lang)
    
    items = []
    for path in sorted(lang_dir.glob("*.md")) if lang_dir.exists() else []:
        stem = path.stem
        number = stem.split("_", 1)[0]
        items.append({
            "id": stem,
            "number": number,
            "title": _lesson_title(path),
            "filename": path.name,
        })
    
    # Fallback to legacy flat structure if lang-specific dir is empty
    if not items:
        for path in sorted(fallback_dir.glob("*.md")):
            stem = path.stem
            number = stem.split("_", 1)[0]
            items.append({
                "id": stem,
                "number": number,
                "title": _lesson_title(path),
                "filename": path.name,
            })
    return items


def read_lesson(lesson_id: str, lang: str | None = None) -> dict | None:
    """Read a single lesson by ID for the given language."""
    if lang is None:
        lang = paths.get_language()
    
    lang_dir = _lessons_dir_for_lang(lang)
    fallback_dir = _fallback_dir(LESSONS_DIR, lang)
    
    path = lang_dir / f"{lesson_id}.md"
    if not path.exists():
        path = fallback_dir / f"{lesson_id}.md"
    
    if not path.exists() or not path.is_file():
        return None
    
    body = path.read_text(encoding="utf-8")
    return {
        "id": lesson_id,
        "title": _lesson_title(path),
        "body": body,
    }


# ─────────────────────────────────────────────────────────────
# Exercises
# ─────────────────────────────────────────────────────────────


def _docstring(source: str) -> str:
    """Extract module docstring using ast."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ""
    return ast.get_docstring(tree) or ""


def _exercise_title(source: str, fallback: str) -> str:
    """Exercise title: first meaningful line of docstring."""
    doc = _docstring(source)
    if doc:
        for line in doc.splitlines():
            line = line.strip()
            if line and not set(line) <= set("=-─═ "):
                return line
    return fallback


def _exercise_description(source: str) -> str:
    """Short description: rest of docstring without separator lines."""
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


def list_exercises(lang: str | None = None) -> list[dict]:
    """List all exercises for the given language."""
    if lang is None:
        lang = paths.get_language()
    
    lang_dir = _exercises_dir_for_lang(lang)
    fallback_dir = _fallback_dir(EXERCISES_DIR, lang)
    
    items = []
    for path in sorted(lang_dir.glob("ex*.py")) if lang_dir.exists() else []:
        try:
            source = path.read_text(encoding="utf-8")
        except OSError:
            continue
        match = _PY_DIGITS.match(path.stem)
        number = int(match.group(1)) if match else 0
        title = _exercise_title(source, path.stem)
        # Strip "Exercise N — " prefix; number shown in sidebar
        title = re.sub(r"^(?:تمرین|Exercise)\s*[۰-۹0-9]+\s*[—\-–]\s*", "", title).strip() or title
        items.append({
            "id": path.stem,
            "number": number,
            "title": title,
            "description": _exercise_description(source),
            "filename": path.name,
            "has_solution": (SOLUTIONS_DIR / f"{path.stem}_sol.py").exists(),
        })
    
    # Fallback to legacy flat structure
    if not items:
        for path in sorted(fallback_dir.glob("ex*.py")):
            try:
                source = path.read_text(encoding="utf-8")
            except OSError:
                continue
            match = _PY_DIGITS.match(path.stem)
            number = int(match.group(1)) if match else 0
            title = _exercise_title(source, path.stem)
            title = re.sub(r"^(?:تمرین|Exercise)\s*[۰-۹0-9]+\s*[—\-–]\s*", "", title).strip() or title
            items.append({
                "id": path.stem,
                "number": number,
                "title": title,
                "description": _exercise_description(source),
                "filename": path.name,
                "has_solution": (SOLUTIONS_DIR / f"{path.stem}_sol.py").exists(),
            })
    return items


def read_exercise(exercise_id: str, lang: str | None = None) -> dict | None:
    """Read a single exercise by ID for the given language."""
    if lang is None:
        lang = paths.get_language()
    
    lang_dir = _exercises_dir_for_lang(lang)
    fallback_dir = _fallback_dir(EXERCISES_DIR, lang)
    
    path = lang_dir / f"{exercise_id}.py"
    if not path.exists():
        path = fallback_dir / f"{exercise_id}.py"
    if not path.exists():
        # Some exercises live in projects/ (e.g., first_steps)
        path = _projects_dir_for_lang(lang) / f"{exercise_id}.py"
    if not path.exists():
        path = PROJECTS_DIR / f"{exercise_id}.py"
    
    if not path.exists() or not path.is_file():
        return None
    
    source = path.read_text(encoding="utf-8")
    user_part, tests_part = split_tests(source)
    title = _exercise_title(source, exercise_id)
    # Strip "Exercise N — " prefix; number shown in sidebar
    title = re.sub(r"^(?:تمرین|Exercise)\s*[۰-۹0-9]+\s*[—\-–]\s*", "", title).strip() or title
    return {
        "id": exercise_id,
        "title": title,
        "description": _exercise_description(source),
        "source": source,
        "user_part": user_part,
        "tests_part": tests_part,
    }


def split_tests(source: str) -> tuple[str, str]:
    """Split source into (user_code, tests_part) at TESTS_MARKER."""
    idx = source.find(TESTS_MARKER)
    if idx == -1:
        return source, ""
    # Back up to start of line
    line_start = source.rfind("\n", 0, idx) + 1
    return source[:line_start].rstrip() + "\n", source[line_start:]


def read_solution(exercise_id: str) -> dict | None:
    """Read solution file for an exercise."""
    path = SOLUTIONS_DIR / f"{exercise_id}_sol.py"
    if not path.exists() or not path.is_file():
        return None
    source = path.read_text(encoding="utf-8")
    note = ""
    for line in source.splitlines():
        if line.strip().startswith("#") and ("پاسخ" in line or "راه‌حل" in line or "solution" in line.lower()):
            note = line.strip().lstrip("# ").strip()
            break
    return {"id": exercise_id, "source": source, "note": note}


# ─────────────────────────────────────────────────────────────
# Projects
# ─────────────────────────────────────────────────────────────


def list_projects(lang: str | None = None) -> list[dict]:
    """List all projects for the given language."""
    if lang is None:
        lang = paths.get_language()
    
    lang_dir = _projects_dir_for_lang(lang)
    fallback_dir = _fallback_dir(PROJECTS_DIR, lang)
    
    items = []
    for path in sorted(lang_dir.glob("*.md")) if lang_dir.exists() else []:
        items.append({
            "id": path.stem,
            "title": _lesson_title(path),
            "filename": path.name,
        })
    
    # Fallback to legacy flat structure
    if not items:
        for path in sorted(fallback_dir.glob("*.md")):
            items.append({
                "id": path.stem,
                "title": _lesson_title(path),
                "filename": path.name,
            })
    return items


def read_project(project_id: str, lang: str | None = None) -> dict | None:
    """Read a single project by ID for the given language."""
    if lang is None:
        lang = paths.get_language()
    
    lang_dir = _projects_dir_for_lang(lang)
    fallback_dir = _fallback_dir(PROJECTS_DIR, lang)
    
    path = lang_dir / f"{project_id}.md"
    if not path.exists():
        path = fallback_dir / f"{project_id}.md"
    
    if not path.exists() or not path.is_file():
        return None
    return {
        "id": project_id,
        "title": _lesson_title(path),
        "body": path.read_text(encoding="utf-8"),
    }


def read_any(doc_id: str, lang: str | None = None) -> dict | None:
    """Read any document (lesson, project, or misc file) by ID for the given language."""
    if lang is None:
        lang = paths.get_language()
    
    if doc_id in ("first_steps",):
        path = _projects_dir_for_lang(lang) / "first_steps.py"
        if not path.exists():
            path = PROJECTS_DIR / "first_steps.py"
        if path.exists():
            return {
                "id": doc_id,
                "title": "First Steps" if lang == "en" else "اولین قدم‌ها",
                "body": path.read_text(encoding="utf-8"),
                "kind": "code",
            }
        return None
    
    lesson = read_lesson(doc_id, lang)
    if lesson:
        lesson["kind"] = "markdown"
        return lesson
    
    project = read_project(doc_id, lang)
    if project:
        project["kind"] = "markdown"
        return project
    
    return None


# ─────────────────────────────────────────────────────────────
# Legacy compatibility (for existing code)
# ─────────────────────────────────────────────────────────────


def list_lessons_legacy() -> list[dict]:
    """Legacy compatibility - uses default language."""
    return list_lessons()


def read_lesson_legacy(lesson_id: str) -> dict | None:
    """Legacy compatibility - uses default language."""
    return read_lesson(lesson_id)


def list_exercises_legacy() -> list[dict]:
    """Legacy compatibility - uses default language."""
    return list_exercises()


def read_exercise_legacy(exercise_id: str) -> dict | None:
    """Legacy compatibility - uses default language."""
    return read_exercise(exercise_id)


def list_projects_legacy() -> list[dict]:
    """Legacy compatibility - uses default language."""
    return list_projects()


def read_project_legacy(project_id: str) -> dict | None:
    """Legacy compatibility - uses default language."""
    return read_project(project_id)


def read_any_legacy(doc_id: str) -> dict | None:
    """Legacy compatibility - uses default language."""
    return read_any(doc_id)