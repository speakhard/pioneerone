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

## The domain also carries live email — read this before touching DNS

`pioneerone.tv` is not only a website. It has working mail at Bluehost:

    MX    pioneerone.tv          0 mail.pioneerone.tv
    A     mail                   50.6.154.91
    A     webmail                50.6.154.91
    A     autodiscover           50.6.154.91
    CNAME smtp                   mail.pioneerone.tv
    TXT   pioneerone.tv          "v=spf1 ip4:50.6.154.59 a mx include:websitewelcome.com ~all"

**Losing these breaks email for the domain, silently and completely.** They are
listed here so they can be checked off one by one after the zone is imported,
rather than discovered missing a week later.

Note also what this means for the site: `contact@pioneerone.tv` does not exist
as a mailbox, but the domain *does* accept mail, so anything sent to it is
taken at the edge and dropped without a bounce. That is why the build refuses
to publish an unverified address — see step 6.

## 1. The repository

Public, at:

    git@github.com:speakhard/pioneerone.git

Nothing in it is secret: prose, public URLs, and images recovered from the
Internet Archive.

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

This is the only step that changes what the public sees.

There is really only one route, and it is worth knowing why. Pointing a domain
at Pages from external DNS needs a CNAME, and classic DNS forbids a CNAME at
the apex — so leaving the zone at Bluehost can only put `www.pioneerone.tv` on
Pages, never the bare `pioneerone.tv`. The bare domain is the one you say out
loud, so: **move the zone to Cloudflare**, which resolves apex CNAMEs by
flattening them.

1. Cloudflare → Add a site → `pioneerone.tv`. Let it scan and import.

2. **Before changing any nameservers**, check the imported records against the
   mail list at the top of this file. All six must be present and correct.

3. Set every mail record to **DNS only** (grey cloud, not orange). Proxying
   `mail`, `webmail`, `smtp` or `autodiscover` routes mail through Cloudflare's
   HTTP proxy, which does not speak SMTP, and mail stops. This is the single
   most common way this migration goes wrong.

4. Leave `A pioneerone.tv → 66.235.200.147` and `CNAME www → pioneerone.tv` as
   imported for now. The WordPress site keeps serving through the nameserver
   change, so the switch to Pages is a separate, deliberate step you take once
   you are happy with the preview.

5. Change the nameservers at the registrar to the two Cloudflare gives you.
   Propagation is usually under an hour but can take longer. Nothing visible
   changes when it completes — that is the point.

6. Confirm mail still works: send a message to an address on the domain that
   you know exists, and watch it arrive. Do this **before** step 7.

7. Pages project → Custom domains → add **both** `pioneerone.tv` and
   `www.pioneerone.tv`. Cloudflare replaces the A record with its own routing.
   This is the moment the public sees the new site.

## 5. Verify on the real domain

    curl -sI https://pioneerone.tv/ | head -1                 # 200, no CF challenge
    curl -s  https://pioneerone.tv/ | grep -o '<title>.*</title>'
    curl -sI https://pioneerone.tv/story/   | head -1
    curl -sI https://pioneerone.tv/archive/ | head -1
    curl -s  https://pioneerone.tv/robots.txt

HTTPS is automatic — Pages issues the certificate once the domain is attached.
Give it a few minutes before concluding it is broken.

## 6. The "stay in touch" section

As shipped, this section offers the YouTube channel, not an email link. That is
deliberate: `contact@pioneerone.tv` does not exist, the domain accepts mail for
it anyway, and a contact button that swallows replies is worse than no button.

Two minutes of work upgrades it. In Bluehost cPanel → **Forwarders** (or
**Email Accounts**), create `contact@pioneerone.tv` pointing at whichever inbox
you actually read. Send it a test message and watch it arrive. Then:

    # content/site.toml
    fallback_verified = true

Commit and push; Pages rebuilds and the section becomes an email link. The
build prints a warning in the Cloudflare log for as long as this is unverified,
so it cannot be quietly forgotten.

If you would rather have a real list, set `newsletter.action` to any endpoint
that accepts a POSTed `email` field and the section becomes a form instead.

## 7. Rollback

Pages keeps every deployment: Project → Deployments → the last good one →
Rollback. A failed build never replaces a working site.

To put the old WordPress site back, point the apex A record at
`66.235.200.147` again and remove the custom domain from the Pages project.
Nothing in this project has modified that install, so it is still there
waiting. This is why the nameserver move and the domain attachment are separate
steps, and why everything before them is verifiable on `pages.dev`.

## Afterwards

- **The old URLs.** The 2010–2012 site used `/YYYY/MM/DD/slug/` permalinks and
  there are live inbound links to them from TorrentFreak and elsewhere. They
  will 404. Redirects belong in a `_redirects` file when the archive lands and
  there is somewhere to send them; sending them all to `/` today would be worse
  than a 404.
- **The WordPress install.** Once the domain is on Pages, that install is no
  longer serving anything but is still running, still on 6.7.1, and still
  reachable at its IP. Decide whether to keep it as a mail host only, or
  retire it — but export it first either way.
