# Contributing

The most useful contribution is a **correction**: a site that died, a price that changed, a badge clause nobody noticed. Second most useful: a new directory with a verified entry point.

## Fix or add a row

1. Edit `data/directories.csv` only. `directories.md` / `directories.jsonl` / `stats.json` are generated.
2. Keep the schema from `data/SCHEMA.md` — same 19 columns, same enum values.
3. Write observations, not opinions:
   - good: `2026-11-20 复核：免费档要求页脚挂 badge，价格页第二屏写明「永久保留」`
   - bad: `看起来要收费`
4. Set `verified` to `YYYY-MM-DD` (or `YYYY-MM-DD 实测（已提交）` etc.). If you did not open the site, leave `未核验` and use `priority = U`.
5. Re-render and validate:
   ```bash
   python3 tools/gen_md.py && python3 tools/validate.py
   ```
   Both must pass; CI runs the same commands.

## Rules for a new row

- One row per directory. Dedupe on `domain`.
- `submit_url` must be the page that actually has the form, not the homepage. If it is an email pitch, `mailto:` is fine.
- `priority` reflects the submission decision, not the site's popularity. `X` needs a reason in `notes`.
- Do not add affiliate links, paid-submission services, "we submit for you" agencies, or lists of lists.
- Do not add personal data: your email, handles, tokens, screenshots with account names. `validate.py` warns on email-like strings for exactly this reason.

## Change the docs or tools

- Keep the Python scripts dependency-free (stdlib only) — they must run on a clean `python3`.
- `AGENTS.md` is a contract, not prose. If you change a rule, change the corresponding line in `skill/backlink-submission-assistant/SKILL.md` too.
- Two READMEs (`README.md`, `README.zh-CN.md`) must stay in sync on facts: row counts, badge counts, file layout.

## Pull requests

- One logical change per PR (a batch of new sites, one site fix, one doc improvement).
- Say what you observed and when, and include the receipt/URL when you claim a submission works.
- If a claim cannot be verified, mark it as unverified instead of deleting it. History matters: "used to be free, now charges" is the signal the next person needs.

## Reporting instead of coding

Open a "Directory report" issue with the domain, what you saw, the date, and (for price/badge claims) where on the page you saw it. That is enough — someone will fold it into the table.

## Code of conduct

Be accurate, be specific, and do not turn the issue tracker into link-building. Submissions promoting a product will be treated as spam.
