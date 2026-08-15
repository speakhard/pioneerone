"""Assert that everything in a text column shares one left edge.

Alignment is the kind of thing that looks fine until someone with an eye for it
opens the page, and then cannot be unseen. Eyeballing a screenshot is not good
enough — a few pixels of drift is both clearly visible and easy to miss. So the
left edge of every block in the reading column is measured and compared.

    python serve.py &
    python check_alignment.py
"""
from __future__ import annotations

import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8791"

# Per page: the selectors whose left edges must agree.
COLUMNS = {
    "/story/": [
        ".page-head .eyebrow",
        ".page-head h1",
        ".page-head .standfirst",
        ".article > p",
        ".article > h2",
        ".article > .pull",
        ".article > ul",
    ],
    "/": [
        ".facts .shell",
        "#watch .shell",
        "#now .shell",
    ],
}

WIDTHS = [(1600, 1000), (1280, 800), (393, 852)]
TOLERANCE = 1.0  # px; sub-pixel rounding is not a defect


def main() -> int:
    failures = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width, height in WIDTHS:
            page = browser.new_page(viewport={"width": width, "height": height})
            for path, selectors in COLUMNS.items():
                page.goto(BASE + path, wait_until="load")
                edges = page.evaluate(
                    """(selectors) => selectors.map(sel => {
                        const el = document.querySelector(sel);
                        if (!el) return [sel, null];
                        // Box edges, not text edges. A pull quote's rule is meant
                        // to sit on the column edge with its text indented past
                        // it; measuring the text would call that correct design a
                        // 26px error.
                        return [sel, Math.round(el.getBoundingClientRect().left * 10) / 10];
                    })""",
                    selectors,
                )
                found = [(s, x) for s, x in edges if x is not None]
                missing = [s for s, x in edges if x is None]
                if missing:
                    failures.append(f"{width}px {path}: selector matched nothing: {missing}")
                if len(found) < 2:
                    continue
                base = found[0][1]
                off = [(s, x) for s, x in found if abs(x - base) > TOLERANCE]
                if off:
                    detail = ", ".join(f"{s} at {x}px" for s, x in off)
                    failures.append(
                        f"{width}px {path}: column starts at {base}px but {detail}"
                    )
                else:
                    print(f"  ok  {width:>4}px {path:<11} {len(found)} blocks aligned at {base}px")
            page.close()
        browser.close()

    for failure in failures:
        print("  MISALIGNED:", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
