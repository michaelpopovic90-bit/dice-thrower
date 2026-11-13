import pytest

SIDES = [4, 6, 8, 10, 12, 20]

TIMING_JS = """() => new Promise((resolve) => {
  const roll = document.getElementById('roll');
  const val = document.getElementById('result-value');
  const out = { disabledAfterClick: null, changedAt: null, enabledAt: null, stale: null, typeDisabled: null };
  const before = val.textContent;
  const t0 = performance.now();
  roll.click();
  out.disabledAfterClick = roll.disabled;
  out.typeDisabled = document.getElementById('die-type').disabled;
  out.stale = val.classList.contains('is-stale');
  const poll = () => {
    const now = performance.now() - t0;
    if (out.changedAt === null && val.textContent !== before) { out.changedAt = now; }
    if (!roll.disabled) { out.enabledAt = now; resolve(out); return; }
    if (now > 4000) { resolve(out); return; }
    setTimeout(poll, 5);
  };
  poll();
})"""


def assert_clean(page):
    assert page.console_errors == []
    assert not [u for u in page.requests if u.startswith(("http:", "https:", "ws:", "wss:"))]


def test_single_roll_button(page):
    assert page.get_by_role("button", name="Kasta").count() == 1
    assert page.locator("button").count() == 1


def test_timing_and_disabled_state(page):
    out = page.evaluate(TIMING_JS)
    assert out["disabledAfterClick"] is True
    assert out["typeDisabled"] is True
    assert out["stale"] is True
    assert out["changedAt"] is not None and 600 <= out["changedAt"] <= 1500
    assert out["enabledAt"] is not None and out["enabledAt"] <= 1600
    assert page.locator("#die-type").is_enabled()
    assert page.locator("#result-value.is-stale").count() == 0
    assert_clean(page)


def test_stale_colour_during_roll(page):
    page.evaluate("document.getElementById('roll').click()")
    colour = page.evaluate("getComputedStyle(document.getElementById('result-value')).color")
    assert colour == "rgb(92, 92, 92)"
    assert page.evaluate("document.getElementById('die').dataset.state") == "rolling"
    page.wait_for_function("document.getElementById('die').dataset.state === 'landed'")


@pytest.mark.parametrize("sides", SIDES)
def test_animation_and_landing(page, sides):
    page.get_by_role("radio", name=f"T{sides}", exact=True).check(force=True)
    assert page.evaluate("document.getElementById('die').dataset.sides") == str(sides)
    snaps = page.evaluate(
        """() => new Promise((resolve) => {
          const c = document.getElementById('die-canvas');
          const s = [];
          document.getElementById('roll').click();
          setTimeout(() => s.push(c.toDataURL()), 150);
          setTimeout(() => { s.push(c.toDataURL()); resolve(s); }, 300);
        })"""
    )
    assert snaps[0] != snaps[1]
    page.wait_for_function("document.getElementById('die').dataset.state === 'landed'")
    text = page.locator("#result-value").inner_text()
    assert page.evaluate("document.getElementById('die').dataset.value") == text
    assert page.evaluate("String(window.tarningDebug.frontFaceValue())") == text
    assert 1 <= int(text) <= sides
    assert page.locator("#result-die").text_content() == f"T{sides}: "
    assert_clean(page)


def test_frame_interval(page):
    mean = page.evaluate(
        """() => new Promise((resolve) => {
          const ts = [];
          let on = true;
          const tick = (t) => { if (on) { ts.push(t); requestAnimationFrame(tick); } };
          requestAnimationFrame(tick);
          document.getElementById('roll').click();
          setTimeout(() => {
            on = false;
            resolve((ts[ts.length - 1] - ts[0]) / (ts.length - 1));
          }, 900);
        })"""
    )
    assert mean < 20


def test_reduced_motion_is_synchronous(make_page):
    page = make_page(reduced_motion="reduce")
    out = page.evaluate(
        """() => {
          const roll = document.getElementById('roll');
          roll.click();
          return { text: document.getElementById('result-value').textContent,
                   state: document.getElementById('die').dataset.state,
                   disabled: roll.disabled, typeDisabled: document.getElementById('die-type').disabled,
                   die: document.getElementById('result-die').textContent,
                   value: document.getElementById('die').dataset.value,
                   front: String(window.tarningDebug.frontFaceValue()) };
        }"""
    )
    assert out["state"] == "landed"
    assert out["disabled"] is False and out["typeDisabled"] is False
    assert out["die"] == "T6: "
    assert out["text"] == out["value"] == out["front"]
    assert 1 <= int(out["text"]) <= 6
    assert_clean(page)


def test_reduced_motion_evaluated_on_each_click(make_page):
    page = make_page()
    page.emulate_media(reduced_motion="reduce")
    page.evaluate("document.getElementById('roll').click()")
    assert page.evaluate("document.getElementById('die').dataset.state") == "landed"
    page.emulate_media(reduced_motion="no-preference")
    page.evaluate("document.getElementById('roll').click()")
    assert page.evaluate("document.getElementById('roll').disabled") is True
    page.wait_for_function("!document.getElementById('roll').disabled")


@pytest.mark.parametrize("key", ["Enter", "Space"])
def test_keyboard(page, key):
    page.locator("#roll").focus()
    page.keyboard.press(key)
    page.wait_for_function("document.getElementById('die').dataset.state === 'landed'")
    assert page.evaluate("document.activeElement.id") == "roll"
    assert page.locator("#result-die").text_content() == "T6: "
    assert 1 <= int(page.locator("#result-value").inner_text()) <= 6


def test_arrow_keys_select_type(page):
    page.locator("#sides-6").focus()
    for _ in range(2):
        page.keyboard.press("ArrowRight")
    assert page.evaluate("document.getElementById('die').dataset.sides") == "10"
