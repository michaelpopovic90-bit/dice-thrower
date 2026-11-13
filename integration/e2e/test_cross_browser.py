"""INT-001: the delivered index.html over file:// in Chromium and Firefox (R-001, R-002)."""

import json
import os
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

SIDES = [4, 6, 8, 10, 12, 20]
FORBIDDEN = ("http:", "https:", "ws:", "wss:")
REPORT_JSON = Path(os.environ.get("E2E_VERSIONS_JSON", ".factory/scratch/int-browsers.json"))

TIMED_THROW = """() => {
  const t0 = performance.now();
  document.getElementById('roll').click();
  const ms = performance.now() - t0;
  return {ms, text: document.getElementById('result-value').textContent,
          state: document.getElementById('die').dataset.state};
}"""


@pytest.fixture(scope="module", params=["chromium", "firefox"])
def browser(request):
    with sync_playwright() as pw:
        kwargs = {"headless": True}
        if request.param == "chromium":
            exe = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
            if exe:
                kwargs["executable_path"] = exe
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                kwargs["args"] = ["--no-sandbox"]
        b = getattr(pw, request.param).launch(**kwargs)
        REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
        data = json.loads(REPORT_JSON.read_text()) if REPORT_JSON.exists() else {}
        data[request.param] = b.version
        REPORT_JSON.write_text(json.dumps(data))
        yield b
        b.close()


def open_page(browser, reduced_motion):
    ctx = browser.new_context(viewport={"width": 1280, "height": 800}, reduced_motion=reduced_motion)
    pg = ctx.new_page()
    pg.console_errors = []
    pg.requests = []
    pg.on("console", lambda m: pg.console_errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: pg.console_errors.append(str(e)))
    pg.on("request", lambda r: pg.requests.append(r.url))
    pg.goto(Path(os.environ.get("INDEX_HTML", "index.html")).resolve().as_uri())
    return ctx, pg


def check_clean(pg):
    assert pg.console_errors == []
    assert [u for u in pg.requests if u.startswith(FORBIDDEN)] == []


def test_all_dice_throw(browser):
    ctx, pg = open_page(browser, "no-preference")
    try:
        for n in SIDES:
            pg.check(f"#sides-{n}")
            pg.click("#roll")
            pg.wait_for_function("() => !document.getElementById('roll').disabled", timeout=10000)
            text = pg.inner_text("#result-value").strip()
            assert text.isdigit(), f"T{n}: result {text!r} is not an integer"
            assert 1 <= int(text) <= n, f"T{n}: {text} out of range"
            assert pg.get_attribute("#die", "data-value") == text
        check_clean(pg)
    finally:
        ctx.close()


def test_reduced_motion_is_immediate(browser):
    ctx, pg = open_page(browser, "reduce")
    try:
        for n in SIDES:
            pg.check(f"#sides-{n}")
            r = pg.evaluate(TIMED_THROW)
            assert r["state"] == "landed", r
            assert r["text"].strip().isdigit() and 1 <= int(r["text"]) <= n, r
            assert r["ms"] <= 100, f"T{n}: result took {r['ms']:.0f} ms with reduced motion"
            assert pg.get_attribute("#die", "data-value") == r["text"].strip()
        check_clean(pg)
    finally:
        ctx.close()
