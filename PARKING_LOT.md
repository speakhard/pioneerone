# Parking lot

Things deliberately not done for the weekend MVP. Nothing here is a defect;
each was a decision to keep the homepage finishable.

## The archive

Cut from the site entirely on 2026-08-15, not deferred. An archive page only
earns its place as material for something — a documentary about making the
series is the obvious candidate — and nobody has committed to that, so the
site does not promise it. If the documentary becomes real, this material is
its source and the page comes back in that context.

Known to exist:

- 32 behind-the-scenes video blogs made during production
- Scripts at several drafts
- Stills and production photography
- Artwork
- Cut and alternate footage, including the episode 3 rough cut with ~20 minutes
  of excised footage (per the 2012 DVD feature list)
- Cast commentary tracks for every episode
- Subtitles in English, Spanish, French, Italian and Swedish
- Contemporary press
- Development-era drafts, treatments and pitch material from 2012–2022

Doing this properly means cataloging, confirming what may be shared, and
presenting it well. It is a project, not a page. The site is already structured
for it: episodes are data, not markup.

## Per-episode pages

`/watch/episode-1/` and so on, each with the full synopsis, credits, a
transcript, the commentary track and the relevant video blogs. Wanted for SEO
as much as for readers — six pages that can rank for their own titles. Needs
the archive first, or it is six thin pages.

## Redirects for the old permalinks

The 2010–2012 site used `/YYYY/MM/DD/slug/`. There are live inbound links to
those from TorrentFreak and elsewhere, and they will 404 after the switch.

Deliberately deferred: sending them all to `/` is worse than a 404, because it
tells the visitor the page is gone *and* wastes their tap. When the archive
gives those posts somewhere real to land, a `_redirects` file maps them
properly. The full list of old URLs is recoverable from the CDX index in the
palimpsest archive.

## A real mailing list

`newsletter.action` in `content/site.toml` is one line away from a working
form. Left as a mailto because signing Josh up to a service is his decision,
not the site's.

## Episode 6's still

Only the 420×300 crop was ever archived; the original is not in the Wayback
Machine at any timestamp. If it turns up on a drive, drop it into
`assets-src/` and re-run `prepare_assets.py`.

## Considered and rejected

- **Self-hosting the video.** The episodes are already on the production's own
  YouTube channel and at the Internet Archive. Building a player would be a
  weekend on its own and would serve nobody better.
- **Embedding six iframes directly.** Megabytes and third-party cookies on the
  page most likely to be opened on mobile data. The click-to-play facade costs
  ~30 lines and one extra tap.
- **Using the YouTube episode thumbnails as card art.** They are official, but
  they carry the episode number and title burned in, which the card already
  says in text. The clean stills from the original site are better pictures.
- **Naming the development-era collaborators.** Their involvement is described
  on `/story/`; the names are Josh's to publish, not the site's.
- **Analytics.** None added. Nothing on the site needs to know who visited.
