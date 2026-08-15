# Every factual claim on the site, and where it comes from

The site states a number of specific things — dollar amounts, download counts,
dates, awards. This file says where each came from, so any of it can be
checked or corrected. Almost all of it traces to Pioneer One's own writing,
recovered from the Wayback Machine.

Three primary sources do most of the work:

- **The production's own YouTube episode descriptions**, on the channel today.
  This is Josh's current copy and the strongest source available: it names the
  cast, calls the capsule's occupant a boy, and gives the season's funding
  figures. Added as a source on 2026-08-15.

- **"The Future of PIONEER ONE"**, `pioneerone.tv`, June 18, 2016. Josh
  Bernhard's own six-year retrospective. Recovered as article
  `2016-06-18-the-future-of-pioneer-one` in the `palimpsest` archive.
- **The site's own RSS feed**, captured 2015–2016, which carries the full text
  of the episode pages including synopses and release dates.

The last two are held locally in the `palimpsest` archive on ppmanchester at
`~/Development/palimpsest/archive/articles/`.

## Claims

| Claim on the site | Source | Confidence |
|---|---|---|
| A **boy**, not a man, is found in the capsule | Episode 1 description: "a boy of mysterious origin is recovered from inside the capsule"; the production's social copy: "A Boy from Mars Fell to Earth" | Certain |
| He says he was **born on Mars** | Episode 6 description: Yuri is "the child of two Soviet cosmonauts who were stranded on Mars in the 1980s"; episode 2: "may have been born on Mars" | Certain |
| Roughly **$100,000** in fan donations funded the season | The site's own About page and every episode description: "fans donated $100,000 to fund the rest of the 6-episode first season" | Certain |
| Released under a **Creative Commons BY-NC-SA** license | The Internet Archive's copy of the VODO season-one release states the license | Certain |
| Produced by **LastSat Productions LLC** | Footer of the original site | Certain |
| Six full-length episodes, one complete season | Episode pages 1–6, site feed | Certain |
| $6,000 raised on Kickstarter for the pilot | 2016 retrospective, verbatim | Certain |
| Pilot released June 16, 2010 via VODO/BitTorrent | 2016 retrospective; "Watch the Pilot now!", June 16, 2010 | Certain |
| Downloaded over 2,000,000 times in two weeks | 2016 retrospective: "Within two weeks the pilot was downloaded over 2,000,000 times" | Certain |
| ~$20,000 in donations in the same period | 2016 retrospective, verbatim | Certain |
| $30,000 total funded episodes 2–4, shot together in October 2010 | "And Now, For Our Next Trick…", Nov 28, 2010 | Certain |
| Cast and crew largely worked unpaid | 2016 retrospective; "Season 2 and beyond", Dec 14, 2011 | Certain |
| Previous film *The Lionshare*, also via VODO | "Pioneer One" project description, Apr 1, 2010 | Certain |
| Best Drama Pilot, New York Television Festival 2010 | Production's own laurel image; "'Pioneer One' Wins for Best Drama Pilot!", Sep 25, 2010 | Certain |
| Pilot aired on NYC-TV, November 2011 | "Pilot to air on NYC TV Life", Nov 3, 2011 (broadcast 4 Nov) | Certain |
| Webby Awards 2012: Best Drama nominee; Best Writing honoree | Production's own laurel images; "Webby Awards Nomination", Apr 10, 2012 | Certain |
| Over four million downloads by April 2012 | Official YouTube channel description: "over 4.1 million completed downloads as of April, 2012" | High |
| Finale premiered at Anthology Film Archives, Dec 5, 2011 | "Season Finale Premiere Event December 5", Nov 12, 2011 | Certain |
| Episode 6 released December 13, 2011 | See "The one date I corrected" below | High |
| Four hard drives failed the night before a release | 2016 retrospective, verbatim | Certain |
| A car hit a deer driving back from a night shoot | 2016 retrospective, verbatim | Certain |
| 32 behind-the-scenes video blogs | "DVD and Blu Ray on sale now", Apr 20, 2012, listing special features | Certain |
| Josh moved to LA to edit and write; Bracey moved into VR | 2016 retrospective | Certain |
| Roughly a decade of development, none of it made | 2016 retrospective, plus Josh's account in the brief for this site | Certain |
| A producer in LA and an established TV director came aboard | 2016 retrospective (names deliberately omitted) | Certain |

## Two figures I revised on 2026-08-15

**Donations.** The site first said $20,000, from the 2016 retrospective. That
figure is real but partial — it is the first two weeks only. The production's
own About page and episode descriptions give **$100,000** across the season.
Both now appear, in that order, because the two-week number is the startling
one and the total is the true one.

**"Man" became "boy".** The first draft called the capsule's occupant a man,
which is wrong and was never the show's word for him. Corrected everywhere. The
episode title "The Man From Mars" is left alone — that is the episode's actual
title.

## The one date I corrected

The site's own episode 6 page says "Originally released December 13, **2012**".
That is wrong, and the page contradicts itself: it was published on
November 16, 2012, so it cannot have been describing a release a month in its
own future as something that had already happened.

Three contemporaneous posts give 2011:

- Nov 14, 2011 — "Episode 6, titled 'War of the World', will be released on
  **December 13**."
- Nov 12, 2011 — the finale premiere is announced for December 5, 2011.
- Dec 14, 2011 — "Season 2 and beyond" opens "the first season of *Pioneer One*
  is complete."

`content/episodes.toml` therefore records `2011-12-13`.

## Deliberately not claimed

- **No collaborator from the development years is named.** Their involvement is
  described; the names are Josh's to publish.
- **No credit reading "created by".** The production settled on *developed by
  Josh Bernhard and Bracey Smith*, and that is what the site says. "Created by"
  is Josh's own credit and does not describe Bracey's part.
- **Nothing about the feature film or a second season** beyond that they are
  being worked on and thought about. The "Now" section says outright that
  nothing is financed or greenlit.
- **No claim that the show was "the first" anything.** Wikipedia and
  contemporary press describe it as the first series made for and released on
  BitTorrent. That is very likely true and it is not on the site, because the
  page does not need it and it is the kind of claim that invites an argument.

## Credits: where each name came from

The original site's `/about/cast/` and `/about/crew/` pages were published
empty and never filled in, so there is no authoritative list to recover.
`content/credits.toml` records a `source` for every person:

- **`channel`** — named in the production's own YouTube episode descriptions.
  Six cast members and the writer/director credits. Treat as solid.
  James Rich (Tom Taylor), Aleksandr Evtushenko (Yuri), Jack Haley
  (Dr. Zachary Walzer), Laura Graham (Jane Campbell), Einar Gunn (Secretary
  Eric McClellan), Jean Neftin (Aleksei Chertov).
- **`blog`** — named in a pioneerone.tv post at the time. From "Money stuff and
  other business", April 26, 2010: Bracey Smith on visual effects, Alice Millar
  editing, Dan Coletta on sound.
- **`wikipedia`** — listed on the Wikipedia article and not corroborated by
  anything the production wrote. **These need checking:** Alexandra Blatt
  (Sofie Larson), Guy Wegener (Vernon), E. James Ford (Dileo), Laurence Cantor
  (Norton), Matthew Foster (Walzer in the original pilot), Ari Meisel
  (executive producer), Louis Meisel (producer), and the shooting locations.

Note also: Wikipedia spells the character **Sofie** Larson, TVmaze spells it
**Sophie**. The site uses Sofie.

This list is certainly incomplete. Everyone who worked on the show unpaid has a
claim to being on it.

## Mistakes made and corrected

Recorded so the same shape of error is easier to spot next time.

1. **A still from the wrong show.** A control-room frame was published as a
   Pioneer One production still. It is from *Control*, the 2012 pilot by the
   same team. Both unverified frames were withdrawn. See
   `assets-src/SOURCES.md`.
2. **Reconstructed credits.** A cast and crew list assembled from Wikipedia and
   the YouTube descriptions was wrong. Withdrawn; see `content/credits.toml`.
3. **"Man" for "boy"**, corrected from the production's own copy.
4. **$20,000 presented as the total**, when it was the first two weeks of a
   figure that reached $100,000.

The common thread is publishing something plausible in place of something
checked. Where a claim cannot be sourced to the production's own words, it
should not be on the site.

## For Josh to confirm

1. **The credits above**, particularly the `wikipedia`-sourced names and
   anybody missing entirely. This is the item most worth thirty seconds.
2. **Episode 2's release date.** Its page says December 15, 2010; the
   announcement post is dated the 16th. The site uses the 15th.
3. **The feature.** The site says only that you are writing it, and names
   nobody else. Earlier notes mentioned a friend directing; that is not on the
   site.
4. **A documentary** about making the series is in `PARKING_LOT.md` as a future
   possibility, not on the site. Say the word if it should be in "Now".
5. **`contact@pioneerone.tv`** does not exist, and the domain accepts and drops
   mail for it. The signup section currently offers the YouTube channel
   instead. See `deploy/README.md` step 6.
