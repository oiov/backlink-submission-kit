# Changelog

All notable changes to this kit. Format loosely follows Keep a Changelog; dates are ISO.

## 0.1.0 — 2026-11-15

First public release.

### Added
- `data/directories.csv` — 452 directories × 19 columns, 262 verified in a real browser.
- Generated views: `data/directories.md` (readable), `directories.jsonl` (machine), `stats.json` (aggregates), `data/SCHEMA.md` (field dictionary + Chinese glossary).
- `AGENTS.md` — the agent contract: read order, 10 hard rules, 5-step workflow, ledger output format, hand-off conditions.
- `playbook/` — materials (13 items), batching + red lines, per-site flow + recording, gotchas, maintenance.
- `skill/backlink-submission-assistant/` — portable skill (SKILL.md + `agents/openai.yaml`) built on the same rules.
- `templates/` — ledger, product pack, agent prompt.
- `examples/example-product/` — filled pack + a realistic finished ledger.
- `tools/query.py` (filter the pool, `--json`), `tools/gen_md.py` (re-render), `tools/validate.py` (schema + privacy + staleness checks).
- `docs/` — ai-usage, faq, data-notes (provenance, scrubbing, corrections).
- CI: validates schema, privacy warnings and generated-file freshness on every push/PR.

### Notes on the data
- Personal contact addresses and account handles were removed before publication; product names that serve as evidence were kept.
- Manual corrections: LibHunt reclassified `X` → `P0` (it had only been closed because the author's repo was already listed), ToolFame entry URL cleared, Surge/Vercel entry URLs pointed at the site instead of a CLI command, Hacker Noon DR normalised to a number.
