import contextlib
import os
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def index_url():
    return Path("index.html").resolve().as_uri()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pw:
        kwargs = {"headless": True}
        exe = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        if exe:
            kwargs["executable_path"] = exe
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            kwargs["args"] = ["--no-sandbox"]
        b = pw.chromium.launch(**kwargs)
        yield b
        b.close()


@pytest.fixture
def make_page(browser, index_url, request):
    contexts = []
    pages = []

    def factory(viewport=(1280, 800), reduced_motion="no-preference"):
        ctx = browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]},
            reduced_motion=reduced_motion,
        )
        contexts.append(ctx)
        pg = ctx.new_page()
        pg.console_errors = []
        pg.requests = []
        pg.on("console", lambda m: pg.console_errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: pg.console_errors.append(str(e)))
        pg.on("request", lambda r: pg.requests.append(r.url))
        pg.goto(index_url)
        pages.append(pg)
        return pg

    yield factory

    rep = getattr(request.node, "rep_call", None)
    art = os.environ.get("E2E_ARTIFACT_DIR")
    if art and rep is not None and rep.failed:
        for i, pg in enumerate(pages):
            with contextlib.suppress(Exception):
                pg.screenshot(path=str(Path(art) / f"fail-{request.node.name}-{i}.png"))
    for ctx in contexts:
        ctx.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, "rep_" + call.when, outcome.get_result())  # noqa: B010


@pytest.fixture
def page(make_page):
    return make_page()
