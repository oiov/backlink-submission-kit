# Where the data comes from, what was removed, what was corrected

## Provenance

Two layers, mixed in one table:

1. **A harvested list** (359 rows) collected in late 2026 from a curated "high-DR backlink list" circulating in Chinese indie-maker circles, plus follow-up harvests from directory rankings (e.g. `refined.so/tools/seo-directories`) and community link pages.
2. **First-hand verification.** ~262 rows were opened in a real browser and either run through the submission flow or explicitly ruled out. Those rows carry a `verified` date and notes with field IDs, captcha types, wizard order, and what the site's "free" plan actually required.

Rows that were never opened keep `verified = 未核验` and sit in the `U` priority. They are candidates, not claims.

## What was removed before publishing

| Removed | Why |
| --- | --- |
| Personal contact email, plus-addressing variants, project domain email | would be scraped; replaced with neutral wording ("自有邮箱" / "自有账号") |
| OAuth account handles, usernames, subdomains of personal blogs | identify the author, not the directory |
| Screenshots, browser profiles, tokens, passwords | never stored in the table in the first place |
| Submission ledgers of the author's own products | private history; `examples/example-product/ledger.md` shows the format instead |

Product names that appear in notes (a video tool, a file-attachment tool, an app-cleanup tool) were kept: they are the evidence that a site was really tested, and they are public products. No private project details, revenue figures, or unpublished roadmap are included.

`tools/validate.py` warns whenever an email-like string appears in the table, so future contributions cannot quietly reintroduce one.

## Manual corrections applied to the published snapshot

| Row | Change | Reason |
| --- | --- | --- |
| LibHunt (#12) | `X` → `P0`, notes rewritten | It had been marked "do not submit" only because the author's repo was already listed. For a new repo it is the easiest submission in the whole table (repo URL → auto-approved). |
| ToolFame (#381) | `submit_url` cleared | The recorded value was a dash, not an entry point. |
| Surge (#388), Vercel (#392) | `submit_url` set to the site URL | They are deploy targets, not forms; the CLI commands live in `notes`. |
| Hacker Noon (#389) | `dr` `90+` → `90` | Numeric column. |

## Known limitations

- **It is a snapshot.** Free tiers, badge rules and entry points change. Every row can be wrong tomorrow; the 30-second live re-check is not optional.
- **DR values are stale and partial.** Only ~30% of rows have one, and DR is a proxy, not a quality measure.
- **Coverage is biased** toward directories that were relevant to a handful of small, English-language indie products (a video downloader, an attachment preparer, a desktop cleaner). A B2B SaaS or a mobile game will find thinner coverage.
- **AI directories dominate the unverified pool** (115 of 243 `U` rows). They are useless for non-AI products, which is why the tag exists.
- **Chinese notes.** Deliberate: the precise wording ("勾选框是隐藏 input，要 focus 后按 Space") is the value, and translation loses it. `data/SCHEMA.md` has a glossary; `tools/query.py --json` gives English keys.

## Syncing your own master sheet

The author maintains a private master sheet in Chinese with the same content plus a per-product ledger. This repo is the published projection of it:

1. map your columns to the names in `data/SCHEMA.md`;
2. `python3 tools/gen_md.py && python3 tools/validate.py`;
3. commit. Never hand-edit the generated files.

If you contribute a batch of new rows, the same commands apply — `validate.py` fails the build on schema or staleness problems.
