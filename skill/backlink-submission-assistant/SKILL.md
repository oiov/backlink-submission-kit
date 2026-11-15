---
name: backlink-submission-assistant
description: Qualify, submit, and track free website/tool-directory listings for a product, starting from a verified 452-row directory table instead of a fresh list. Use when planning or executing backlink outreach / directory submissions for any project. Never invents product facts, never pays, never agrees to reciprocal badges, never promises ranking outcomes.
---

# Backlink Submission Assistant

You are running a **directory submission batch** for one product. The work is mostly judgment, not typing: pick the right sites, refuse the wrong ones, submit through the free path, and leave a truthful record.

The kit lives wherever this file lives. Resolve the repo root as `$BACKLINK_KIT` if set, else two levels up from this file (`skill/backlink-submission-assistant/` → repo root), else ask the user for the path. Read `AGENTS.md` at the root first — it holds the hard rules and the output contract.

## 1. Select sites from the table, never from scratch

```bash
python3 tools/query.py --shapes                                   # what shapes exist
python3 tools/query.py --shape generic --free --no-badge          # default new-project filter
python3 tools/query.py --priority P0,P1 --limit 12 --json         # candidate batch
```

- `P0` = proven free + no reciprocal badge + self-serve. Do these first.
- `P1` = needs an account or an unverified step. Second wave.
- `P2` = real but nofollow / long review / needs stars. Volume only, no ranking expectation.
- `P3` = reciprocal link, paid acceleration, or Top-3-only dofollow. **Business decision — ask, default no.**
- `U` = unverified pool. Filter by `tags`, check the site live before trusting anything.
- `X` = do not submit. Read the reason in `data/directories.md` §7; do not "give it another try".

Never submit to an AI-only directory for a non-AI product, and never force a product into a category that does not exist just because the form was free.

## 2. Account and email convention

- One **designated contact email** for the whole project: registrations, form `Email` fields, and the inbox used to click verification links. Keep it identical everywhere so verification mail, review notices, and listing claims all land in one readable inbox.
- Prefer Google/GitHub OAuth when offered. When email OTP or a magic link is required, open that inbox inside the same browser task space, click the link, and come back to the form. **Do not** mark a site blocked just because you cannot read its verification mail.
- Two documented exceptions worth knowing before you hit them:
  - the platform demands an `@yourdomain` address or a DNS TXT record for ownership → record `blocked: domain verification`, let the human decide (add DNS or drop the site);
  - the platform hard-rejects free inboxes (observed: "we only accept work/business emails") → it needs the project's domain email; note that notifications go there and must be followed up separately.
- The ledger records the login **method** only. Never write passwords, OTPs, or tokens anywhere.

## 3. Per-site flow

1. Open `submit_url` directly (never hunt for the form from the homepage).
2. **30-second re-check** — the table is a snapshot:
   - is the free tier still there, or moved behind a paywall?
   - does it require a badge/backlink on our site ("put this on your site", "embed code **required**")?
   - is there a category that genuinely fits?
   Any "no" → record `skipped` + reason, move on.
3. Fill. Read that row's `notes` first — it usually names the field IDs, the wizard order, the auto-scrape errors, and the captcha type.
4. Get proof: receipt, queue number, or listing URL. A URL change or an intermediate wizard step is **not** proof of submission.
5. Record one row in the project ledger immediately, before opening the next site.

## 4. Red lines

Skip and record when any of these is true:

- the free tier requires a badge or a followed backlink on the product site (link exchange)
- only a paid path exists, or the "free" button does nothing
- the site is a list-of-lists, an agency ("we submit for you"), or a marketplace — not a directory
- the submission requires signing a factual declaration about the product or its code that we cannot verify
- the entry is dead: 404, cert error, parked/redirected, Cloudflare loop
- the required account can only be created with an email we do not control (and no OAuth)

`$0` is not the same as free. Free pricing tiers frequently hide "badge must stay installed permanently" on the second screen of the pricing page. Read the pricing page, not the headline.

## 5. Recording

Append to the project ledger using `templates/ledger.md`. Status vocabulary is fixed: `live` / `submitted` / `queued` / `pending email` / `blocked` / `skipped` / `dead`. Always include: date, the price+badge terms **as seen that day**, the receipt, and the next action with an owner.

`submitted` is not `accepted`; `accepted` is not `live`. If the site gives no receipt, write that down and check for a confirmation email before claiming success.

## 6. Feed the table back

After each batch:

1. new trap, changed price, changed entry point, or a wrong `priority` → edit `data/directories.csv` (that row's `notes` / `price` / `badge` / `review` / `priority` / `verified`);
2. `python3 tools/gen_md.py` to re-render, then `python3 tools/validate.py`;
3. keep `notes` factual and reproducible: field id, wizard order, captcha type, what the scraper got wrong, what "free" actually required.

Never hand-edit `data/directories.md` or `directories.jsonl` — they are generated.

## 7. Traps worth knowing before you start

Full detail in [`playbook/gotchas.md`](../../playbook/gotchas.md). The five that cost the most time:

- **Framework rerender** (Nuxt/Vue/Livewire): values written via DOM setters get wiped. Write all fields in one pass, or type with real keystrokes.
- **Custom dropdowns** (react-select): the underlying input has zero width; click the visible container by coordinates, then click the option element. Enter usually does not submit.
- **Auto-scrape is not copy**: directories that prefill from your URL routinely put the tagline in the Name field and add wrong tags. Re-type everything.
- **Hidden `input[type=file]`**: upload via the input directly; the field clearing afterwards is normal, look at the on-page counter instead.
- **Browser-native permission bubbles** are not in the DOM. Hand the tab back to the human; `about:blank` clears it afterwards.

## 8. Stop and hand off

Captcha, SMS/phone verification, DNS ownership check, browser permission prompt, an OAuth consent screen asking for more than name/avatar/email, a required field only the human can answer (real pricing, license, founder), or any request to pay / exchange links / publish a launch. Fill everything up to that point, keep the page, and report what is left.
