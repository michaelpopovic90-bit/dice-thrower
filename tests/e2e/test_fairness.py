import pytest

COUNT_JS = """(args) => {
  const [n, runs] = args;
  document.getElementById('sides-' + n).click();
  const roll = document.getElementById('roll');
  const counts = {};
  let bad = 0;
  for (let i = 0; i < runs; i++) {
    roll.click();
    const text = document.getElementById('result-value').textContent;
    const v = Number(text);
    if (!Number.isInteger(v) || v < 1 || v > n || String(v) !== text) { bad++; continue; }
    counts[v] = (counts[v] || 0) + 1;
  }
  return { counts: counts, bad: bad, disabled: roll.disabled };
}"""


def run(page, n, runs):
    return page.evaluate(COUNT_JS, [n, runs])


@pytest.mark.parametrize(("n", "runs"), [(6, 6000), (20, 20000)])
def test_uniform_counts(make_page, n, runs):
    page = make_page(reduced_motion="reduce")
    out = run(page, n, runs)
    assert out["bad"] == 0
    assert out["disabled"] is False
    assert sorted(int(k) for k in out["counts"]) == list(range(1, n + 1))
    for v, c in out["counts"].items():
        assert 850 <= c <= 1150, (v, c)
    assert page.console_errors == []


@pytest.mark.parametrize("n", [4, 8, 10, 12])
def test_all_values_present(make_page, n):
    page = make_page(reduced_motion="reduce")
    out = run(page, n, n * 200)
    assert out["bad"] == 0
    assert sorted(int(k) for k in out["counts"]) == list(range(1, n + 1))
    assert page.console_errors == []
