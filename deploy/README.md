# Deploying pioneerone.tv

Same shape as Crows, Lens, Kino and jbcom: GitHub holds the source, Cloudflare
Pages runs the builder and serves the result, generated output never enters git.

> Steps 2 onward need the Cloudflare and Bluehost dashboards, which this machine
> has no credentials for. They are written to be followed by hand and have not
> been run. Everything before them **has** been: the build, the tests and the
> device-size render all pass locally.

## What is there now

`pioneerone.tv` resolves to `66.235.200.147` on Bluehost nameservers
(`ns1`/`ns2.bluehost.com`), with Cloudflare proxying in front — the origin
answers a Cloudflare bot challenge rather than serving pages to anything that
looks automated.

Behind it is WordPress 6.7.1 running WooCommerce and the "streamit" theme: a
video-marketplace template, with Shop, Cart, Checkout, Wishlist, Sign In and
Upload Video in the navigation, titled *"LANDING – PIONEER ONE: The
Groundbreaking Sci-Fi Web Series"*. It was last meaningfully touched in
December 2024.

**Nothing in this repository has touched it.** It stays up, exactly as it is,
until step 4 — and step 4 is reversible.

Before you switch anything: take a WordPress export and a file backup. Not
because this plan needs one, but because that install is the only copy of
whatever has accumulated in it since 2010, and it is about to stop being the
thing serving the domain.

## 1. The repository

Already created and pushed, private, matching every other project here:

    git@github.com:speakhard/pioneerone.git

Nothing in it is secret — it is prose, public URLs, and images recovered from
the Internet Archive — so making it public later is a free choice, not a
disclosure decision. Cloudflare Pages reads private repositories happily.

## 2. The Pages project

Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git →
`speakhard/pioneerone`.

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | None |
| Build command | `pip install -r requirements.txt && python builder.py` |
| Build output directory | `site` |
| Root directory | *(blank)* |

No environment variables and no secrets. If this project ever appears to need a
credential, something has gone wrong — read `builder.py` before adding one.

The build installs one package (Jinja2). Cloudflare's Python image is 3.11+;
`builder.py` uses `tomllib`, standard library from 3.11. If the build reports
`No module named 'tomllib'`, set the `PYTHON_VERSION` build variable to `3.12`.

## 3. Check the preview before touching DNS

Pages gives the project a `*.pages.dev` address. Everything can be verified
there while the real domain carries on serving WordPress.

    curl -s https://<project>.pages.dev/ | grep -o '<title>.*</title>'
    curl -s https://<project>.pages.dev/story/   | head -3
    curl -s https://<project>.pages.dev/archive/ | head -3
    curl -sI https://<project>.pages.dev/static/img/social-card.jpg | head -3

Do not trust a bare status code — this family's own hard-won rule. A page that
answers `200` with `<!doctype html>` where a JPEG was expected is Cloudflare
serving the homepage for a path that does not exist: a failed deploy wearing a
success.

Then check the two things a status code cannot tell you:

    # all six episodes present
    curl -s https://<project>.pages.dev/ | grep -c 'episode__frame'   # expect 6

    # the social card, which is what people actually see when the link is shared
    open https://cards-dev.twitter.com/validator     # or paste the URL into Signal

And open it on a phone. That is the entire point of the site.

## 4. The custom domain

This is the only step that changes what the public sees, and the only one that
needs thinking about.

`pioneerone.tv` is on Bluehost nameservers today, so Cloudflare cannot add the
record for you the way it does for zones already on the account. Two routes:

**(a) Move the zone to Cloudflare** — add `pioneerone.tv` as a zone in the same
Cloudflare account, let it import the existing records, then change the
nameservers at the registrar. Afterwards the Pages custom domain attaches in one
click, exactly like the other four sites. Slower to start (nameserver changes
take hours to propagate) but leaves the domain managed alongside everything else.

**(b) Point a CNAME from Bluehost** — in Bluehost's DNS, point `pioneerone.tv`
and `www` at the `*.pages.dev` hostname. Faster, but leaves DNS split across two
providers, which is how a domain gets lost in three years' time.

(a) is the better long-term answer and matches the rest of the estate. (b) is
the one to reach for if the site has to be live by Saturday.

Either way: add **both** `pioneerone.tv` and `www.pioneerone.tv` to the Pages
project, so the address people half-remember still works.

## 5. Verify on the real domain

    curl -sI https://pioneerone.tv/ | head -1                 # 200, no CF challenge
    curl -s  https://pioneerone.tv/ | grep -o '<title>.*</title>'
    curl -sI https://pioneerone.tv/story/   | head -1
    curl -sI https://pioneerone.tv/archive/ | head -1
    curl -s  https://pioneerone.tv/robots.txt

HTTPS is automatic — Pages issues the certificate once the domain is attached.
Give it a few minutes before concluding it is broken.

## 6. Rollback

Pages keeps every deployment: Project → Deployments → the last good one →
Rollback. A failed build never replaces a working site.

To put the old WordPress site back, point DNS back at `66.235.200.147`. Nothing
in this project has modified that install, so it is still there waiting. This is
the reason step 4 is last and everything before it is verifiable on `pages.dev`.

## Afterwards

- **The mailing list.** `newsletter.action` in `content/site.toml` is empty, so
  the signup renders a mailto link to `contact@pioneerone.tv`. Confirm that
  address still routes, or set `action` to a real endpoint. One line.
- **The old URLs.** The 2010–2012 site used `/YYYY/MM/DD/slug/` permalinks and
  there are live inbound links to them from TorrentFreak and elsewhere. They
  will 404. Redirects belong in a `_redirects` file when the archive lands and
  there is somewhere to send them; sending them all to `/` today would be worse
  than a 404.
