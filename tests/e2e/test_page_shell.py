import pytest

NAMES = ["T4", "T6", "T8", "T10", "T12", "T20"]
SIDES = [4, 6, 8, 10, 12, 20]


def assert_clean(page):
    assert page.console_errors == []
    assert not [u for u in page.requests if u.startswith(("http:", "https:", "ws:", "wss:"))]


def test_basics(page):
    assert page.get_attribute("html", "lang") == "sv"
    assert page.title() == "Tärning"
    assert page.inner_text("#result-value") == "Tryck på Kasta"
    assert page.get_attribute("#die", "aria-hidden") == "true"
    assert page.get_attribute("#result", "aria-live") == "polite"
    assert page.get_attribute("#die", "data-state") == "idle"
    assert page.get_attribute("#die", "data-value") == ""
    assert page.locator("#die-canvas").count() == 1
    assert_clean(page)


def test_one_button_and_radios(page):
    buttons = page.get_by_role("button")
    assert buttons.count() == 1
    assert buttons.first.inner_text() == "Kasta"
    assert page.get_by_role("button", name="Kasta").count() == 1
    group = page.get_by_role("group", name="Tärning")
    assert group.count() == 1
    radios = group.get_by_role("radio")
    assert radios.count() == 6
    for name in NAMES:
        assert group.get_by_role("radio", name=name, exact=True).count() == 1
    assert group.get_by_role("radio", name="T6", exact=True).is_checked()
    assert page.get_attribute("#die", "data-sides") == "6"


@pytest.mark.parametrize(("name", "sides"), list(zip(NAMES, SIDES, strict=True)))
def test_selecting_sets_sides(page, name, sides):
    page.get_by_role("radio", name=name, exact=True).check(force=True)
    assert page.get_attribute("#die", "data-sides") == str(sides)
    assert page.get_attribute("#die", "data-state") == "idle"


def test_sides_set_synchronously(page):
    got = page.evaluate(
        """() => { const r = document.getElementById('sides-20'); r.checked = true;
        r.dispatchEvent(new Event('change', {bubbles: true}));
        return document.getElementById('die').dataset.sides; }"""
    )
    assert got == "20"


def test_arrow_keys(page):
    page.get_by_role("radio", name="T6", exact=True).focus()
    page.keyboard.press("ArrowRight")
    assert page.get_attribute("#die", "data-sides") == "8"
    page.keyboard.press("ArrowRight")
    page.keyboard.press("ArrowRight")
    assert page.get_attribute("#die", "data-sides") == "12"
    assert page.get_by_role("radio", name="T12", exact=True).is_checked()
    page.keyboard.press("ArrowLeft")
    assert page.get_attribute("#die", "data-sides") == "10"


def boxes_inside(page, viewport):
    for sel in ("#die", "#result", "#die-type", "#roll"):
        b = page.locator(sel).bounding_box()
        assert b is not None
        assert b["x"] >= 0 and b["y"] >= 0, sel
        assert b["x"] + b["width"] <= viewport[0], sel
        assert b["y"] + b["height"] <= viewport[1], sel
    assert page.evaluate("document.documentElement.scrollHeight <= innerHeight")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")


def font_px(page):
    return float(page.evaluate("getComputedStyle(document.getElementById('result')).fontSize").removesuffix("px"))


def test_layout_desktop(make_page):
    pg = make_page((1280, 800))
    assert font_px(pg) >= 96
    boxes_inside(pg, (1280, 800))
    assert_clean(pg)


def test_layout_mobile(make_page):
    pg = make_page((375, 667))
    assert font_px(pg) >= 72
    boxes_inside(pg, (375, 667))
    radios = [pg.locator(f"label[for=sides-{n}]").bounding_box() for n in SIDES]
    assert len({round(r["y"]) for r in radios}) == 1  # one row
    assert_clean(pg)


def test_canvas_and_button_size(make_page):
    pg = make_page((1280, 800))
    die = pg.locator("#die").bounding_box()
    assert abs(die["width"] - 272) < 1 and abs(die["height"] - 272) < 1  # min(55vmin, 34vh, 360px)
    btn = pg.locator("#roll").bounding_box()
    assert btn["height"] >= 48 and btn["width"] >= 160


def test_focus_outline(page):
    page.keyboard.press("Tab")  # the checked radio
    page.keyboard.press("Tab")  # the button
    assert page.evaluate("document.activeElement.id") == "roll"
    outline = page.evaluate("getComputedStyle(document.getElementById('roll')).outlineStyle")
    assert outline != "none"
    width = page.evaluate("getComputedStyle(document.getElementById('roll')).outlineWidth")
    assert width == "3px"
