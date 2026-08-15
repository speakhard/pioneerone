"""Turn the recovered originals in assets-src/ into the derivatives the site serves.

This is run by hand, not at deploy time, and its output is committed. The
reasoning: the originals were recovered once from the Wayback Machine and will
not change, so re-deriving them on every Cloudflare build would add Pillow to
the deploy path and a network dependency to the archive, in exchange for
nothing. Provenance for every source file is in assets-src/SOURCES.md.

    python prepare_assets.py

Safe to re-run; it overwrites its own output and touches nothing else.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
SRC = ROOT / "assets-src"
OUT = ROOT / "static" / "img"

# The identity, sampled from the 2024 wordmark and icon the site last carried.
RED = (207, 56, 39)
INK = (11, 11, 12)

# Episode still -> the file Josh's own WordPress upload names identify it as.
EPISODE_STILLS = {
    1: "ep1-full.png",
    2: "ep2.png",
    3: "ep3.png",
    4: "ep4.png",
    5: "ep5.png",
    6: "ep6-small.png",
}

# Card widths. 880 covers a two-up desktop card on a 2x display; 440 covers a
# phone. Anything larger is wasted bytes on the page that matters most.
CARD_WIDTHS = (880, 440)
HERO_WIDTHS = (2000, 1400, 900, 560)


def load(name: str) -> Image.Image:
    """Open a source image flattened onto black.

    Several of the recovered PNGs carry an alpha channel that is fully opaque.
    Flattening rather than converting keeps any genuinely transparent edge from
    turning white when it is saved as JPEG.
    """
    im = Image.open(SRC / name)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        base = Image.new("RGB", im.size, INK)
        base.paste(im, mask=im.split()[-1])
        return base
    return im.convert("RGB")


def crop_to(im: Image.Image, ratio: float) -> Image.Image:
    """Center-crop to an aspect ratio, taking the width or height as needed."""
    w, h = im.size
    if w / h > ratio:
        new_w = round(h * ratio)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = round(w / ratio)
    # Bias slightly above center: faces sit in the upper half of most of these
    # frames, and a true center crop cuts foreheads.
    top = int((h - new_h) * 0.4)
    return im.crop((0, top, w, top + new_h))


def save_widths(im: Image.Image, stem: str, widths, quality: int = 82) -> list[str]:
    """Write one JPEG per requested width, never upscaling.

    A width larger than the source collapses to the source's own width instead
    of being dropped, so a 825px still still gets its full-resolution variant
    and only genuinely invented detail is refused.
    """
    wanted = sorted({min(w, im.width) for w in widths}, reverse=True)
    written = []
    for width in wanted:
        scaled = im if width == im.width else im.resize(
            (width, round(im.height * width / im.width)), Image.LANCZOS
        )
        path = OUT / f"{stem}-{width}.jpg"
        scaled.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
        written.append(path.name)
    return written


def build_episode_cards() -> dict[int, list[int]]:
    made = {}
    for number, filename in EPISODE_STILLS.items():
        im = crop_to(load(filename), 16 / 9)
        names = save_widths(im, f"ep{number}", CARD_WIDTHS)
        made[number] = sorted(int(n.rsplit("-", 1)[1][:-4]) for n in names)
        print(f"  episode {number}: {', '.join(names)}")
    return made


def build_hero() -> None:
    im = crop_to(load("ep1-full.png"), 16 / 9)
    print("  hero:", ", ".join(save_widths(im, "hero", HERO_WIDTHS, quality=80)))



def build_keyart() -> None:
    im = crop_to(load("featured-video.jpg"), 16 / 9)
    print("  keyart:", ", ".join(save_widths(im, "keyart", (1200, 700))))


# vlc-a.png and vlc-b.png are deliberately not derived. See assets-src/SOURCES.md:
# one of them turned out to be from Control, a different show by the same
# people, and the other cannot be told apart from it.


def build_social_card() -> None:
    """Compose the 1200x630 OpenGraph card: the hero frame, the real wordmark.

    Social previews are the first thing most people will see of this site, so
    the card is composed rather than borrowed from a page image — but only from
    assets the production actually produced.
    """
    W, H = 1200, 630
    card = crop_to(load("ep1-full.png"), W / H).resize((W, H), Image.LANCZOS)

    # The frame is a bright red flight-suit patch, and the wordmark's own red
    # disappears against it. Two scrims fix that: an overall knock-down so the
    # image reads as a backdrop, and a bottom-weighted one giving the type a
    # genuinely dark bed. Measured, not guessed — see the contrast check below.
    black = Image.new("RGB", (W, H), INK)
    card = Image.blend(card, black, 0.34)

    shade = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(shade)
    for y in range(H):
        t = max(0.0, (y - H * 0.30) / (H * 0.70))
        draw.line([(0, y), (W, y)], fill=int(232 * t**1.35))
    card = Image.composite(black, card, shade)

    mark = Image.open(SRC / "header2024.png").convert("RGBA")
    mark = mark.resize((560, round(mark.height * 560 / mark.width)), Image.LANCZOS)
    mark_x, mark_y = 76, H - mark.height - 104

    # Sample the bed the type will sit on *before* pasting it — measuring after
    # would average in the wordmark's own red and white and report nonsense.
    bed = card.crop((mark_x, mark_y, mark_x + mark.width, mark_y + mark.height))
    pixels = list(bed.convert("RGB").getdata())
    mean = tuple(sum(p[i] for p in pixels) // len(pixels) for i in range(3))

    card.paste(mark, (mark_x, mark_y), mark)
    rule = ImageDraw.Draw(card)
    rule.rectangle([mark_x, mark_y + mark.height + 30, mark_x + 88, mark_y + mark.height + 34], fill=RED)
    card.save(OUT / "social-card.jpg", "JPEG", quality=88, optimize=True, progressive=True)

    verdict = "ok" if max(mean) < 90 else "TOO LIGHT — the wordmark will not read"
    print(f"    backdrop under wordmark: rgb{mean} — {verdict}")
    print("  social card: social-card.jpg")


def build_icons() -> None:
    """Favicons and app icons from the 2024 'p1' mark."""
    icon = Image.open(SRC / "icon2024.png").convert("RGBA")

    for size in (192, 512):
        icon.resize((size, size), Image.LANCZOS).save(OUT / f"icon-{size}.png", optimize=True)

    # Apple touch icons are composited on white if they carry alpha, and the
    # mark is dark-on-dark, so it gets its own opaque background.
    touch = Image.new("RGB", (180, 180), INK)
    scaled = icon.resize((180, 180), Image.LANCZOS)
    touch.paste(scaled, (0, 0), scaled)
    touch.save(OUT / "apple-touch-icon.png", optimize=True)

    frames = [icon.resize((s, s), Image.LANCZOS) for s in (16, 32, 48)]
    frames[0].save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  icons: favicon.ico, apple-touch-icon.png, icon-192.png, icon-512.png")


def build_wordmark() -> None:
    """The authentic wordmark, passed through untouched but re-optimised."""
    for name, out in (("header2024.png", "wordmark.png"), ("header2011.png", "wordmark-2011.png")):
        im = Image.open(SRC / name).convert("RGBA")
        im.save(OUT / out, optimize=True)
    print("  wordmark: wordmark.png, wordmark-2011.png")


def build_laurels() -> None:
    for name in ("nytvf", "webbydrama", "webbywriting", "iawtv"):
        im = Image.open(SRC / f"laurel-{name}.png").convert("RGBA")
        im.save(OUT / f"laurel-{name}.png", optimize=True)
    print("  laurels: 4 files")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Deriving site assets from", SRC.name)
    build_hero()
    build_episode_cards()
    build_keyart()
    build_social_card()
    build_icons()
    build_wordmark()
    build_laurels()
    total = sum(p.stat().st_size for p in OUT.iterdir() if p.is_file())
    print(f"Done. {len(list(OUT.iterdir()))} files, {total / 1024:.0f} KB in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
