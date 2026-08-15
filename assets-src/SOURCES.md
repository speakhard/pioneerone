# Where these files came from

Every image in this directory was published by the Pioneer One production
itself and was recovered from the Internet Archive's capture of
`pioneerone.tv`. Nothing here was generated, and nothing was sourced from a
third party.

The live site sits behind a Cloudflare interstitial, so recovery went through
the Wayback Machine rather than the origin. No attempt was made to defeat the
challenge. This mirrors the approach taken by the wider `palimpsest` archive
project, which holds the full text corpus for this domain.

Retrieved 2026-08-15. Wayback raw-content URLs take the form
`https://web.archive.org/web/<timestamp>id_/<original>`.

| File | Original URL | Wayback timestamp |
|---|---|---|
| `ep1-full.png` | `/wp-content/uploads/2015/01/ep1-a.png` | 20160311103026 |
| `ep2.png` | `/wp-content/uploads/2012/11/episode-2-a-825x464.png` | 20160602234823 |
| `ep3.png` | `/wp-content/uploads/2015/01/ep3-a-825x464.png` | 20160602235537 |
| `ep4.png` | `/wp-content/uploads/2015/01/ep4-825x464.png` | 20160602233858 |
| `ep5.png` | `/wp-content/uploads/2015/01/ep5-825x464.png` | 20160602234053 |
| `ep6-small.png` | `/wp-content/uploads/2015/01/ep6-420x300.png` | 20161030101623 |
| `featured-video.jpg` | `/wp-content/uploads/2015/01/p1-tv-featured-video.jpg` | 20150213112842 |
| `header2024.png` | `/wp-content/uploads/2024/10/p1.tv-header-small-cropped.png` | 20241227081225 |
| `icon2024.png` | `/wp-content/uploads/2024/12/p1tv-icon-5.png` | 20241227081243 |
| `header2011.png` | `/wp-content/uploads/2011/03/site_header_mar2011_flat1.png` | 20110526050643 |
| `p1-title-big.png` | `/wp-content/uploads/2015/01/p1-title-big.png` | 20150213112340 |
| `laurel-nytvf.png` | `/wp-content/uploads/2015/02/laurels-nytvf-243.png` | 20150213102227 |
| `laurel-webbydrama.png` | `/wp-content/uploads/2015/02/laurels-webbydrama-243.png` | 20150213101439 |
| `laurel-webbywriting.png` | `/wp-content/uploads/2015/02/laurels-webbywriting-243.png` | 20150213102422 |
| `laurel-iawtv.png` | `/wp-content/uploads/2015/02/laurels-iawtv-243.png` | 20150213112344 |
| `vlc-a.png` | `/wp-content/uploads/2012/11/vlcsnap-2015-01-26-13h11m22s169-825x464.png` | 20160602235039 |
| `vlc-b.png` | `/wp-content/uploads/2012/11/vlcsnap-2015-01-28-14h44m31s215-825x464.png` | 20160602235346 |

## Notes

**Episode stills.** The episode a still belongs to is taken from the filename
the production gave it (`ep3-a`, `episode-2-a`, and so on), not from a guess
about its content.

**Episode 6.** Only the 420&times;300 crop was ever archived; the full-size
original is not in the Wayback Machine at any timestamp. It is therefore the
one still the site serves below its ideal resolution. `prepare_assets.py`
refuses to upscale it. If the original turns up on a drive, drop it in as
`ep6-full.png`, point `EPISODE_STILLS` at it, and re-run.

**Not used by the site.** `vlc-a.png` (a mission-control room) and `vlc-b.png`
(a press conference) are held here because they are good frames, but they are
not published: nothing establishes which episodes they come from, and captions
that guess are how an archive starts lying.

**`p1-title-big.png`** is the lighter 2015 title treatment. The site uses the
2024 wordmark instead, as the most recent identity the production settled on.
