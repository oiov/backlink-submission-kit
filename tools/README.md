# Tools

Zero dependencies — Python 3.8+ stdlib only, so they run anywhere without a venv.

| Command | What it does |
| --- | --- |
| `python3 tools/query.py --shapes` | list project shapes with counts |
| `python3 tools/query.py --shape generic --free --no-badge` | the default "new project" shortlist |
| `python3 tools/query.py --priority P0,P1 --json` | machine-readable batch |
| `python3 tools/query.py --search captcha` | find rows with known traps |
| `python3 tools/gen_md.py` | rebuild `directories.md`, `directories.jsonl`, `stats.json` from the CSV |
| `python3 tools/gen_md.py --check` | exit 1 if the generated files are stale (CI) |
| `python3 tools/validate.py` | schema, enum, URL, duplicate-id, privacy and staleness checks |

## query.py flags

```
--shape    generic|opensource|desktop|extension|ai|chinese|saas|launch|mobile|content
--priority P0,P1,P2,P3,U,X
--tag --type --fit --search --ids
--min-dr FLOAT
--free         recorded price mentions a free tier
--no-badge     recorded as not requiring a reciprocal badge
--dofollow     recorded as dofollow
--verified     has a real verification date
--sort priority|dr|id|site   --limit N
--json  --brief
```

`--json` adds three derived keys: `url`, `free` (true/false/null), `badge_state` (`none`/`required`/`unknown`). `null` and `unknown` mean "not recorded" — check live before submitting.

## Adding a tool

Keep it stdlib-only, read `data/directories.csv` as UTF-8-sig, and never write to the generated files from anywhere except `gen_md.py`.
