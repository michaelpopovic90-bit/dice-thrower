import os
import re
from pathlib import Path

import pytest

SIDES = [4, 6, 8, 10, 12, 20]
SIZES = {4: 3, 6: 4, 8: 3, 10: 4, 12: 5, 20: 3}

PIXELS_JS = """() => {
  const c = document.getElementById('die-canvas');
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const hist = {};
  let die = 0;
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] < 255) { continue; }
    die++;
    const lum = Math.round(0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]);
    hist[lum] = (hist[lum] || 0) + 1;
  }
  return { die: die, hist: hist, w: c.width };
}"""


def assert_clean(page):
    assert page.console_errors == []
    assert not [u for u in page.requests if u.startswith(("http:", "https:", "ws:", "wss:"))]


@pytest.mark.parametrize("sides", SIDES)
def test_face_counts_and_sizes(page, sides):
    page.evaluate("n => window.tarningDebug.show(n, 1)", sides)
    assert page.evaluate("() => window.tarningDebug.faceCount()") == sides
    assert page.evaluate("() => window.tarningDebug.faceSizes()") == [SIZES[sides]] * sides
    assert_clean(page)


@pytest.mark.parametrize("sides", SIDES)
def test_front_face_is_the_value(page, sides):
    got = page.evaluate(
        """n => {
          const out = [];
          const dbg = window.tarningDebug;
          for (let v = 1; v <= n; v++) { dbg.show(n, v); out.push(dbg.frontFaceValue()); }
          return out;
        }""",
        sides,
    )
    assert got == list(range(1, sides + 1))
    assert_clean(page)


@pytest.mark.parametrize("sides", SIDES)
def test_rest_pose_is_shaded(page, sides):
    page.evaluate("n => window.tarningDebug.show(n, 1)", sides)
    data = page.evaluate(PIXELS_JS)
    assert data["die"] > 0.05 * data["w"] * data["w"], "canvas is blank or the die is tiny"
    hist = {int(k): v for k, v in data["hist"].items() if int(k) >= 100}  # face colours, not ink
    top = max(hist, key=hist.get)
    others = sum(v for k, v in hist.items() if abs(k - top) >= 10)
    assert others > 0.005 * data["die"], "all face pixels have the same brightness"
    assert_clean(page)


def test_radio_change_changes_shape(page):
    page.locator("#sides-6").check()
    six = page.evaluate("() => document.getElementById('die-canvas').toDataURL()")
    page.locator("#sides-20").check()
    assert page.get_attribute("#die", "data-sides") == "20"
    assert page.evaluate("() => window.tarningDebug.faceCount()") == 20
    twenty = page.evaluate("() => document.getElementById('die-canvas').toDataURL()")
    assert six != twenty
    page.locator("#sides-4").check()
    assert page.evaluate("() => window.tarningDebug.faceCount()") == 4
    assert_clean(page)


def test_canvas_backing_store_follows_css_size(make_page):
    pg = make_page(viewport=(375, 667))
    got = pg.evaluate(
        "() => { const c = document.getElementById('die-canvas');"
        " return [c.width, c.getBoundingClientRect().width * Math.min(devicePixelRatio, 2)]; }"
    )
    assert abs(got[0] - got[1]) <= 1
    pg.set_viewport_size({"width": 1280, "height": 800})
    pg.wait_for_function("() => document.getElementById('die-canvas').width > 250")
    got = pg.evaluate(
        "() => { const c = document.getElementById('die-canvas');"
        " return [c.width, c.getBoundingClientRect().width * Math.min(devicePixelRatio, 2)]; }"
    )
    assert abs(got[0] - got[1]) <= 1
    assert got[0] > 200
    assert_clean(pg)


@pytest.mark.parametrize("sides", SIDES)
def test_save_landing_png(page, sides, tmp_path):
    out_dir = Path(os.environ.get("E2E_ARTIFACT_DIR") or tmp_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    page.evaluate("n => window.tarningDebug.show(n, n)", sides)
    target = out_dir / f"render-T{sides}.png"
    page.locator("#die").screenshot(path=str(target))
    assert target.stat().st_size > 1000
    assert_clean(page)


def test_source_is_canvas_2d_only():
    text = Path("index.html").read_text(encoding="utf-8")
    assert not re.search(r"webgl|experimental-webgl|getContext\(\s*['\"](?!2d)", text, re.I)
    assert 'getContext("2d")' in text
    assert len(text.encode("utf-8")) < 61440
