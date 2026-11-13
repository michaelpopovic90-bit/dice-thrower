from playwright.sync_api import expect


def _landed(page, expected_sides):
    die = page.locator("#die")
    expect(die).to_have_attribute("data-state", "landed")
    expect(page.get_by_role("button", name="Kasta")).to_be_enabled()
    shown = page.locator("#result-value").inner_text()
    assert shown.isdigit()
    assert 1 <= int(shown) <= expected_sides
    assert die.get_attribute("data-value") == shown


def test_keyboard_only_journey(page):
    # Tab reaches the checked radio of the group (T6).
    page.keyboard.press("Tab")
    expect(page.get_by_role("radio", name="T6")).to_be_focused()

    # T6 -> T8 -> T10 -> T12 -> T20
    for _ in range(4):
        page.keyboard.press("ArrowRight")
    expect(page.get_by_role("radio", name="T20")).to_be_checked()
    expect(page.locator("#die")).to_have_attribute("data-sides", "20")

    page.keyboard.press("Tab")
    button = page.get_by_role("button", name="Kasta")
    expect(button).to_be_focused()

    page.keyboard.press("Enter")
    _landed(page, 20)

    # Focus must survive the roll so Space works without another Tab.
    expect(button).to_be_focused()
    page.keyboard.press("Space")
    expect(page.locator("#die")).to_have_attribute("data-state", "rolling")
    _landed(page, 20)

    assert page.console_errors == []
    assert [u for u in page.requests if u.startswith(("http:", "https:", "ws:", "wss:"))] == []
