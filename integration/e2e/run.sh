#!/usr/bin/env bash
# INT-001: run index.html over file:// in Chromium and Firefox (see plan/INTERFACES.md section 7).
# Exit 0 = both browsers passed; 3 = Firefox unavailable (never a pass); other = failure.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1
SCRATCH="$ROOT/.factory/scratch"
VENV="$SCRATCH/int-venv"
FF_PATH="$SCRATCH/ms-playwright"
mkdir -p "$SCRATCH" "$FF_PATH"

INDEX_HTML="${INDEX_HTML:-index.html}"
if [ ! -f "$INDEX_HTML" ]; then
  echo "INDEX_HTML not found: $INDEX_HTML" >&2
  exit 2
fi
INDEX_HTML="$(cd "$(dirname "$INDEX_HTML")" && pwd)/$(basename "$INDEX_HTML")"
export INDEX_HTML

if [ ! -x "$VENV/bin/python" ]; then
  uv venv "$VENV" >/dev/null && \
    uv pip install --python "$VENV/bin/python" "pytest>=8,<10" "playwright>=1.47,<2" "ruff>=0.6" >/dev/null || {
    echo "could not create the test venv" >&2
    exit 2
  }
fi
PY="$VENV/bin/python"

# Chromium: explicit executable, else the shared Playwright cache.
if [ -z "${PLAYWRIGHT_CHROMIUM_EXECUTABLE:-}" ]; then
  for base in "${PLAYWRIGHT_BROWSERS_PATH:-}" /opt/ms-playwright "$HOME/.cache/ms-playwright"; do
    [ -n "$base" ] || continue
    for c in "$base"/chromium-*/chrome-linux*/chrome; do
      [ -x "$c" ] && PLAYWRIGHT_CHROMIUM_EXECUTABLE="$c"
    done
    [ -n "${PLAYWRIGHT_CHROMIUM_EXECUTABLE:-}" ] && break
  done
fi
export PLAYWRIGHT_CHROMIUM_EXECUTABLE

# Firefox: Playwright's own build in the scratch dir, installed when missing.
export PLAYWRIGHT_BROWSERS_PATH="$FF_PATH"
if ! ls -d "$FF_PATH"/firefox-* >/dev/null 2>&1; then
  if ! out="$("$PY" -m playwright install firefox 2>&1)"; then
    reason="$(printf '%s' "$out" | tail -n 1)"
    echo "FIREFOX NOT VERIFIED: ${reason:-install failed}"
    exit 3
  fi
fi

PYTHONDONTWRITEBYTECODE=1 "$PY" -m pytest integration/e2e -q -p no:cacheprovider
rc=$?
pkill -f "$FF_PATH" >/dev/null 2>&1 || true
exit $rc
