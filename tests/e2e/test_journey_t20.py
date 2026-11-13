from playwright.sync_api import expect


def test_choose_t20_and_throw(page):
    page.get_by_role("radio", name="T20").check()
    die = page.locator("#die")
    expect(die).to_have_attribute("data-sides", "20")

    button = page.get_by_role("button", name="Kasta")
    button.click()
    expect(button).to_be_disabled()

    expect(die).to_have_attribute("data-state", "landed")
    expect(button).to_be_enabled()

    shown = page.locator("#result-value").inner_text()
    assert shown.isdigit()
    assert 1 <= int(shown) <= 20
    assert die.get_attribute("data-value") == shown
    assert page.locator("#result-die").text_content() == "T20: "

    assert page.console_errors == []
    assert [u for u in page.requests if u.startswith(("http:", "https:", "ws:", "wss:"))] == []
