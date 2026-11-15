# Agent prompt template

Copy this into Claude Code / Cursor / Codex / WorkBuddy after cloning the repo. Replace the bracketed parts. It works because the repo already contains the rules — the prompt only supplies the product.

---

You have this repo locally: `[path/to/backlink-submission-kit]`.

Read, in this order:
1. `AGENTS.md` (hard rules + output contract)
2. `data/directories.md` §0–§2 (routes by project shape)
3. `playbook/materials.md`, `playbook/per-site-flow.md`, `playbook/gotchas.md`

My product is described in `[path/to/product-pack.md]`. Do not invent anything that is not in that file.

Task: **plan and execute the first batch of free directory submissions.**

1. Determine the project shape, then build a candidate list with
   `python3 tools/query.py --shape [generic|opensource|desktop|extension|ai|chinese] --free --no-badge --json`
2. Pick 8–12 sites: `P0` first, no-account sites before account sites. Show me the list with one line per site (why eligible / why skipped) before touching a browser.
3. For each site: re-check free tier / badge / category on the live page, fill the form from the product pack, reach the receipt.
4. Stop and ask me when a captcha, SMS, DNS/domain-email check, browser permission prompt, or unclear product fact appears. Never pay, never accept a reciprocal badge, never sign a declaration about how the code was written.
5. After each site, append one row to my ledger using `templates/ledger.md` (status vocabulary: live / submitted / queued / pending email / blocked / skipped / dead).
6. At the end: update `data/directories.csv` for anything that differed from the table, then run `python3 tools/gen_md.py && python3 tools/validate.py`. Report the batch summary: receipts, blockers, and the 1–3 things only I can do.

Constraints: free listings only; no invented facts; no ranking promises; one listing per site.

---

## Variants

**Plan only (no browser):** ask for steps 1–2 and a per-site field map, plus the blockers you predict. Cheap way to sanity-check a batch.

**Single site:** `Submit to directory #3 (Uneed) per AGENTS.md, then record it.`

**Audit an existing batch:** `Read ledger-*.md, verify every "live" row still resolves, and flag rows whose status is optimistic.`

**Extend the table:** `Find 10 more [AI / desktop / Chinese] directories and append them to data/directories.csv with priority U, then verify and re-render.`
