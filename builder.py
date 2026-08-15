"""Build pioneerone.tv into site/.

Reads content/*.toml, renders templates/, copies static/, writes site/. It
reaches nothing over the network and holds no credential, so it runs the same
on a laptop as it does on Cloudflare Pages:

    python builder.py

Images are not derived here — see prepare_assets.py for why. The build is
therefore pure template rendering and a file copy, which is about as little as
can go wrong at deploy time.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tomllib
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
SITE = ROOT / "site"
STAGING = ROOT / "site.tmp"

# Which pages exist, and where each one lands. Clean URLs throughout: every
# page is index.html inside its own directory, so nothing ever ends in .html.
PAGES = [
    ("index.html", Path("index.html"), "home", ""),
    ("story.html", Path("story/index.html"), "story", "../"),
    ("archive.html", Path("archive/index.html"), "archive", "../"),
]


class BuildError(RuntimeError):
    """Raised when the site cannot be built, or would be built wrong."""


def load_toml(name: str) -> dict:
    path = CONTENT / name
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except OSError as error:
        raise BuildError(f"content/{name} is missing or unreadable: {error}") from error
    except tomllib.TOMLDecodeError as error:
        raise BuildError(f"content/{name} is not valid TOML: {error}") from error


def image_widths(stem: str) -> list[int]:
    """The widths actually present on disk for an image stem.

    Read rather than assumed, because prepare_assets.py refuses to upscale: the
    one still that survives only as a small crop has fewer variants than the
    rest, and a srcset promising a file that is not there is a broken image on
    somebody's phone.
    """
    pattern = re.compile(rf"^{re.escape(stem)}-(\d+)\.jpg$")
    widths = sorted(
        int(match.group(1))
        for path in (STATIC / "img").iterdir()
        if (match := pattern.match(path.name))
    )
    if not widths:
        raise BuildError(
            f"no images found for '{stem}' in static/img — run: python prepare_assets.py"
        )
    return widths


def srcset(stem: str, widths: list[int], prefix: str) -> str:
    return ", ".join(f"{prefix}static/img/{stem}-{w}.jpg {w}w" for w in widths)


def display_date(iso: str) -> str:
    """'2010-06-16' -> '16 June 2010'."""
    try:
        parsed = date.fromisoformat(iso)
    except ValueError as error:
        raise BuildError(f"bad date {iso!r} in content/episodes.toml: {error}") from error
    return f"{parsed.day} {parsed:%B} {parsed.year}"


def prepare_episodes(raw: list[dict], prefix: str) -> list[dict]:
    episodes = []
    for entry in sorted(raw, key=lambda e: e["number"]):
        stem = entry["still"]
        widths = image_widths(stem)
        episodes.append(
            {
                # Only two episodes carry a subtitle ("Pilot", "Season Finale").
                # StrictUndefined is deliberate everywhere else, so the optional
                # key is filled in here rather than guarded in the template.
                "subtitle": "",
                **entry,
                "widths": widths,
                "srcset": srcset(stem, widths, prefix),
                "released_display": display_date(entry["released"]),
            }
        )
    if len(episodes) != 6:
        # Not a hard error — a seventh episode would be very good news — but a
        # count that has silently changed is worth saying out loud.
        print(f"  note: {len(episodes)} episodes, expected 6")
    return episodes


def structured_data(site: dict, episodes: list[dict], watch: dict) -> str:
    """schema.org TVSeries, so search results describe a show and not a blog."""
    base = site["canonical_url"].rstrip("/")
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "TVSeries",
            "name": site["name"],
            "description": site["description"],
            "url": base + "/",
            "image": f"{base}/static/img/social-card.jpg",
            "genre": ["Science Fiction", "Drama"],
            "numberOfSeasons": 1,
            "numberOfEpisodes": len(episodes),
            "datePublished": episodes[0]["released"] if episodes else None,
            "creator": [
                {"@type": "Person", "name": "Josh Bernhard"},
                {"@type": "Person", "name": "Bracey Smith"},
            ],
            "containsSeason": {
                "@type": "TVSeason",
                "seasonNumber": 1,
                "numberOfEpisodes": len(episodes),
                "episode": [
                    {
                        "@type": "TVEpisode",
                        "episodeNumber": ep["number"],
                        "name": ep["title"],
                        "description": ep["synopsis"],
                        "datePublished": ep["released"],
                        "url": f"https://www.youtube.com/watch?v={ep['youtube']}",
                    }
                    for ep in episodes
                ],
            },
            "sameAs": [watch["channel_url"], watch["archive_org_url"]],
        },
        indent=2,
    ).replace("<", r"\u003c")  # cannot break out of the <script> that carries it


def write_extras(out: Path, site: dict) -> None:
    base = site["canonical_url"].rstrip("/")

    (out / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8"
    )

    urls = "".join(
        f"  <url><loc>{base}/{path}</loc></url>\n"
        for path in ("", "story/", "archive/")
    )
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n",
        encoding="utf-8",
    )

    (out / "site.webmanifest").write_text(
        json.dumps(
            {
                "name": site["name"],
                "short_name": site["name"],
                "description": site["description"],
                "start_url": "/",
                "display": "standalone",
                "background_color": "#0b0b0c",
                "theme_color": "#0b0b0c",
                "icons": [
                    {"src": "/static/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                    {"src": "/static/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Cloudflare Pages reads this. Long-lived caching for fingerprint-free but
    # never-changing assets (fonts, the recovered stills); the HTML stays fresh.
    (out / "_headers").write_text(
        "/static/fonts/*\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "/static/img/*\n"
        "  Cache-Control: public, max-age=604800\n"
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n",
        encoding="utf-8",
    )


def build(site_dir: Path | None = None) -> Path:
    site_dir = site_dir or SITE
    staging = STAGING if site_dir == SITE else site_dir.with_name(site_dir.name + ".tmp")

    site_cfg = load_toml("site.toml")
    episodes_cfg = load_toml("episodes.toml")

    site = site_cfg["site"]
    watch = site_cfg["watch"]
    newsletter = site_cfg["newsletter"]
    laurels = episodes_cfg["laurel"]

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html"]),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    shutil.copytree(STATIC, staging / "static")

    base = site["canonical_url"].rstrip("/")
    hero_widths = image_widths("hero")

    for template_name, out_path, page, rel in PAGES:
        episodes = prepare_episodes(episodes_cfg["episode"], rel)
        html = env.get_template(template_name).render(
            site=site,
            watch=watch,
            newsletter=newsletter,
            episodes=episodes,
            laurels=laurels,
            page=page,
            rel=rel,
            canonical=f"{base}/{out_path.parent.as_posix() + '/' if out_path.parent.name else ''}",
            hero_srcset=srcset("hero", hero_widths, rel),
            schema=structured_data(site, episodes, watch),
        )
        destination = staging / out_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding="utf-8")
        print(f"  {out_path.as_posix()}  ({len(html) / 1024:.1f} KB)")

    write_extras(staging, site)

    # Swap only once everything rendered, so a failed build never leaves a
    # half-written site behind for the dev server to serve.
    if site_dir.exists():
        shutil.rmtree(site_dir)
    staging.rename(site_dir)
    return site_dir


def main() -> int:
    print("Building Pioneer One")
    try:
        out = build()
    except BuildError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    total = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    print(f"Done. {out.relative_to(ROOT)}/ — {total / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
