---
schema: devtracker/current-state@1
project: pioneerone
status: MVP built and verified locally, pushed private. Blocked only on Cloudflare/Bluehost access for the deploy.
milestone:
  current: M1 complete — weekend MVP built, verified locally, committed and pushed private to speakhard/pioneerone (d4fc748)
  next: M2 — Cloudflare Pages project and custom domain; then the archive
goal: 'pioneerone.tv presents Pioneer One as a show worth watching now: cinematic, credible, present-tense, and excellent on a phone'
definition_of_done: Responsive site with a polished homepage, all six episodes watchable, concise Story and Now sections, correct social/SEO metadata, no placeholders beyond the deliberately deferred Archive, and deployed to the domain
next_task: "Josh: create the Cloudflare Pages project against speakhard/pioneerone (build 'pip install -r requirements.txt && python builder.py', output 'site'), verify on the pages.dev preview, then attach pioneerone.tv. Steps and rollback are in deploy/README.md"
estimated_remaining: About an hour of Josh's dashboard time to go live
blockers:
  - Deployment to pioneerone.tv requires Cloudflare and Bluehost dashboard access, which this machine does not have
risks:
  - The domain is on Bluehost nameservers with Cloudflare proxying, so pointing it at Pages means either moving the zone or splitting DNS across two providers
  - The live WordPress/WooCommerce install is the only copy of whatever has accumulated since 2010; deploy/README.md says to export it before switching
  - Episode 6's still survives only as a 420px crop, so its card is the one image below ideal resolution
docs:
  - ~/Development/pioneerone/README.md
  - ~/Development/pioneerone/deploy/README.md
  - ~/Development/pioneerone/STORY-SOURCES.md
git:
  branch: main
  head: d4fc748
  head_subject: 'Pioneer One: a site that leads with the show'
  dirty: 1
  ahead: 0
  behind: 0
  observed_at: '2026-08-15T17:01:25Z'
latest_session: 20260815T170125Z-unknown.md
resume:
  directory: /home/fs42/Development/pioneerone
  command: cd /home/fs42/Development/pioneerone && claude
updated_at: '2026-08-15T17:01:25Z'
provenance:
  status:
    source: model
    at: '2026-08-15T17:01:25Z'
  milestone:
    source: model
    at: '2026-08-15T17:01:25Z'
  goal:
    source: model
    at: '2026-08-15T17:01:25Z'
  definition_of_done:
    source: model
    at: '2026-08-15T17:01:25Z'
  next_task:
    source: model
    at: '2026-08-15T17:01:25Z'
  estimated_remaining:
    source: model
    at: '2026-08-15T17:01:25Z'
  blockers:
    source: model
    at: '2026-08-15T17:01:25Z'
  risks:
    source: model
    at: '2026-08-15T17:01:25Z'
  docs:
    source: model
    at: '2026-08-15T17:01:25Z'
  git:
    source: observed
    at: '2026-08-15T17:01:25Z'
---

# pioneerone — Current State

_Generated 2026-08-15T17:01:25Z. The front-matter above is the source of truth; this body is rendered from it._

| | |
|---|---|
| **Status** | MVP built and verified locally, pushed private. Blocked only on Cloudflare/Bluehost access for the deploy. |
| **Current milestone** | M1 complete — weekend MVP built, verified locally, committed and pushed private to speakhard/pioneerone (d4fc748) |
| **Next milestone** | M2 — Cloudflare Pages project and custom domain; then the archive |
| **Branch** | main |
| **HEAD** | d4fc748 — Pioneer One: a site that leads with the show |
| **Working tree** | 1 changed |
| **Observed** | 2026-08-15T17:01:25Z |

## Today's goal

pioneerone.tv presents Pioneer One as a show worth watching now: cinematic, credible, present-tense, and excellent on a phone

## Definition of done

Responsive site with a polished homepage, all six episodes watchable, concise Story and Now sections, correct social/SEO metadata, no placeholders beyond the deliberately deferred Archive, and deployed to the domain

## Next task

Josh: create the Cloudflare Pages project against speakhard/pioneerone (build 'pip install -r requirements.txt && python builder.py', output 'site'), verify on the pages.dev preview, then attach pioneerone.tv. Steps and rollback are in deploy/README.md

## Blockers

- Deployment to pioneerone.tv requires Cloudflare and Bluehost dashboard access, which this machine does not have

## Known risks

- The domain is on Bluehost nameservers with Cloudflare proxying, so pointing it at Pages means either moving the zone or splitting DNS across two providers
- The live WordPress/WooCommerce install is the only copy of whatever has accumulated since 2010; deploy/README.md says to export it before switching
- Episode 6's still survives only as a 420px crop, so its card is the one image below ideal resolution

## Estimated remaining

About an hour of Josh's dashboard time to go live

## Resuming

```bash
cd /home/fs42/Development/pioneerone && claude
```

### Resume prompt

```text
Continue development of pioneerone.

Repository:
/home/fs42/Development/pioneerone

Read:
~/Development/pioneerone/README.md
~/Development/pioneerone/deploy/README.md
~/Development/pioneerone/STORY-SOURCES.md

Current milestone:
M1 complete — weekend MVP built, verified locally, committed and pushed private to speakhard/pioneerone (d4fc748)

Today's Goal:
pioneerone.tv presents Pioneer One as a show worth watching now: cinematic, credible, present-tense, and excellent on a phone

Definition of Done:
Responsive site with a polished homepage, all six episodes watchable, concise Story and Now sections, correct social/SEO metadata, no placeholders beyond the deliberately deferred Archive, and deployed to the domain

First task:
Josh: create the Cloudflare Pages project against speakhard/pioneerone (build 'pip install -r requirements.txt && python builder.py', output 'site'), verify on the pages.dev preview, then attach pioneerone.tv. Steps and rollback are in deploy/README.md

Blockers:
- Deployment to pioneerone.tv requires Cloudflare and Bluehost dashboard access, which this machine does not have

Known risks:
- The domain is on Bluehost nameservers with Cloudflare proxying, so pointing it at Pages means either moving the zone or splitting DNS across two providers
- The live WordPress/WooCommerce install is the only copy of whatever has accumulated since 2010; deploy/README.md says to export it before switching
- Episode 6's still survives only as a 420px crop, so its card is the one image below ideal resolution

Do not revisit completed architectural decisions unless necessary.
```

## Provenance

| Field | Source | When | By |
|---|---|---|---|
| status | model | 2026-08-15T17:01:25Z | — |
| milestone | model | 2026-08-15T17:01:25Z | — |
| goal | model | 2026-08-15T17:01:25Z | — |
| definition_of_done | model | 2026-08-15T17:01:25Z | — |
| next_task | model | 2026-08-15T17:01:25Z | — |
| estimated_remaining | model | 2026-08-15T17:01:25Z | — |
| blockers | model | 2026-08-15T17:01:25Z | — |
| risks | model | 2026-08-15T17:01:25Z | — |
| docs | model | 2026-08-15T17:01:25Z | — |
| git | observed | 2026-08-15T17:01:25Z | — |

_Latest session log: `20260815T170125Z-unknown.md`_
