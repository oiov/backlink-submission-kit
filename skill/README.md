# Skill — backlink-submission-assistant

A portable skill built on the rules in `AGENTS.md` and the data in `data/`. It works as a Claude/WorkBuddy skill, and as a plain instruction file for any agent.

## Install

```bash
git clone https://github.com/oiov/backlink-submission-kit ~/backlink-submission-kit
export BACKLINK_KIT=~/backlink-submission-kit

# Claude Code / Claude skills
mkdir -p ~/.claude/skills
ln -s "$BACKLINK_KIT/skill/backlink-submission-assistant" ~/.claude/skills/backlink-submission-assistant

# WorkBuddy
mkdir -p ~/.workbuddy/skills
ln -s "$BACKLINK_KIT/skill/backlink-submission-assistant" ~/.workbuddy/skills/backlink-submission-assistant
```

Without `BACKLINK_KIT`, the skill resolves the repo root relative to its own path; symlinks keep that working. If you copy the folder instead of linking, set `BACKLINK_KIT` — otherwise it cannot find `data/directories.csv`.

## Files

| File | Purpose |
| --- | --- |
| `backlink-submission-assistant/SKILL.md` | workflow, rules, hand-off conditions |
| `backlink-submission-assistant/agents/openai.yaml` | display name + default prompt |

The reference material is deliberately not duplicated here: the skill points at `playbook/gotchas.md`, `data/SCHEMA.md` and `templates/ledger.md` in the repo root, so there is one copy of every rule.
