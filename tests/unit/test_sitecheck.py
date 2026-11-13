import subprocess
import sys

import pytest

from sitecheck.checks import html_problems, readme_problems
from sitecheck.cli import main

GOOD_HTML = (
    '<!DOCTYPE html><html lang="sv"><head><title>Tärning</title><style>a{background:url(data:image/png;base64,AA)}'
    '</style></head><body><a href="#x">x</a><script>crypto.getRandomValues(new Uint32Array(1));'
    "requestAnimationFrame(f);</script></body></html>"
)
GOOD_README = "Öppna index.html och tryck på Kasta. Finns T4 till T20. Ingen server behövs.\n"


def probs(text=GOOD_HTML, size=1000):
    return html_problems(text, size)


def test_good_html_passes():
    assert probs() == []


@pytest.mark.parametrize(
    "bad",
    [
        "http:",
        "https:",
        "@import",
        "<link",
        "fetch(",
        "XMLHttpRequest",
        "WebSocket",
        "localStorage",
        "sessionStorage",
        "indexedDB",
        "document.cookie",
    ],
)
def test_forbidden_substrings(bad):
    result = probs(GOOD_HTML + f"<!-- {bad} -->")
    assert any(bad in p for p in result)


def test_script_src_flagged():
    assert any("<script src" in p for p in probs(GOOD_HTML + '<script src="a.js"></script>'))
    assert not any("<script src" in p for p in probs())


@pytest.mark.parametrize("attr", ["src", "href", "srcset", "action", "poster"])
@pytest.mark.parametrize("value", ["//cdn/x", "other.js", "x.png"])
def test_attribute_values_flagged(attr, value):
    assert any(f"{attr}=" in p for p in probs(GOOD_HTML + f'<x {attr}="{value}">'))


def test_attribute_fragment_and_data_ok():
    assert probs(GOOD_HTML + "<img src=\"data:image/png;base64,AA\"><a href='#top'>") == []


def test_css_url_rules():
    assert any("url(" in p for p in probs(GOOD_HTML + "<style>a{background:url(x.png)}</style>"))
    assert not any("url(" in p for p in probs(GOOD_HTML + "<style>a{background:url('data:x')}</style>"))


def test_lang_and_title():
    assert any("lang" in p for p in probs(GOOD_HTML.replace('lang="sv"', 'lang="en"')))
    assert any("title" in p for p in probs(GOOD_HTML.replace("Tärning", "Dice")))


def test_required_apis():
    assert any("getRandomValues" in p for p in probs(GOOD_HTML.replace("crypto.getRandomValues", "x")))
    assert any("requestAnimationFrame" in p for p in probs(GOOD_HTML.replace("requestAnimationFrame", "x")))


def test_size_limit():
    assert probs(size=61439) == []
    assert any("too large" in p for p in probs(size=61440))


def test_readme_good():
    assert readme_problems(GOOD_README) == []


def test_readme_line_limit():
    assert readme_problems(GOOD_README + "x\n" * 59) == []
    assert any("60" in p for p in readme_problems(GOOD_README + "x\n" * 60))


@pytest.mark.parametrize("word", ["index.html", "Kasta", "T20"])
def test_readme_required_words(word):
    assert any(word in p for p in readme_problems(GOOD_README.replace(word, "")))


def test_readme_server_sentence():
    assert any("server" in p for p in readme_problems("index.html Kasta T20 på och att. Server finns.\n"))
    assert readme_problems("index.html Kasta T20 och att. Utan server.\n") == []


def test_readme_swedish_heuristic():
    english = "index.html Kasta T20. No server, nothing else: ingen server.\n"
    assert any("Swedish" in p for p in readme_problems(english))
    assert readme_problems("index.html Kasta T20. Ingen server, och att.\n") == []


def test_cli(tmp_path, capsys):
    good = tmp_path / "index.html"
    good.write_text(GOOD_HTML, encoding="utf-8")
    assert main(["html", str(good)]) == 0
    assert capsys.readouterr().out.strip() == "OK"
    bad = tmp_path / "bad.html"
    bad.write_text('<a href="https://x">', encoding="utf-8")
    assert main(["html", str(bad)]) == 1
    readme = tmp_path / "README.md"
    readme.write_text(GOOD_README, encoding="utf-8")
    assert main(["readme", str(readme)]) == 0
    assert main(["html", str(tmp_path / "missing.html")]) == 1
    assert main([]) == 2


def test_module_exit_code(tmp_path):
    bad = tmp_path / "x.html"
    bad.write_text("<script src='a.js'></script> https:", encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "sitecheck", "html", str(bad)], capture_output=True, text=True)  # noqa: S603
    assert r.returncode == 1
    assert "https:" in r.stdout
    assert "<script src" in r.stdout
