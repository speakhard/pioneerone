# Every factual claim on the site, and where it comes from

The site states a number of specific things — dollar amounts, download counts,
dates, awards. This file says where each came from, so any of it can be
checked or corrected. Almost all of it traces to Pioneer One's own writing,
recovered from the Wayback Machine.

Two primary sources do most of the work:

- **"The Future of PIONEER ONE"**, `pioneerone.tv`, 18 June 2016. Josh
  Bernhard's own six-year retrospective. Recovered as article
  `2016-06-18-the-future-of-pioneer-one` in the `palimpsest` archive.
- **The site's own RSS feed**, captured 2015–2016, which carries the full text
  of the episode pages including synopses and release dates.

Both are held locally in the `palimpsest` archive on ppmanchester at
`~/Development/palimpsest/archive/articles/`.

## Claims

| Claim on the site | Source | Confidence |
|---|---|---|
| Six full-length episodes, one complete season | Episode pages 1–6, site feed | Certain |
| $6,000 raised on Kickstarter for the pilot | 2016 retrospective, verbatim | Certain |
| Pilot released 16 June 2010 via VODO/BitTorrent | 2016 retrospective; "Watch the Pilot now!", 16 June 2010 | Certain |
| Downloaded over 2,000,000 times in two weeks | 2016 retrospective: "Within two weeks the pilot was downloaded over 2,000,000 times" | Certain |
| ~$20,000 in donations in the same period | 2016 retrospective, verbatim | Certain |
| $30,000 total funded episodes 2–4, shot together in October 2010 | "And Now, For Our Next Trick…", 28 Nov 2010 | Certain |
| Cast and crew largely worked unpaid | 2016 retrospective; "Season 2 and beyond", 14 Dec 2011 | Certain |
| Previous film *The Lionshare*, also via VODO | "Pioneer One" project description, 1 Apr 2010 | Certain |
| Best Drama Pilot, New York Television Festival 2010 | Production's own laurel image; "'Pioneer One' Wins for Best Drama Pilot!", 25 Sep 2010 | Certain |
| Pilot aired on NYC-TV, November 2011 | "Pilot to air on NYC TV Life", 3 Nov 2011 (broadcast 4 Nov) | Certain |
| Webby Awards 2012: Best Drama nominee; Best Writing honoree | Production's own laurel images; "Webby Awards Nomination", 10 Apr 2012 | Certain |
| Over four million downloads by April 2012 | Official YouTube channel description: "over 4.1 million completed downloads as of April, 2012" | High |
| Finale premiered at Anthology Film Archives, 5 Dec 2011 | "Season Finale Premiere Event December 5", 12 Nov 2011 | Certain |
| Episode 6 released 13 December 2011 | See "The one date I corrected" below | High |
| Four hard drives failed the night before a release | 2016 retrospective, verbatim | Certain |
| A car hit a deer driving back from a night shoot | 2016 retrospective, verbatim | Certain |
| 32 behind-the-scenes video blogs | "DVD and Blu Ray on sale now", 20 Apr 2012, listing special features | Certain |
| Josh moved to LA to edit and write; Bracey moved into VR | 2016 retrospective | Certain |
| Roughly a decade of development, none of it made | 2016 retrospective, plus Josh's account in the brief for this site | Certain |
| A producer in LA and an established TV director came aboard | 2016 retrospective (names deliberately omitted) | Certain |

## The one date I corrected

The site's own episode 6 page says "Originally released December 13, **2012**".
That is wrong, and the page contradicts itself: it was published on
16 November 2012, so it cannot have been describing a release a month in its
own future as something that had already happened.

Three contemporaneous posts give 2011:

- 14 Nov 2011 — "Episode 6, titled 'War of the World', will be released on
  **December 13**."
- 12 Nov 2011 — the finale premiere is announced for 5 December 2011.
- 14 Dec 2011 — "Season 2 and beyond" opens "the first season of *Pioneer One*
  is complete."

`content/episodes.toml` therefore records `2011-12-13`.

## Deliberately not claimed

- **No collaborator from the development years is named.** Their involvement is
  described; the names are Josh's to publish.
- **No cast or crew credits**, beyond Josh Bernhard and Bracey Smith as
  creators, who are named throughout the production's own material.
- **Nothing about the feature film or a second season** beyond that they are
  being worked on and thought about. The "Now" section says outright that
  nothing is financed or commissioned.
- **No claim that the show was "the first" anything.** Wikipedia and
  contemporary press describe it as the first series made for and released on
  BitTorrent. That is very likely true and it is not on the site, because the
  page does not need it and it is the kind of claim that invites an argument.

## For Josh to confirm

1. **`contact@pioneerone.tv`** is used as the signup fallback. Does it still
   route to you? If not, change `newsletter.fallback_email` in
   `content/site.toml`, or set `newsletter.action` to a real list endpoint.
2. **Episode 2's release date.** Its page says 15 December 2010; the
   announcement post is dated the 16th. The site uses the 15th.
3. **The feature.** The site says a friend would direct and does not name them.
