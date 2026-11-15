# FAQ

## Is this an "ultimate backlink list"?

No. It is a **judgment kit with a table attached**. 452 rows is small compared to the 5,000-row lists floating around — those are mostly unverified, and half of them are dead, paid-only, or wrong-category. What is here was opened in a real browser, and the notes say what happened.

The offer is: *do 12 sites properly this weekend and know exactly what you got*, instead of submitting to 200 sites and not knowing which ones count.

## Will this improve my ranking?

Nobody can promise that, and any list that does is selling something. What free directory listings reliably give you: a page that can rank for your product name, referral traffic, a footprint for reviewers and journalists, and a few dofollow links from real (if modest) domains. They are the cheapest part of a launch, not a growth strategy.

Use them for: brand search, a credible "as seen on" set, and the first few links a new domain needs. Do not use them as a link-building campaign.

## Why are the notes in Chinese?

They were written during execution by someone working in Chinese, and the value is in the exact wording — "the checkbox is a hidden input, focus it and press Space", "the free queue needs ≥10 same-day upvotes". Translating them loses that precision. `data/SCHEMA.md` has an English glossary, and `tools/query.py --json` returns English keys. English notes are welcome as a contribution.

## Why do some rows say `dofollow` as "待核验" (unverified)?

Because it was not measured. A third-party list claiming dofollow is not evidence. Where the link attribute was actually inspected, the note says so (e.g. "7 outbound links, all rel empty"). Treat unverified as "unknown, check yourself".

## Are paid directories included?

They are recorded, and they are `P3`. When the free tier requires a reciprocal badge, the row says exactly that. The kit's default answer to "should I pay or exchange links" is **ask the human, default no** — because that is a strategy decision, not an execution step.

## Can I use this commercially / in a paid product?

Site data is CC0-1.0 (public domain). Code and docs are MIT. Do whatever you want; attribution is appreciated but not required for the data.

## How current is it?

See `data/stats.json` → `updated`, plus the per-row `verified` dates. The bulk was verified in October–November 2026. Anything older than ~6 months should be re-checked on site before you spend time on it.

## I found a dead site / a site that now charges. What do I do?

Open a "directory report" issue (template provided) with the domain, what you saw, and the date. Or fix the row yourself: edit `data/directories.csv`, run `python3 tools/gen_md.py && python3 tools/validate.py`, and open a PR. Corrections are the most valuable contribution — a table's half-life is about a year.

## Why is the biggest group "U — unverified"?

Because honesty costs a column. Harvested rows are useful as candidates, but marketing them as verified would make the whole table untrustworthy. `U` rows are filtered by tag and DR, then checked live — roughly 30 seconds each.

## Does an agent really need all this ceremony?

Yes, and the ceremony is the product. Left alone, agents invent a pricing tier, accept a badge requirement, submit a video tool to an AI directory, and report "published" for a pending review. `AGENTS.md` exists to make those four failures impossible to do accidentally.
