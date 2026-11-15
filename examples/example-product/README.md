# Example product pack (illustrative)

`ClipNest` is **fictional**. This folder exists to show an agent what "enough information to submit" looks like, and what a finished ledger looks like. The directory ids referenced are real rows from `data/directories.csv`, so you can follow a full run end to end without guessing.

| File | What it demonstrates |
| --- | --- |
| [product-pack.md](product-pack.md) | A filled materials sheet: facts, approved copy at every length, assets, and an explicit "do not claim" list |
| [ledger.md](ledger.md) | A realistic batch: two `live`, three `queued` / `submitted`, two `blocked`, four `skipped` with reasons |

How an agent should use it: read the pack, run `python3 tools/query.py --shape opensource --free --no-badge`, and compare its own shortlist and ledger against the example's structure — not its site choices (yours depend on your shape, traffic goals and appetite for review queues).

Two things this example deliberately gets right:

- **Nothing is claimed that cannot be defended.** The pack has no user count, no "trusted by", no invented founder story — because a reviewer who catches one invented number can reject the whole submission.
- **`skipped` rows carry the reason.** SaaSFame and twelve.tools are skipped for a required badge; Softpedia for the "no AI-written code" declaration; AlternativeTo because it excludes downloaders. Those four lines are why the next batch is faster.
