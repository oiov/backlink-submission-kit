# Ledger — ClipNest（示例）

> Illustrative only: a realistic first batch for the fictional product in `product-pack.md`. Ids reference real rows in `data/directories.csv`, so you can open each one and follow the story.
> Status vocabulary: live / submitted / queued / pending email / blocked / skipped / dead.

## Product

| Field | Value |
| --- | --- |
| Product | ClipNest |
| Website | `https://clipnest.example.com` |
| Shape | open source + desktop + web tool |
| One-line positioning | Save clips from public links — in the browser or as a desktop app |
| Candidate categories | Video/Media · Productivity · Open source |
| Pricing | Free (no paid tier) |
| Contact email | `hello@clipnest.example.com` |
| Repository | `https://github.com/example/clipnest` |
| Materials folder | `examples/example-product/` |

## Batch 1 — 2026-11-15

| # | Site | Status | Date | Receipt / listing URL | Price & badge at the time | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Indie Hackers | live | 2026-11-15 | `/products/clipnest` — public, then completed `/edit` and ticked published | $0, no badge | — (add Motivation + founding year later for ranking) |
| 3 | Uneed | queued | 2026-11-15 | `/edit/waiting-line/48211`, estimated 2027-04-02 | $0 waiting line; skipped $39.99 date-pick, $14.99 fast-track, $249 auto-submit | rewrite auto-scraped description (it said "Screen Recording"); needs ≥10 same-day upvotes to stay listed |
| 12 | LibHunt | live | 2026-11-15 | `libhunt.com/r/clipnest` — auto-approved on repo submit | free | — (license/topics were picked up from the repo) |
| 10 | appsgit | submitted | 2026-11-15 | review queue receipt: "approved apps usually appear within a week" | free; no badge | check in 1 week |
| 2 | SaaSHub | submitted | 2026-11-15 | `saashub.com/clipnest/added` | free standard queue, 1–12 weeks; $75/$99 tiers not taken | 3 categories + competitor step both completed; the banner asking AI agents to hand off to a human was respected (submitted by the human) |
| 14 | osalt | submitted | 2026-11-15 | `/thank_you` after suggestion form | free | editor decides whether an entry is created; homepage URL submitted without trailing slash |
| 16 | Tiny Startups | submitted | 2026-11-15 | "ClipNest is saved" (step 5) | free = human queue; instant listing is £69, not taken | fixed scraper errors: tagline had landed in the Name field |
| 6 | Launching Next | blocked | 2026-11-15 | form fully filled, stopped at the arithmetic captcha on the confirmation page | free Regular Links; Fast-Track $99 not taken | **human**: type the captcha (2+3) and click Submit; then `/thanks/?i=…` gives the queue number |
| 349 | AlternativeTo | skipped | 2026-11-15 | — | free | category: FAQ explicitly excludes downloaders — do not retry |
| 68 | Fazier | skipped | 2026-11-15 | — | free tier requires a reciprocal footer link | link exchange = business decision, not taken |
| 354 | NewTool.site | skipped | 2026-11-15 | — | $0 plan requires a permanent badge, checked periodically | link exchange, not taken |
| 378 | Softpedia | skipped | 2026-11-15 | — | free | requires signing "no AI-written code" plus a 32×32 icon URL and an image captcha — the declaration is not true for this repo |

## Skipped summary

| Site | Reason | Decided on |
| --- | --- | --- |
| AlternativeTo | category excludes downloaders | 2026-11-15 |
| Fazier | reciprocal footer link required for free tier | 2026-11-15 |
| NewTool.site | permanent badge required | 2026-11-15 |
| Softpedia | "no AI-written code" declaration + captcha + 32×32 icon | 2026-11-15 |

## Summary

- Live (public URL exists): 2 — Indie Hackers, LibHunt
- Submitted / queued: 5 — Uneed (queue), appsgit, SaaSHub, osalt, Tiny Startups
- Waiting on a human: 1 — Launching Next (arithmetic captcha)
- Skipped: 4 — recorded above so the next batch does not retry them
- Feed back into `data/directories.csv`: no row changed this batch. If Softpedia's declaration gate is new to you, it is already in the row's `notes`.
