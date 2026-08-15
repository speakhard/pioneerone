"""Live-browser checks for the one piece of behaviour the site has.

The episode grid ships as stills with links and upgrades to an embedded player
on click. Two things must hold, and neither is visible in the HTML alone:

  1. nothing is requested from a third party until someone presses play;
  2. pressing play actually plays, rather than navigating away.

Needs the dev server:

    python serve.py &
    python -m pytest tests/test_interaction.py -q
"""
from __future__ import annotations

import urllib.error
import urllib.request

import pytest

BASE = "http://127.0.0.1:8791"

playwright = pytest.importorskip("playwright.sync_api")


def _server_is_up() -> bool:
    try:
        urllib.request.urlopen(BASE, timeout=2).read(1)
        return True
    except (urllib.error.URLError, OSError):
        return False


pytestmark = pytest.mark.skipif(
    not _server_is_up(), reason=f"no dev server at {BASE} — run: python serve.py"
)


@pytest.fixture(scope="module")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        instance = pw.chromium.launch()
        yield instance
        instance.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 393, "height": 852})
    page = context.new_page()
    yield page
    context.close()


def test_nothing_third_party_loads_before_play(page):
    external = []
    page.on(
        "request",
        lambda r: external.append(r.url) if not r.url.startswith(BASE) else None,
    )
    page.goto(BASE + "/", wait_until="networkidle")
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1200)
    assert not external, f"the page reached off-site before anyone pressed play: {external}"


def test_pressing_play_embeds_the_player_in_place(page):
    page.goto(BASE + "/", wait_until="networkidle")
    frame = page.locator(".episode__frame").first
    frame.scroll_into_view_if_needed()
    frame.click()

    iframe = page.locator(".episode__frame iframe").first
    iframe.wait_for(state="attached", timeout=5000)

    src = iframe.get_attribute("src")
    assert "youtube-nocookie.com/embed/68RD46kl8ng" in src, src
    assert "autoplay=1" in src

    # Clicking must not have navigated to YouTube.
    assert page.url.rstrip("/") == BASE, f"the click navigated away to {page.url}"
    # The still is gone, replaced rather than stacked behind the player.
    assert page.locator(".episode__frame").first.locator("img").count() == 0


def test_every_episode_is_a_working_link_without_javascript(browser):
    """With JS off the grid is still six links to the episodes."""
    context = browser.new_context(java_script_enabled=False, viewport={"width": 393, "height": 852})
    page = context.new_page()
    page.goto(BASE + "/", wait_until="load")

    hrefs = page.eval_on_selector_all(
        ".episode__frame", "els => els.map(e => e.getAttribute('href'))"
    )
    assert len(hrefs) == 6
    assert all(h and "youtube.com/watch?v=" in h for h in hrefs), hrefs
    assert len(set(hrefs)) == 6, "two episodes point at the same video"
    context.close()


def test_the_skip_link_reaches_the_content(page):
    page.goto(BASE + "/", wait_until="load")
    page.keyboard.press("Tab")
    assert page.evaluate("() => document.activeElement.className") == "skip-link"
    assert page.evaluate("() => document.activeElement.getAttribute('href')") == "#main"


def test_headings_descend_in_order(page):
    """One h1, and no level is skipped — the structure screen readers navigate by."""
    for path in ("/", "/story/", "/archive/"):
        page.goto(BASE + path, wait_until="load")
        levels = page.eval_on_selector_all(
            "h1, h2, h3", "els => els.map(e => Number(e.tagName[1]))"
        )
        assert levels.count(1) == 1, f"{path} has {levels.count(1)} h1 elements"
        for previous, current in zip(levels, levels[1:]):
            assert current <= previous + 1, f"{path} jumps from h{previous} to h{current}"
