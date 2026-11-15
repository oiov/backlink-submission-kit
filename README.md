# backlink-submission-kit

**A verified directory table + an agent-ready playbook for getting a product listed in free, no-reciprocal-link directories.**

Not a list of 5,000 links. 452 rows, each one either opened in a real browser or marked as unverified — with notes that say which field breaks, which "free" plan secretly wants a badge, and which categories a site actually accepts.

[![directories](https://img.shields.io/badge/directories-452-2f6fed)](data/directories.md)
[![verified](https://img.shields.io/badge/verified-262-1a9c6b)](data/stats.json)
[![code](https://img.shields.io/badge/code-MIT-blue)](LICENSE)
[![data](https://img.shields.io/badge/data-CC0-lightgrey)](LICENSE-DATA)
[![中文](https://img.shields.io/badge/README-中文-red)](README.zh-CN.md)

---

## The problem

Every "backlink list" tells you to submit to 300 directories. Nobody tells you that:

- SaaSFame's `$0` plan requires their badge on your site **permanently** — that is a link exchange, not a free listing.
- 10015.io's free queue is nofollow and 3–4 months long.
- Softpedia opens with "this app contains no AI-written code" — a factual declaration you may not be able to sign.
- Uneed's entry only survives if it gets 10 upvotes on launch day.
- Half of an unmaintained list 404s within a year.

This repo is what is left after running those submissions for real: a table with the traps recorded, a five-step flow that stops you wasting review-queue slots, and a ledger format so the next project does not start from zero.

## What is in the box

| Component | What you get |
| --- | --- |
| **452 directories** | `P0` 27 proven free + no badge + self-serve · `P1` 13 need an account · `P2` 44 volume · `P3` 22 need a business decision · `U` 243 unverified · `X` 103 ruled out with reasons |
| **A playbook** | materials checklist, batch strategy, 5-step per-site flow, red lines, and the form/browser traps that eat hours |
| **A skill** | `skill/backlink-submission-assistant/` — drop into Claude Code / WorkBuddy and ask it to run a batch |
| **For agents** | `AGENTS.md` (contract), `data/directories.jsonl`, `tools/query.py --json`, an example product pack and ledger |
| **Tools** | zero-dependency Python: query the pool, re-render the docs, validate the CSV |

```
backlink-submission-kit/
├── AGENTS.md              ← agents start here (rules + output contract)
├── README.md / README.zh-CN.md
├── data/                  ← CSV (source of truth) + rendered MD/JSONL/stats + SCHEMA
├── playbook/              ← materials, batching, per-site flow, gotchas, maintenance
├── skill/backlink-submission-assistant/   ← SKILL.md + agent config
├── templates/             ← ledger, product pack, agent prompt
├── examples/example-product/  ← a filled pack + a realistic finished ledger
├── tools/                 ← query.py, gen_md.py, validate.py
├── docs/                  ← ai-usage, faq, data-notes
└── llms.txt               ← machine-friendly index of the above
```

## 60-second start

```bash
git clone https://github.com/oiov/backlink-submission-kit
cd backlink-submission-kit

python3 tools/query.py --shapes                                    # what product shapes exist
python3 tools/query.py --shape generic --free --no-badge --limit 12  # a first batch
```

Each result prints the direct submit URL, the account requirement, the review delay, and the one thing that usually goes wrong.

Then:

1. Copy `templates/product-pack.md` and fill in the 13 materials (`playbook/materials.md`). Do not guess pricing, platform, or category.
2. Copy `templates/ledger.md` for the project.
3. Work through the batch using `playbook/per-site-flow.md`; check `playbook/gotchas.md` before debugging a stuck form.
4. Record every site before opening the next one. `submitted` is not `live`.

## What the rows look like

| # | Site | Priority | DR | Price | Badge | Account | The note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | LibHunt | P0 | – | free | none | repo URL | real entry is `/repo/submit`; repo URL only, auto-approved; resubmitting an existing repo says "already submitted" — that is success |
| 3 | Uneed | P0 | 74 | free queue (~4 months) | none | Google | auto-scraped copy and tags are wrong; free entry needs ≥10 same-day upvotes to stay, ≥20 to keep dofollow |
| 378 | Softpedia | X | – | free | none | – | requires signing "no AI-written code", a 32×32 icon URL, and an image captcha — do not submit if the declaration is untrue |
| 68 | Fazier | P3 | 82 | "free" | **required** | – | free tier wants a reciprocal footer link; a business decision, default no |

Full table: [`data/directories.md`](data/directories.md) · fields: [`data/SCHEMA.md`](data/SCHEMA.md) · provenance and what was scrubbed: [`docs/data-notes.md`](docs/data-notes.md).

## Using it with an agent

```bash
export BACKLINK_KIT=~/backlink-submission-kit
ln -s "$BACKLINK_KIT/skill/backlink-submission-assistant" ~/.claude/skills/backlink-submission-assistant
ln -s "$BACKLINK_KIT/skill/backlink-submission-assistant" ~/.workbuddy/skills/backlink-submission-assistant
```

Then: *"Read AGENTS.md in $BACKLINK_KIT and submit my product (pack: …) to the first 10 eligible free directories."*

The agent gets the rules it needs to **not** do the four things agents do by default: invent a pricing tier, accept a badge requirement, submit a video tool to an AI directory, and report "published" for a pending review. Details and prompt templates: [`docs/ai-usage.md`](docs/ai-usage.md), [`templates/agent-prompt.md`](templates/agent-prompt.md).

## Field notes: what it looks like to run this with WorkBuddy

This kit wasn't written first and used afterwards. It is the residue of doing it: five products, 262 sites actually opened in a browser, most of the form-filling done by WorkBuddy driving a logged-in browser window. Six things that decided whether a session was productive:

**1. Point the agent at the repo instead of pasting rules.** One line — *"read `AGENTS.md` at `$BACKLINK_KIT`, then submit the pack in `./pack.md` to the next 10 eligible `P0` sites"* — beats a three-paragraph prompt. The rules live in a file, so you fix them once and every later session inherits the fix. Pasted rules rot; the repo doesn't.

**2. Batch 8–12 sites, not 30.** Every batch of size runs into at least one email verification, one image captcha, and one site that redirects to a dashboard you have never seen. Past roughly a dozen, the agent starts skipping the record-keeping to "finish the batch" — the worst possible trade, because you lose the ledger and keep the unverified claims.

**3. The logged-in browser is the whole trick.** More than half of the free directories hide the form behind Google or GitHub login. With a persistent browser session, the agent goes straight to the form; without one, you spend the first twenty minutes of every batch on OAuth and half the batch on "please sign in first".

**4. One dedicated mailbox, and let the agent read it.** Use a single generic address for every submission, and when a site sends a confirmation link, let the agent open that inbox in the same browser and finish the loop. If the agent has to stop at "verification email sent", you become the bottleneck and the batch dies there. Two related traps: a handful of directories treat a domain address as a signal of self-promotion and review it harder, and a few require DNS TXT proof of domain ownership — that last one genuinely is yours to do.

**5. The ledger is the deliverable, not the listing.** Agents will cheerfully report "done" the moment the submit button is clicked. Insist on one row per site, written *before* the next form opens: status, entry URL, what was filled, what is still pending. `submitted` ≠ `accepted` ≠ `live`. Two weeks later that file is the only record of which of your forty submissions are still sitting in a queue.

**6. Four things always come back to you:** a badge requirement, a declaration you must sign (Softpedia's "no AI-written code"), a paid tier dressed up as free, and domain-ownership proof. The agent stops and asks on those; it does not decide. That is a hard rule in `AGENTS.md`, and it is what keeps the rest of the work legitimate rather than spam.

None of this is specific to WorkBuddy — it applies to any agent with a browser and a filesystem. This is simply the setup the table was built and tested on. If you are on WorkBuddy, the skill installs the same way as in the section above (`~/.workbuddy/skills/`), and `docs/ai-usage.md` has the prompt shapes that worked.

## The four rules that matter

1. **`$0` is not free** until you have read the badge clause at the bottom of the pricing page.
2. **Category beats availability.** No fitting category → skip, however free the form is.
3. **30-second live re-check** before every form: price, badge, entry, category. The table is a snapshot.
4. **Record the receipt, not the intention.** `submitted` ≠ `accepted` ≠ `live`.

## Contributing

Dead sites, changed prices, new directories, English translations of notes — all welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md). The short version: edit `data/directories.csv`, then

```bash
python3 tools/gen_md.py && python3 tools/validate.py
```

## License

- Code, docs, playbook, skill: **MIT** ([LICENSE](LICENSE))
- Site data (`data/`): **CC0-1.0** ([LICENSE-DATA](LICENSE-DATA)) — use it, remix it, ship it commercially, no attribution required

## Honest disclaimer

This kit maximises *legitimate* visibility: free listings, correct categories, no spam, no link schemes. It does not promise rankings, and the numbers in `data/` were true when checked, not forever. Verify before you submit — that is the whole method.
