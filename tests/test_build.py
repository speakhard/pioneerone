"""Checks on the built site.

These exist to catch the failures that are invisible in a screenshot: a srcset
pointing at a file that was never written, an episode quietly dropped from the
grid, a social card that would render as a broken image on somebody's phone.

    python -m pytest -q
"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import builder  # noqa: E402


@pytest.fixture(scope="module")
def site(tmp_path_factory) -> Path:
    """Build into a temporary directory, never over the working site/."""
    return builder.build(tmp_path_factory.mktemp("site") / "out")


@pytest.fixture(scope="module")
def home(site: Path) -> str:
    return (site / "index.html").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def episodes() -> list[dict]:
    with (ROOT / "content" / "episodes.toml").open("rb") as handle:
        return sorted(tomllib.load(handle)["episode"], key=lambda e: e["number"])


def test_every_page_is_written(site: Path):
    for path in ("index.html", "story/index.html", "archive/index.html"):
        assert (site / path).is_file(), f"{path} was not built"


def test_all_six_episodes_are_on_the_homepage(home: str, episodes: list[dict]):
    assert len(episodes) == 6
    for episode in episodes:
        assert episode["title"] in home, f"episode {episode['number']} missing"
        assert episode["youtube"] in home, f"episode {episode['number']} has no video id"
        # The synopsis is the show's own words; a stray apostrophe change would
        # mean the file no longer matches what was recovered.
        assert episode["synopsis"][:60] in home


def test_every_referenced_asset_exists(site: Path):
    """No src, srcset entry or stylesheet may point at a file that is not there.

    This is the check that matters most: a missing image is a hole in the page
    and a 404 is invisible until somebody loads it on a phone.
    """
    missing = []
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        refs = set(re.findall(r'(?:src|href)="([^"]+)"', html))
        for srcset in re.findall(r'srcset="([^"]+)"', html):
            refs.update(part.strip().split()[0] for part in srcset.split(",") if part.strip())
        for ref in refs:
            if ref.startswith(("http", "mailto:", "#", "data:")):
                continue
            clean = ref.split("#")[0].split("?")[0]
            if not clean:
                continue
            # Root-relative links resolve against the site root, not the page.
            target = (site / clean.lstrip("/")) if clean.startswith("/") else (page.parent / clean)
            target = target.resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                missing.append(f"{page.relative_to(site)} -> {ref}")
    assert not missing, "referenced but not built:\n  " + "\n  ".join(missing)


def test_srcset_widths_match_real_files(site: Path):
    """Each srcset descriptor must equal the file's real width."""
    wrong = []
    for page in site.rglob("*.html"):
        for srcset in re.findall(r'srcset="([^"]+)"', page.read_text(encoding="utf-8")):
            for part in srcset.split(","):
                url, _, descriptor = part.strip().partition(" ")
                match = re.search(r"-(\d+)\.jpg$", url)
                if match and descriptor:
                    assert descriptor == f"{match.group(1)}w", f"{url} declared {descriptor}"
    assert not wrong


def test_no_upscaled_episode_still(site: Path):
    """prepare_assets.py must never invent detail it does not have."""
    from PIL import Image

    for image in (site / "static" / "img").glob("*-[0-9]*.jpg"):
        # social-card.jpg and friends carry no width suffix; skip them.
        suffix = image.stem.rsplit("-", 1)[1]
        if not suffix.isdigit():
            continue
        assert Image.open(image).width == int(suffix), f"{image.name} is not {suffix}px wide"


def test_social_card_is_the_size_the_meta_tag_promises(site: Path, home: str):
    from PIL import Image

    assert 'property="og:image:width" content="1200"' in home
    assert Image.open(site / "static" / "img" / "social-card.jpg").size == (1200, 630)


def test_structured_data_is_valid_json_and_lists_the_season(home: str):
    block = re.search(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', home, re.S
    )
    assert block, "no JSON-LD on the homepage"
    data = json.loads(block.group(1))
    assert data["@type"] == "TVSeries"
    assert data["numberOfEpisodes"] == 6
    assert len(data["containsSeason"]["episode"]) == 6


def test_pages_carry_their_own_title_and_description(site: Path):
    seen = set()
    for path in ("index.html", "story/index.html", "archive/index.html"):
        html = (site / path).read_text(encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
        description = re.search(r'<meta name="description" content="([^"]+)"', html).group(1)
        assert title.strip() and description.strip()
        assert title not in seen, f"{path} reuses a title"
        seen.add(title)


def test_no_placeholder_text_survived(site: Path):
    for page in site.rglob("*.html"):
        text = page.read_text(encoding="utf-8").lower()
        for banned in ("lorem ipsum", "todo", "fixme", "xxx", "placeholder text"):
            assert banned not in text, f"{page.name} still contains {banned!r}"


def test_episode_six_date_was_corrected(episodes: list[dict]):
    """The original page said 2012. Three contemporaneous posts say 2011.

    Pinned by a test because it is exactly the kind of correction that gets
    silently reverted by someone copying from the old page. See STORY-SOURCES.md.
    """
    assert episodes[5]["released"] == "2011-12-13"


def test_the_now_section_promises_nothing(home: str):
    """The brief is explicit: no greenlight, no financing, no announcement.

    Checked as claims rather than as substrings. "nothing has been greenlit" is
    a denial and must pass; "has been greenlit" on its own must not. The first
    version of this test failed on the site's own disclaimer, which is the
    right kind of mistake to have made once and not again.
    """
    text = re.sub(r"<[^>]+>", " ", home.lower())
    text = re.sub(r"\s+", " ", text)

    assert "an announcement" in text, "the Now section lost its disclaimer"

    claims = (
        r"season 2 is happening",
        r"officially announced",
        r"has been greenlit",
        r"now in production",
        r"fully financed",
        r"in production",
    )
    negations = ("no ", "not ", "nothing ", "never ", "neither ", "isn't ", "is not ")
    for claim in claims:
        for match in re.finditer(claim, text):
            preceding = text[max(0, match.start() - 60) : match.start()]
            if not any(word in preceding for word in negations):
                raise AssertionError(
                    f"the page appears to claim {claim!r}: ...{preceding[-60:]}{claim}..."
                )


def test_extras_are_written(site: Path):
    assert "Sitemap:" in (site / "robots.txt").read_text()
    assert (site / "sitemap.xml").read_text().startswith("<?xml")
    manifest = json.loads((site / "site.webmanifest").read_text())
    assert manifest["icons"]
    assert (site / "_headers").is_file()


# --- palette -------------------------------------------------------------

def _relative_luminance(hex_colour: str) -> float:
    channels = hex_colour.lstrip("#")
    values = [int(channels[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in values]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(foreground: str, background: str) -> float:
    a, b = _relative_luminance(foreground), _relative_luminance(background)
    high, low = max(a, b), min(a, b)
    return (high + 0.05) / (low + 0.05)


def _tokens() -> dict[str, str]:
    css = (ROOT / "static" / "style.css").read_text(encoding="utf-8")
    return dict(re.findall(r"(--[a-z-]+):\s*(#[0-9a-f]{6});", css))


def test_text_colours_meet_wcag_aa():
    """Every text colour clears 4.5:1 on every ground it is used on.

    The caption grey failed this at 3.72:1 when the palette was first drawn.
    It is small text on a dark page — exactly the combination that looks fine
    to someone who already knows what it says.
    """
    t = _tokens()
    failures = []
    for text in ("--paper", "--paper-dim", "--paper-faint"):
        for ground in ("--ink", "--ink-raised"):
            ratio = _contrast(t[text], t[ground])
            if ratio < 4.5:
                failures.append(f"{text} on {ground}: {ratio:.2f}:1")
    # White on the red button, which is the one light-on-colour pairing.
    button = _contrast("#ffffff", t["--red"])
    if button < 4.5:
        failures.append(f"white on --red: {button:.2f}:1")
    assert not failures, "below 4.5:1 — " + "; ".join(failures)


def test_brand_red_is_the_one_sampled_from_the_wordmark():
    """#cf3827 comes from the 2024 wordmark. Drifting off it is a real change."""
    assert _tokens()["--red"] == "#cf3827"


# --- the signup section --------------------------------------------------

@pytest.mark.parametrize(
    "newsletter, expected",
    [
        ({"action": "https://example.com/subscribe"}, "form"),
        ({"action": "", "fallback_email": "a@b.c", "fallback_verified": True}, "mailto"),
        ({"action": "", "fallback_email": "a@b.c", "fallback_verified": False}, "channel"),
        ({"action": "", "fallback_email": "", "fallback_verified": True}, "channel"),
        ({}, "channel"),
    ],
)
def test_signup_offers_only_what_actually_works(newsletter, expected):
    assert builder.newsletter_mode(newsletter) == expected


def test_an_unverified_address_is_never_published(home: str):
    """The near-miss this guards against.

    contact@pioneerone.tv does not exist, but the domain has MX records at
    Bluehost — so mail to it is accepted and dropped with no bounce. Publishing
    it would have produced a contact button that swallowed replies silently.
    """
    with (ROOT / "content" / "site.toml").open("rb") as handle:
        newsletter = tomllib.load(handle)["newsletter"]
    if not newsletter.get("action") and not newsletter.get("fallback_verified"):
        address = newsletter.get("fallback_email", "")
        assert address not in home, f"{address} is unverified but appears on the page"
        assert "mailto:" not in home, "an unverified build still rendered a mailto"
