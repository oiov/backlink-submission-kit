# Maintenance

A directory list decays. Roughly half of any unmaintained list is dead within a year. Three habits keep this one usable.

## Weekly (10 min)

- Read the inbox: verification links, approval notices, "your listing was rejected" mail.
- Move every `pending email` to `submitted` / `live` / `dead`.

## Monthly (30 min)

- Check `queued` entries: did they publish? Record the URL and flip to `live`.
- Spot-check 10 `P0`/`P1` `submit_url`s: still 200? still a form? still a free tier?
- Dead entries → `priority = X`, add `入口失效 + date` to `notes`.

## Per batch (while it is fresh)

- New trap → that row's `notes`.
- Price/badge changed → `price` / `badge`, and `priority` if it crossed the free/badge line.
- Found a site that is not in the table → append with `priority = U`, then verify and upgrade.
- Re-render and validate:

```bash
python3 tools/gen_md.py && python3 tools/validate.py
```

## Rules for edits

- `data/directories.csv` is the only source of truth. `directories.md`, `directories.jsonl`, `stats.json` are generated.
- One row per directory. Dedupe on `domain`; when two source lists disagree, keep the verified one and put the older claim in `notes`.
- `verified` is a date plus outcome, never a bare "yes": `2026-11-14` / `2026-11-08 实测（已提交）` / `未核验`.
- Write observations, not opinions: "free tier forces a footer badge, checked pricing page 2026-11-14" beats "sketchy site".
- Never add personal data (your email, handles, tokens, screenshots with account names). `tools/validate.py` warns on email-like strings for this reason.

## When a site changes its rules

Update the row and add the date. Do not delete the history in `notes` — the fact that a site *used* to be free and now charges is exactly the signal the next person needs.
