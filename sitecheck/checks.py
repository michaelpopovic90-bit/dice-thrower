"""Static rules for index.html and README.md (plan/INTERFACES.md section 5)."""

from __future__ import annotations

import re

MAX_BYTES = 61440

FORBIDDEN_SUBSTRINGS = (
    "http:",
    "https:",
    "@import",
    "<link",
    "fetch(",
    "XMLHttpRequest",
    "WebSocket",
    "localStorage",
    "sessionStorage",
    "indexedDB",
    "document.cookie",
)

_ATTR_RE = re.compile(r"""\b(src|href|srcset|action|poster)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>"']+))""", re.I)
_SCRIPT_SRC_RE = re.compile(r"<script\b[^>]*\ssrc\b", re.I)
_URL_RE = re.compile(r"url\(\s*(?!['\"]?data:)", re.I)
_SERVER_RE = re.compile(r"(ingen|inte|utan)[^\n]{0,40}server", re.I)


def html_problems(text: str, size_bytes: int) -> list[str]:
    problems: list[str] = []
    for needle in FORBIDDEN_SUBSTRINGS:
        if needle in text:
            problems.append(f"forbidden substring: {needle}")
    if _SCRIPT_SRC_RE.search(text):
        problems.append("forbidden: <script src")
    for m in _ATTR_RE.finditer(text):
        value = next(g for g in m.groups()[1:] if g is not None).strip()
        if value and not value.startswith(("#", "data:")):
            problems.append(f"forbidden {m.group(1).lower()}= value pointing elsewhere: {value[:40]}")
    if _URL_RE.search(text):
        problems.append("forbidden: CSS url( other than url(data:")
    if '<html lang="sv">' not in text:
        problems.append('missing <html lang="sv">')
    if "<title>Tärning</title>" not in text:
        problems.append("missing <title>Tärning</title>")
    if "crypto.getRandomValues" not in text:
        problems.append("missing crypto.getRandomValues")
    if "requestAnimationFrame" not in text:
        problems.append("missing requestAnimationFrame")
    if size_bytes >= MAX_BYTES:
        problems.append(f"file too large: {size_bytes} bytes (limit {MAX_BYTES - 1})")
    return problems


def readme_problems(text: str) -> list[str]:
    problems: list[str] = []
    if len(text.splitlines()) > 60:
        problems.append("README has more than 60 lines")
    for word in ("index.html", "Kasta", "T20"):
        if word not in text:
            problems.append(f"README lacks the word {word}")
    if not _SERVER_RE.search(text):
        problems.append("README does not say that no server is needed")
    lowered = text.lower()
    has_letters = any(c in lowered for c in "åäö")
    has_words = re.search(r"\boch\b", lowered) and re.search(r"\batt\b", lowered)
    if not (has_letters or has_words):
        problems.append("README does not look Swedish")
    return problems
