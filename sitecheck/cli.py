"""Command line: python -m sitecheck html [index.html] | readme [README.md]."""

from __future__ import annotations

from pathlib import Path

from sitecheck.checks import html_problems, readme_problems

DEFAULTS = {"html": "index.html", "readme": "README.md"}


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in DEFAULTS or len(argv) > 2:
        print("usage: python -m sitecheck (html|readme) [file]")
        return 2
    kind = argv[0]
    path = Path(argv[1] if len(argv) > 1 else DEFAULTS[kind])
    try:
        raw = path.read_bytes()
    except OSError as exc:
        print(f"cannot read {path}: {exc}")
        return 1
    text = raw.decode("utf-8", errors="replace")
    problems = html_problems(text, len(raw)) if kind == "html" else readme_problems(text)
    if problems:
        for p in problems:
            print(p)
        return 1
    print("OK")
    return 0
