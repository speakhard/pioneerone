"""Render the built site at real device sizes and save screenshots.

Not a test — an eye. `python builder.py` proves the HTML was written; this
proves it looks like something. Run the dev server first:

    python -m http.server 8791 --directory site
    python shoot.py [outdir]
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8791"

# iPhone 14 Pro logical size, a small Android, a laptop, a large desktop.
DEVICES = [
    ("phone", 393, 852, 3),
    ("phone-small", 360, 740, 3),
    ("laptop", 1280, 800, 2),
    ("desktop", 1600, 1000, 2),
]

PAGES = [("home", "/"), ("story", "/story/")]


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "shots")
    out.mkdir(parents=True, exist_ok=True)
    problems = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for device, width, height, dpr in DEVICES:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=1,  # 1x keeps the files readable; layout is what matters
                is_mobile=device.startswith("phone"),
                has_touch=device.startswith("phone"),
                user_agent=(
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
                    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
                    if device.startswith("phone")
                    else None
                ),
            )
            page = context.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))

            for name, path in PAGES:
                page.goto(BASE + path, wait_until="networkidle")

                # Walk the page so loading="lazy" images actually fetch. Without
                # this a full-page screenshot shows blank frames where the
                # episode stills should be, and the site gets blamed for it.
                page.evaluate(
                    """async () => {
                        const settle = ms => new Promise(r => setTimeout(r, ms));

                        // Opt every image out of lazy loading before doing
                        // anything else. Scrolling past a lazy image is not
                        // enough — at screenshot speed the intersection
                        // observer may not fire before we have scrolled away
                        // again, and the image then reports as failed when it
                        // simply never started.
                        document.querySelectorAll("img[loading=lazy]")
                            .forEach(i => { i.loading = "eager"; });

                        const step = window.innerHeight * 0.8;
                        const end = document.body.scrollHeight;
                        for (let y = 0; y < end; y += step) {
                            window.scrollTo(0, y);
                            await settle(40);
                        }
                        window.scrollTo(0, 0);
                        // Bounded: an image that never fires load or error must
                        // not hang the run, it must be reported as broken.
                        await Promise.race([
                            Promise.all([...document.images]
                                .filter(i => !i.complete)
                                .map(i => new Promise(r => { i.onload = i.onerror = r; }))),
                            settle(4000),
                        ]);
                    }"""
                )
                page.wait_for_timeout(350)

                broken = page.evaluate(
                    "() => [...document.images].filter(i => !i.naturalWidth).map(i => i.currentSrc || i.src)"
                )
                if broken:
                    problems.append(f"{device}/{name}: images failed to load: {broken}")
                page.screenshot(path=out / f"{device}-{name}-fold.png")
                page.screenshot(path=out / f"{device}-{name}-full.png", full_page=True)

                # Horizontal overflow is the classic mobile failure and is
                # invisible in a screenshot that has already been clipped.
                overflow = page.evaluate(
                    "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"
                )
                if overflow > 1:
                    problems.append(f"{device}/{name}: {overflow}px horizontal overflow")

            if errors:
                problems.append(f"{device}: console errors: {errors[:3]}")
            context.close()
        browser.close()

    print(f"shots -> {out}/")
    for problem in problems:
        print("  PROBLEM:", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
