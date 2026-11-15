# AGENTS.md

Instructions for AI coding agents (Claude Code, Codex, Cursor, WorkBuddy, Cline, any tool that reads `AGENTS.md`). Humans: read [`README.md`](README.md) instead.

This repo is a **working kit for getting a product listed in free, no-reciprocal-link directories**. It is not a list of "best backlink sites" to copy-paste. It is a judgment playbook, a verified 452-row site table, and the ledger format to record what actually happened.

---

## 0. What you are doing

Take one product, pick the right subset of directories from `data/directories.csv`, submit it through the free path, and record the real outcome. The scarce resource is not the list — it is **judgment** (never waste a review-queue slot on a wrong-category or paid-only submission) and **bookkeeping** (so the next project does not re-learn everything).

## 1. Read order (do this before touching a browser)

| # | File | Why |
| --- | --- | --- |
| 1 | this file | rules and output contract |
| 2 | `data/directories.md` §0–§2 | pick the route for the product shape, get the id list |
| 3 | `data/SCHEMA.md` | what every column means, enum values |
| 4 | `playbook/materials.md` | the 13 materials you must have before opening a single form |
| 5 | `playbook/per-site-flow.md` | the 5 steps + red lines to apply per site |
| 6 | `playbook/gotchas.md` | form/JS/captcha traps; check here before debugging a stuck form |
| 7 | `templates/ledger.md` | copy this to start the project ledger |

Do not read all 452 rows. Query them.

```bash
python3 tools/query.py --shapes                                  # project shapes with counts
python3 tools/query.py --shape opensource --free --no-badge      # the default filter for a new project
python3 tools/query.py --priority P0,P1 --json                   # machine-readable shortlist
python3 tools/query.py --search captcha --limit 5                # find rows with known traps
```

Add `--json` whenever you need to reason over rows programmatically. Never scrape `directories.md` with regex; it is a render, and it is lossy.

## 2. Hard rules

These are not style preferences. Violating them gets the product banned or burns a queue slot permanently.

1. **Never invent a product fact.** Pricing, platform support, founder, company, socials, star counts, user numbers. If a field is required and unknown, stop and ask the human — do not guess `Free` vs `Freemium`.
2. **Free means free end-to-end.** A `$0` plan that requires placing the directory's badge/backlink on the product site is **not free** — it is a link exchange, a business decision. Park it as `P3` / `不投（互换）` and report it, never decide it yourself.
3. **The 30-second re-check is mandatory.** The table is a snapshot. Before filling a form, confirm on the live site: (a) a free tier still exists and is not behind a paywall, (b) no reciprocal badge is required, (c) the category actually fits the product.
4. **Category beats availability.** If the site has no fitting category, skip it. Stuffing a video tool into an AI directory "because the form was free" is worse than not submitting.
5. **Never bypass a gate.** No captcha solving scripts, no anti-bot circumvention, no fake visits/upvotes/stars, no inventing a work email to pass a domain-email check. When a captcha or an SMS/domain check appears, fill everything up to that point, then hand the page to the human.
6. **OAuth scope discipline.** Ordinary sign-in only (name, avatar, email). If the consent screen asks for more, abort and report.
7. **One product, one listing per site.** Search the ledger first; duplicates get rejected and flag the account.
8. **`submitted` ≠ `accepted` ≠ `published`.** Record the exact state you saw, with the receipt: listing URL > confirmation URL > page text > screenshot. Never write "live" without a public URL.
9. **No credentials in the ledger.** Record the login *method* only (Google OAuth / email OTP / username). Passwords live in the browser, never in a file.
10. **Ask before anything irreversible or public.** Publishing a launch, paying, exchanging links, signing a declaration about how the code was written (e.g. "no AI-generated code"), creating an account on a site that requires a personal email account you do not control.

## 3. Workflow

```
plan → verify → fill → confirm → record → (update the table)
```

0. **Materials.** Confirm the 13 items in `playbook/materials.md`. Whatever is missing becomes a blocking question, not a form-field guess.
1. **Select.** `tools/query.py` with the product shape. Aim for 8–12 sites per batch — over 12 you will lose records. Order: no-account sites first, then all account-requiring sites in one login session.
2. **Qualify (per site, 30 s).** Free tier? Badge? Category? Then decide `eligible` / `skip(reason)`.
3. **Fill.** Use `notes` for that row — it usually tells you the field IDs, the wizard order, and what the auto-scraper gets wrong. Re-type anything the site auto-filled; never trust scraped copy.
4. **Confirm.** Reach the receipt/queue page. A URL change or a wizard step is not proof. If the success state is "form cleared, no error", say so and check for the confirmation email before claiming success.
5. **Record.** Append one row to the project ledger (`templates/ledger.md` format). Then verify the next site.
6. **Feed back.** New trap or changed terms → update that row's `notes` / `price` / `badge` / `priority` in `data/directories.csv`, then `python3 tools/gen_md.py && python3 tools/validate.py`. This is how the pool stays worth having.

## 4. Output contract

Every batch must end with a ledger table. One row per site, these exact columns:

```markdown
| # | Site | Status | Date | Receipt / listing URL | Price & badge at the time | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | Uneed | queued (free line) | 2026-11-07 | /edit/waiting-line/71286 · est. 2027-03-23 | $0, no badge, paid tiers skipped | check email in 1 week |
```

Status vocabulary — use only these seven:

| Status | Meaning |
| --- | --- |
| `live` | Public listing page exists; include URL |
| `submitted` | Receipt / confirmation page seen |
| `queued` | Queue position or estimated date given |
| `pending email` | Needs an email link/OTP to complete |
| `blocked` | Form filled but stopped on captcha / account / SMS / domain email |
| `skipped` | Not submitted; include the reason (category / badge / paid / declaration) |
| `dead` | 404, cert error, domain gone |

Also report, in plain text: what you could not resolve, and the 1–3 things the human must do (click a verification link, decide on a link exchange, provide a phone number).

For machine consumption, `--json` a summary at the end:

```json
{"product":"…","batches":[{"date":"2026-11-15","sites":[{"id":3,"site":"Uneed","status":"queued","url":"…","note":"…"}]}]}
```

## 5. Stop and hand off

Stop immediately, keep the page open, and report, when:

- a captcha, SMS PIN, phone verification, or `@yourdomain` / DNS TXT ownership check appears — fill everything else first
- a browser-level permission prompt (notifications, camera…) appears — the human owns that tab now
- the site asks you to sign a factual declaration you cannot verify
- the free tier disappeared and only paid plans remain
- the consent screen requests anything beyond name/avatar/email
- the product's own facts (pricing, platform, license) are unclear and the form requires them

## 6. Browser automation

The reference implementation of this playbook was run with a persistent local browser (ego-browser / Chrome with a logged-in profile). Any agent with form-filling capability works — the traps in `playbook/gotchas.md` are mostly framework-level (react-select, Nuxt/Livewire rerender, hidden file inputs, ProseMirror, Typeform, Cloudflare).

Practical rules that survived contact with ~130 real sites:

- one task space, one tab reused; screenshot only when you need visual proof
- native permission bubbles are browser UI — they are not in the DOM; hand the space back to the human
- Cloudflare "checking your browser" often clears itself in 8–10 s; do not fight it
- after any unexpected state change, re-inspect the page before retrying; never click submit twice

## 7. Never do

- promise ranking/SEO outcomes — this kit maximises *legitimate* visibility, not rankings
- submit to AI directories on behalf of a non-AI product
- mass-submit with the same description across 50 sites in one hour (reviewers notice, and two approvals matter more than twenty pending)
- create paid plans, trials with cards, or "featured" upgrades
- commit personal email addresses, account handles, tokens, or screenshots containing them into this repo
