#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query the directory pool: filter by project shape, priority, tag, price, badge, DR.

This is the script an agent should call instead of parsing the CSV by hand.
Zero dependencies (stdlib only).

Examples:
    python3 tools/query.py --shape opensource --free --no-badge
    python3 tools/query.py --shape generic --priority P0,P1 --json
    python3 tools/query.py --tag AI --min-dr 50 --limit 10
    python3 tools/query.py --ids 1,3,12 --json
    python3 tools/query.py --search captcha
    python3 tools/query.py --shapes            # list known shapes with counts
"""
import argparse
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "directories.csv")

SHAPES = {
    "generic": "通用",
    "opensource": "开源",
    "desktop": "桌面软件",
    "extension": "浏览器扩展",
    "ai": "AI",
    "chinese": "中文",
    "saas": "SaaS",
    "launch": "发布/Startup",
    "mobile": "移动应用",
    "content": "内容",
}
PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "U": 4, "X": 5}
NO_BADGE_TOKENS = ("无", "—", "未发现")
UNKNOWN_TOKENS = ("未标注", "待核验", "未知", "")


def load():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k, v in r.items():
            if isinstance(v, str):
                r[k] = v.strip()
        try:
            r["dr"] = float(r["dr"]) if r["dr"] else None
        except ValueError:
            r["dr"] = None
    return rows


def is_free(r):
    p = (r["price"] or "").lower()
    if not p or p in ("—", "待核验"):
        return None
    if "无免费" in p or "只有付费" in p:
        return False
    return ("免费" in p) or ("$0" in p) or p.startswith("free")


def badge_state(r):
    b = r["badge"] or ""
    if b in UNKNOWN_TOKENS:
        return "unknown"
    if b.startswith(NO_BADGE_TOKENS):
        return "none"
    return "required"


def doc(r):
    return "https://%s" % r["domain"].replace("https://", "").replace("http://", "").strip("/")


def text_out(rows, show_notes=True):
    if not rows:
        return "no match"
    w = [3, 26, 9, 6, 7]
    out = []
    for r in rows:
        out.append("#%-5s %-30s %-6s DR%-4s %s" % (
            r["id"], r["site"][:30], r["priority"], ("%.0f" % r["dr"]) if r["dr"] else "-",
            "free" if is_free(r) is True else ("paid" if is_free(r) is False else "?")))
        out.append("      %s" % r["submit_url"])
        meta = "      badge:%s · account:%s · review:%s" % (
            badge_state(r), (r["account"] or "-")[:28], (r["review"] or "-")[:24])
        out.append(meta)
        if show_notes and (r["notes"] or ""):
            note = r["notes"].replace("\n", " ")
            out.append("      → %s" % (note if len(note) <= 160 else note[:159] + "…"))
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Filter the backlink directory pool.")
    ap.add_argument("--shape", help="project shape: " + " / ".join(SHAPES))
    ap.add_argument("--shapes", action="store_true", help="list shapes with counts and exit")
    ap.add_argument("--priority", help="comma separated: P0,P1,P2,P3,U,X")
    ap.add_argument("--tag", help="substring match on the tags column, e.g. AI / 通用 / 中文")
    ap.add_argument("--type", help="substring match on the site-type column, e.g. 目录 / 下载站")
    ap.add_argument("--fit", help="substring match on the fit column, e.g. 通用 means any product")
    ap.add_argument("--search", help="substring match across site/domain/notes")
    ap.add_argument("--ids", help="comma separated row ids")
    ap.add_argument("--min-dr", type=float, help="minimum DR")
    ap.add_argument("--free", action="store_true", help="only sites whose recorded price mentions a free tier")
    ap.add_argument("--no-badge", action="store_true", help="only sites recorded as not requiring a reciprocal badge")
    ap.add_argument("--dofollow", action="store_true", help="only sites recorded as dofollow")
    ap.add_argument("--verified", action="store_true", help="only sites with a real verification date")
    ap.add_argument("--limit", type=int, default=0, help="max rows (0 = all)")
    ap.add_argument("--sort", default="priority", choices=["priority", "dr", "id", "site"])
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--brief", action="store_true", help="hide notes in text output")
    args = ap.parse_args()

    rows = load()

    if args.shapes:
        for key, label in SHAPES.items():
            n = sum(1 for r in rows if label in (r["tags"] or ""))
            print("%-12s %-10s %d" % (key, label, n))
        return 0

    sel = rows
    if args.shape:
        label = SHAPES.get(args.shape.lower())
        if not label:
            print("unknown shape %r, try: %s" % (args.shape, ", ".join(SHAPES)), file=sys.stderr)
            return 2
        sel = [r for r in sel if label in (r["tags"] or "")]
    if args.priority:
        want = {p.strip().upper() for p in args.priority.split(",")}
        sel = [r for r in sel if r["priority"].upper() in want]
    if args.tag:
        sel = [r for r in sel if args.tag.lower() in (r["tags"] or "").lower()]
    if args.type:
        sel = [r for r in sel if args.type.lower() in (r["type"] or "").lower()]
    if args.fit:
        sel = [r for r in sel if args.fit in (r["fit"] or "")]
    if args.ids:
        want = {x.strip() for x in args.ids.split(",")}
        sel = [r for r in sel if r["id"] in want]
    if args.search:
        q = args.search.lower()
        sel = [r for r in sel if q in " ".join(
            [r["site"], r["domain"], r["notes"], r["type"], r["tags"]]).lower()]
    if args.min_dr is not None:
        sel = [r for r in sel if r["dr"] is not None and r["dr"] >= args.min_dr]
    if args.free:
        sel = [r for r in sel if is_free(r) is True]
    if args.no_badge:
        sel = [r for r in sel if badge_state(r) == "none"]
    if args.dofollow:
        sel = [r for r in sel if (r["link_rel"] or "").startswith("dofollow")]
    if args.verified:
        sel = [r for r in sel if r["verified"] and r["verified"] != "未核验"]

    if args.sort == "priority":
        sel.sort(key=lambda r: (PRIORITY_RANK.get(r["priority"], 9), -(r["dr"] or 0), int(r["id"]) if r["id"].isdigit() else 0))
    elif args.sort == "dr":
        sel.sort(key=lambda r: -(r["dr"] or 0))
    elif args.sort == "id":
        sel.sort(key=lambda r: int(r["id"]) if r["id"].isdigit() else 0)
    else:
        sel.sort(key=lambda r: r["site"])

    if args.limit:
        sel = sel[: args.limit]

    if args.json:
        out = []
        for r in sel:
            d = dict(r)
            d["id"] = int(d["id"]) if d["id"].isdigit() else d["id"]
            d["url"] = doc(r)
            d["free"] = is_free(r)
            d["badge_state"] = badge_state(r)
            out.append(d)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("%d match(es)\n" % len(sel))
        print(text_out(sel, show_notes=not args.brief))
    return 0


if __name__ == "__main__":
    sys.exit(main())
