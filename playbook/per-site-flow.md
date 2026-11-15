# Per-site flow (5 steps) and recording

## The 5 steps

**① Open the direct entry.** Use `submit_url` from the table — it is the page that was actually used, not a homepage guess. If it 404s, the site changed; record `dead` and fix the row later.

**② 30-second re-check.** The table is a snapshot, terms drift.

1. **Does it still cost money?** Does the free tier exist, or has it been pushed behind the paywall?
2. **Does it want something on my site?** Any "badge", "backlink", "put this on your site" → that is an exchange, `P3`, stop and report.
3. **Does it accept my category?** If there is no fitting category, do not squeeze in. A wrong category is worse than no submission.

One "no" → write `skipped` + reason and move on.

**③ Fill the form.** Check the row's `notes` first (field IDs, wizard order, captcha type, known scraper errors). Every required field gets a real value; fix anything the site prefilled wrongly.

**④ Get proof.** Receipt text, queue number, listing URL, or confirmation page. If the only observable is "form cleared, no error", record that literal observation and check the inbox.

**⑤ Record it.** One row, immediately, before the next site. One minute now saves a follow-up you can never do later.

## Recording

Copy `templates/ledger.md` into your project folder. Fixed columns:

| # | Site | Status | Date | Receipt / listing URL | Price & badge at the time | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | Uneed | queued | 2026-11-07 | `/edit/waiting-line/71286`, est. 2027-03-23 | $0 free line, no badge; $39.99/$14.99/$249 tiers skipped | check inbox in 1 week |

Status vocabulary — exactly these seven:

| Status | Meaning | Proof required |
| --- | --- | --- |
| `live` | Public listing page exists | the URL |
| `submitted` | Receipt / confirmation page seen | receipt text or URL |
| `queued` | Position or estimated publish date given | queue number / date |
| `pending email` | A verification link or OTP must be clicked to finish | which inbox |
| `blocked` | Filled but stopped on captcha / SMS / domain email / account | what is missing, who must do it |
| `skipped` | Deliberately not submitted | reason: category / badge / paid / declaration |
| `dead` | 404, cert error, unreachable | date checked |

Three things must always be recorded: **the date**, **the price and badge terms as seen that day**, **the next action and who owns it**.

Evidence hierarchy: listing URL > confirmation URL > quoted page text > screenshot. No evidence → do not write "submitted".

## After the batch

- Update `data/directories.csv` for anything that differed from the table (price, badge, entry point, gotcha) and re-render: `python3 tools/gen_md.py && python3 tools/validate.py`.
- Adjust `priority` from what actually happened: smooth submission → up; repeated failure → `X` with a reason.
- Note the batch in the ledger footer: how many sites, how many receipts, what is left for the human.
