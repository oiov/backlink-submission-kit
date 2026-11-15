# Materials — the 13 items

Missing one of these means you get stuck halfway through a form and the whole batch stalls. Assemble them **before** opening any browser tab, ideally in one product pack file (see `templates/product-pack.md` and `examples/example-product/`).

| # | Item | Spec | Needed by |
| --- | --- | --- | --- |
| 1 | Website URL | `https://` canonical, **no trailing slash** (some sites reject it) | all |
| 2 | Product name | one spelling, one capitalisation, everywhere | all |
| 3 | One-line positioning | ≤60 chars, says *for whom + does what* | tagline fields |
| 4 | Short description | one 100–130 char version, one 200–255 char version (255 is a common cap) | legacy directories |
| 5 | Long description | 300 / 500 / 850 char versions | strict sites require ≥500 chars |
| 6 | Logo | 512×512 PNG + SVG | all |
| 7 | Screenshots | 2–3, **each >50 KB** (some sites silently reject small images) | all |
| 8 | Social/OG image | 1200×630 | auto-scrape forms |
| 9 | Source repo | public, LICENSE present, README with install steps; add `docker-compose.yml` if it has a server | open-source directories |
| 10 | Installer direct links | GitHub Releases URLs (exe/dmg/zip/AppImage) + version number | download sites |
| 11 | Pricing statement | Free / Freemium / one-time. If you cannot state it, do not guess | most directories |
| 12 | Contact email | one designated address for accounts + forms + verification | all |
| 13 | Category shortlist + tags | 2–3 candidate categories and ~8 English tags, decided in advance | all |

**The three that must not be guessed:** pricing, platform support, category. A wrong answer is not a small error — reviewers treat it as a low-quality submission and you lose the queue slot.

## Contact email and accounts

| Situation | What to do |
| --- | --- |
| Registration | Use the project's designated email. If Google/GitHub OAuth is offered, use that instead of inventing a site password. |
| `Email` / `Contact email` field | Same address, so verification and review notices land in one inbox. |
| Verification link or one-time code | Open that inbox **in the same browser task space**, read the mail, click the link, return to the form. Do not record the site as blocked. |
| `@yourdomain` work email or DNS TXT ownership check | Cannot be worked around. Record `blocked: domain verification`, let the human decide. |
| Site rejects free inboxes ("we only accept work/business emails") | Fall back to the project domain address, and note in the ledger that notifications go there and need separate follow-up. |
| Ledger | Login **method** only. No passwords, no tokens. |

Why one inbox: every "I cannot read the confirmation mail" is a self-inflicted block. One readable address turns three dead ends per batch into three extra listings.

## Copy discipline

- Write from verified facts only. No invented user counts, no "trusted by 10,000 teams", no founder bios you have not confirmed.
- Keep the same tagline across sites. Reviewers cross-check; inconsistent positioning reads as spam.
- If a form prefills from your URL, treat the prefilled text as a draft from a stranger: re-type the name, tagline, description, and tags.
