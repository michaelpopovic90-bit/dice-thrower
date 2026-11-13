import pytest
from playwright.sync_api import expect

SIDES = [4, 6, 8, 10, 12, 20]
VIEWPORTS = [(1280, 800), (375, 667)]


@pytest.mark.parametrize("viewport", VIEWPORTS, ids=lambda v: f"{v[0]}x{v[1]}")
def test_every_die_type_throws_in_range(make_page, viewport):
    page = make_page(viewport=viewport)
    button = page.get_by_role("button", name="Kasta")
    die = page.locator("#die")
    for n in SIDES:
        page.get_by_role("radio", name=f"T{n}").check()
        expect(die).to_have_attribute("data-sides", str(n))
        button.click()
        expect(button).to_be_disabled()
        expect(die).to_have_attribute("data-state", "landed")
        expect(button).to_be_enabled()
        shown = page.locator("#result-value").inner_text()
        assert shown.isdigit()
        assert 1 <= int(shown) <= n
        assert die.get_attribute("data-value") == shown

    assert page.console_errors == []
    assert [u for u in page.requests if u.startswith(("http:", "https:", "ws:", "wss:"))] == []
