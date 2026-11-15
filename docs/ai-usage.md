# Using this repo with an AI agent

The kit is built to be consumed by an agent, not just read by a human. Three ways to wire it up.

## 1. Point the agent at the repo (works everywhere)

Any agent that can read files and run shell commands (Claude Code, Codex, Cursor, Cline, WorkBuddy, Gemini CLI…) needs one instruction:

> Read `AGENTS.md` in `[repo path]`, then follow it. My product pack is at `[path]`.

`AGENTS.md` is the contract: read order, hard rules, workflow, and the exact ledger format the run must end with. Most agents pick it up automatically when the repo is the working directory.

Add `templates/agent-prompt.md` when you want a ready-made task prompt (plan-only, single site, audit, extend-the-table variants).

## 2. Install the skill

The `skill/backlink-submission-assistant/` folder is a portable skill (frontmatter + workflow + traps). Install by copying or symlinking it into your tool's skill directory and setting `BACKLINK_KIT` to the repo root:

```bash
git clone https://github.com/oiov/backlink-submission-kit ~/backlink-submission-kit
export BACKLINK_KIT=~/backlink-submission-kit      # add to ~/.zshrc

# Claude Code / Claude skills
ln -s "$BACKLINK_KIT/skill/backlink-submission-assistant" ~/.claude/skills/backlink-submission-assistant

# WorkBuddy
ln -s "$BACKLINK_KIT/skill/backlink-submission-assistant" ~/.workbuddy/skills/backlink-submission-assistant
```

Then a request like *"submit my product to 10 free directories"* loads the skill and it reads the table instead of inventing a list.

## 3. Just ask the questions (no install)

Even without skills or shell access, an agent given the repo URL can answer useful things — the data is plain CSV/JSONL:

```bash
# what a machine reads
curl -s https://raw.githubusercontent.com/oiov/backlink-submission-kit/main/data/directories.jsonl | head -1
```

## What the agent needs to actually submit

| Capability | Why | Without it |
| --- | --- | --- |
| File read + shell | run `tools/query.py`, write the ledger | it can still plan, cannot execute |
| Browser automation with a persistent profile | form filling, Google OAuth, reading the verification inbox | hand the plan to a human |
| A logged-in browser profile | most `P1` sites need an account; captchas and OTPs need a human anyway | expect more `blocked` rows |

Recommended setup: one persistent browser profile with the project's designated email logged in (Gmail), Google OAuth available, and the agent instructed to hand the tab back on any permission prompt.

## What the agent must never do

`AGENTS.md` §2 is the full list; the three that matter most in practice: **do not invent product facts to fill a required field**, **do not accept a reciprocal badge or pay to get past a step**, and **do not report `submitted` as `live`**.

## Practical notes from real runs

- Batch size is the main quality lever: 8–12 sites per run. Agents are happy to do 40 and will then lose half the receipts.
- Have the agent print the shortlist *before* opening a browser. Wrong-category submissions are the most expensive mistake and the easiest to catch on a list.
- Keep the ledger as a file in the repo/folder, not in chat. The next session only sees files.
- Ask for the "what only I can do" list at the end — captchas, SMS, domain-email DNS, link-exchange decisions.
