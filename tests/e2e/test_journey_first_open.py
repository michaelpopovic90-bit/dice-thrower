from playwright.sync_api import expect


def assert_offline(page):
    assert page.console_errors == []
    assert [u for u in page.requests if u.startswith(("http:", "https:", "ws:", "wss:"))] == []


def test_first_open_shows_static_t6_die_and_prompt(page):
    assert page.locator("html").get_attribute("lang") == "sv"
    assert page.title() == "Tärning"

    die = page.locator("#die")
    expect(die).to_have_attribute("data-sides", "6")
    expect(die).to_have_attribute("data-state", "idle")
    expect(die).to_have_attribute("aria-hidden", "true")
    assert page.locator("#die-canvas").evaluate("c => c.width > 0 && c.height > 0")
    # The canvas holds a drawn die: some pixels are not transparent.
    drawn = page.locator("#die-canvas").evaluate(
        "c => { const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;"
        " for (let i = 3; i < d.length; i += 4) { if (d[i] > 0) return true; } return false; }"
    )
    assert drawn

    group = page.get_by_role("group", name="Tärning")
    radios = group.get_by_role("radio")
    expect(radios).to_have_count(6)
    expect(group.get_by_role("radio", name="T6")).to_be_checked()

    buttons = page.get_by_role("button", name="Kasta")
    expect(buttons).to_have_count(1)
    expect(buttons).to_be_enabled()

    result = page.locator("#result")
    expect(result).to_have_text("Tryck på Kasta")
    expect(result).to_have_attribute("aria-live", "polite")
    assert_offline(page)
