#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate data/directories.csv before committing.

Checks
- required columns present, no empty site/domain/priority, ids unique
- enum sanity: priority in P0/P1/P2/P3/U/X, submit_url starts with http(s)
- generated files are up to date (delegates to gen_md.py --check)
- soft warnings: email-like strings (must be a public site contact, not a personal address),
  rows whose notes are empty, DR values outside 0-100

Usage: python3 tools/validate.py
Exit code 1 on errors, 0 otherwise (warnings do not fail the build).
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "directories.csv")

REQUIRED = ["id", "priority", "site", "domain", "submit_url", "type", "fit", "tags", "dr",
            "price", "link_rel", "badge", "account", "review", "notes", "verified",
            "src_category", "src_method", "src_requirement"]
PRIORITIES = {"P0", "P1", "P2", "P3", "U", "X"}

# Public contact addresses that legitimately appear in site notes. Anything else is
# treated as a possible personal address and must be scrubbed before committing.
ALLOWED_EMAILS = {
    "mgnews@majorgeeks.com",
    "hey@aiartapps.com",
    "hi@surges.co",
    "contact@feedmystartup.com",
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def main():
    errors, warnings = [], []

    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        rows = list(reader)

    missing = [c for c in REQUIRED if c not in cols]
    if missing:
        errors.append("missing columns: " + ", ".join(missing))

    seen = set()
    for i, r in enumerate(rows, start=2):
        line = "line %d" % i
        rid = (r.get("id") or "").strip()
        if not rid:
            errors.append(line + ": empty id")
        elif rid in seen:
            errors.append(line + ": duplicate id " + rid)
        seen.add(rid)

        if (r.get("priority") or "").strip() not in PRIORITIES:
            errors.append(line + " (#%s): bad priority %r" % (rid, r.get("priority")))
        for c in ("site", "domain"):
            if not (r.get(c) or "").strip():
                errors.append(line + " (#%s): empty %s" % (rid, c))
        url = (r.get("submit_url") or "").strip()
        if url and not url.startswith(("http://", "https://", "mailto:")):
            errors.append(line + " (#%s): submit_url is not a URL: %r" % (rid, url))
        dr = (r.get("dr") or "").strip()
        if dr:
            try:
                if not 0 <= float(dr) <= 100:
                    warnings.append(line + " (#%s): DR out of range: %s" % (rid, dr))
            except ValueError:
                warnings.append(line + " (#%s): DR is not numeric: %s" % (rid, dr))
        if not (r.get("notes") or "").strip():
            warnings.append(line + " (#%s): empty notes" % rid)

        for field, value in r.items():
            for m in EMAIL_RE.findall(value or ""):
                if m.lower() not in ALLOWED_EMAILS:
                    warnings.append(line + " (#%s): email-like string in %s: %s" % (rid, field, m))

    # generated files must match the CSV
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import gen_md  # noqa: E402

    data = gen_md.load()
    for path, content in (
        (gen_md.MD_PATH, gen_md.build_md(data)),
        (gen_md.JSONL_PATH, gen_md.build_jsonl(data)),
        (gen_md.STATS_PATH, gen_md.json.dumps(gen_md.build_stats(data), ensure_ascii=False, indent=2) + "\n"),
    ):
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if current != content:
            errors.append("stale generated file: %s (run python3 tools/gen_md.py)" % os.path.relpath(path, ROOT))

    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print("\n%d rows · %d error(s) · %d warning(s)" % (len(rows), len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
