# Data schema — `directories.csv`

The CSV is the single source of truth. `directories.md`, `directories.jsonl` and `stats.json` are generated from it by `python3 tools/gen_md.py` — never edit those by hand.

- 452 rows × 19 columns · UTF-8 with BOM (so Excel opens it without mojibake)
- One row = one submission destination
- Free-text columns (`notes`, `price`, `account`, `review`) are written in Chinese; they carry the real field IDs, captcha types and traps observed on site. `query.py --json` gives you the same data with English keys.

## Columns

| Column | Type | Meaning | Enum / format |
| --- | --- | --- | --- |
| `id` | int | Row id, stable. Referenced as `#12` in docs. | 1–452 |
| `priority` | enum | Submission priority + qualification state | `P0` `P1` `P2` `P3` `U` `X` |
| `site` | str | Display name of the site | `Uneed` |
| `domain` | str | Bare domain, used as the dedupe key | `uneed.best` |
| `submit_url` | url | Verified direct submission URL (not the homepage) | `https://…`, `mailto:…`, or empty |
| `type` | str | Kind of destination; decides whether it is a directory at all | `综合目录` `发布/Beta 站` `软件下载站` `静态托管` `媒体` `线索页` … |
| `fit` | str | What the site **only** accepts. `通用` = any product | `通用` `AI` `开源（要 GitHub 仓库）` … |
| `tags` | str | Normalised filter tags, `/`-separated, multi-value | `SaaS/通用` `发布/Startup` `AI` `开源` `中文` |
| `dr` | float\|null | Domain Rating at time of verification. `null` = never looked up | 0–100 |
| `price` | str | Cost terms **as recorded on site**, free tier included | `免费` `免费队列（$39 即时可选）` `待核验` |
| `link_rel` | str | Backlink attribute | `dofollow` `nofollow` `待核验` `仅 Top3 才 dofollow` |
| `badge` | str | Whether the free tier forces a reciprocal badge/backlink on **your** site | `无` `未标注` `免费档强制永久保留 badge` |
| `account` | str | Login requirement | `免登录` `Google 登录` `仅邮箱+密码` `需域名邮箱` |
| `review` | str | Time from submission to publication | `提交即上线` `1–12 周` `人工` `3–4 个月` |
| `notes` | str | **The valuable column.** Observed traps: field IDs, captcha type, auto-scrape errors, wizard order, what "free" actually means | free text |
| `verified` | str | Date the row was last checked by a human or agent, plus the outcome | `2026-11-14` `2026-11-08 实测（已提交）` `未核验` |
| `src_category` | str | Original category from the source list this row came from | free text |
| `src_method` | str | Original "how to submit" text from that list | free text |
| `src_requirement` | str | Original "what it requires" text from that list | free text |

## Priority values

| Value | Meaning | How to use it |
| --- | --- | --- |
| `P0` | Ran end-to-end: free tier works, no reciprocal badge, self-serve submission | Do these first |
| `P1` | Relevant and worth it, but needs an account, an email verification, or an unverified step | Second wave |
| `P2` | Real but low value: nofollow, long human review, needs customers/stars first | Volume only |
| `P3` | Requires a business decision: reciprocal link, paid acceleration, Top-3-only dofollow | Ask the human, default no |
| `U` | Unverified pool harvested from public lists; only "free submit / login required" is known | Filter by `tags`, then verify on site |
| `X` | Do not submit: wrong category, hard gate, dead entry, not a directory | Skip |

`priority` is a **submission** decision, not a quality score. `verified` is the evidence: a row can be `P0` and `verified=未核验` only if it is a well-known default (rare — treat it as `U` if you care).

## Chinese glossary for the free-text columns

| Term | English |
| --- | --- |
| 免费 / 免费队列 | free / free queue |
| 待核验 | not verified yet — do not treat as a promise |
| 未标注 | not recorded |
| 免登录 | no account needed |
| 仅邮箱+密码 | email + password only (no Google OAuth) |
| 需域名邮箱 | requires an `@yourdomain` work email |
| 回链 / 徽章 / badge | reciprocal link or badge on your own site |
| 互换链接 | link exchange — a business decision, not a submission |
| 人工审核 | human review, unpredictable duration |
| 抓取错位 | auto-scraper filled the wrong field |
| 验证码 | captcha |
| 卡验证码 / 卡账号 | blocked on captcha / blocked on account |
| 不投 | do not submit (reason follows) |
| 入口失效 | entry point dead (404 / cert error / closed) |

## Machine interface

```bash
# one JSON object per line, English keys, dr as number|null
head -1 data/directories.jsonl

# filtered + enriched (adds url, free, badge_state)
python3 tools/query.py --shape opensource --free --no-badge --json

# aggregates
cat data/stats.json
```

`query.py` treats the recorded values as *evidence*, never as guarantees: `free: null` means "price not recorded", `badge_state: "unknown"` means "not verified" — both require a live check before submitting.

## Syncing with a private master sheet

If you keep your own master sheet in another language/column set, keep this repo as a published snapshot: map your columns to the names above and run `python3 tools/gen_md.py && python3 tools/validate.py`. `docs/data-notes.md` records where this snapshot came from, what was scrubbed, and which rows were manually corrected.
