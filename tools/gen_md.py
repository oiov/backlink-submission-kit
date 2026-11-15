#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render data/directories.md, data/directories.jsonl and data/stats.json from data/directories.csv.

CSV is the single source of truth. Never hand-edit the generated files.

Usage:
    python3 tools/gen_md.py            # regenerate everything
    python3 tools/gen_md.py --check    # exit 1 if generated files are stale (used by CI)
"""
import argparse
import collections
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "directories.csv")
MD_PATH = os.path.join(ROOT, "data", "directories.md")
JSONL_PATH = os.path.join(ROOT, "data", "directories.jsonl")
STATS_PATH = os.path.join(ROOT, "data", "stats.json")

# One-line "what you actually need to know" per domain, hand-written from real runs.
SHORT = {
    "indiehackers.com": "提交即产品页；补完 /edit 并勾 published 才进目录",
    "saashub.com": "分类至少 3 个，竞品是独立步骤必须走完",
    "libhunt.com": "只收开源仓库，自动批准，最省事的一条",
    "peerpush.com": "排队期条目对外不可见，别指望马上有流量",
    "uneed.best": "抓取的文案和标签会错，必须手改；免费需当日 upvote≥10 保条目、≥20 保 dofollow",
    "pitchwall.co": "Nuxt 表单，字段要一次性同步写入；截图≥50KB",
    "nosignuptools.com": "图标/截图走隐藏 input；提交后表单清空不是失败",
    "freenosignup.com": "只收“完全无需注册”的在线工具",
    "somuch.com": "先勾 Submission Guidelines；描述≤255 字符；3 天内验邮件",
    "tinystartups.com": "抓取会把 tagline 塞进 Name；没有免费发布按钮，保存即完成",
    "launchingnext.com": "先关 cookie 横幅再点提交；有算术验证码",
    "activesearchresults.com": "零成本低价值，只当基础收录",
    "bbs.ss": "中文站；≥500 字、封面必填、新号 30 天约 2 个作品",
    "meta.appinn.net": "中文站；标题禁带网址、一产品一帖、新号前几帖人工审",
    "osalt.com": "Homepage 千万别带结尾斜杠",
    "10015.io": "react-select 要按坐标点选，回车无效；免费档 nofollow",
    "appsgit.com": "需可自托管 + 安装文档 + 12 个月内有活动",
    "awesomeindie.com": "先存草稿再点提交；通过后排期到下一季度",
    "chrome.google.com": "只有“浏览器扩展”形态适用；一次性 $5 开发者注册",
    "medium.com": "内容型，外链 nofollow，价值在引荐流量",
    "substack.com": "长期 newsletter 资产，单篇外链价值有限",
    "dev.to": "写技术向文章；正文外链 nofollow",
    "hashnode.com": "要先建 blog 再发文，长文成本高",
    "github.com": "周刊按固定格式收自荐，用作者本人账号提交",
    "f6s.com": "访问需过 Cloudflare 人机校验",
    "startupstash.com": "11 题 Typeform；分类里没有视频/下载项",
    "toolradar.com": "需 @自有域名 工作邮箱或 DNS 记录验证公司",
    "peerlist.io": "先完成 profile 验证（Get verified to Launch）",
    "toolscout.ai": "只收 AI 产品，非 AI 别硬塞",
}

XGROUP = {
    "品类/形态不符": ["alternativeto.net", "alternative.me", "productivity.directory", "devhunt.org",
                 "business.google.com", "pages.github.com", "ycombinator.com", "climate.stripe.com",
                 "cal.com", "aitools.neilpatel.com", "paa.ge", "sideprojectors.com", "financesonline.com"],
    "要徽章或回链才给外链": ["saasfame.com", "newtool.site", "toolfame.com", "twelve.tools", "fazier.com",
                    "startupfa.st", "tinylaunch.com", "betterlaunch.co"],
    "只有付费入口": ["microlaunch.net"],
    "入口失效 / 无法提交": ["filehippo.com", "promoteproject.com", "resource.fyi", "startups.fyi",
                  "sitelike.org", "saaspo.com", "startupbuffer.com", "opensourcesoftwaredirectory.com",
                  "lead.dev", "fosshub.com", "snapfiles.com"],
    "不是提交站（媒体/代投/服务）": ["techcrunch.com", "venturebeat.com", "smashingmagazine.com", "review.firstround.com",
                           "mixergy.com", "foundr.com", "saastr.com", "dzone.com", "vocal.media", "submitator.com"],
    "有硬性声明门槛": ["softpedia.com"],
}
XSEEN = set(x for v in XGROUP.values() for x in v)


def cell(s, n=120):
    s = (s or "").replace("|", "／").replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def load():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def table(rows, pri):
    out = ["| # | Site | Submit | Account | Price | Review | Key point / gotcha |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        if r["priority"] != pri:
            continue
        key = SHORT.get(r["domain"]) or cell(r["notes"], 78)
        out.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            r["id"], r["site"], cell(r["submit_url"], 52), cell(r["account"], 24),
            cell(r["price"], 30), cell(r["review"], 22), key))
    return "\n".join(out)


def build_md(rows):
    by = {r["domain"]: r for r in rows}
    cnt = collections.Counter(r["priority"] for r in rows)
    verified_n = sum(1 for r in rows if r["verified"] and r["verified"] != "未核验")
    ai_u = sum(1 for r in rows if r["priority"] == "U" and "AI" in (r["tags"] or ""))

    def ref(d):
        return "`#%s` %s" % (by[d]["id"], by[d]["site"]) if d in by else ""

    def route(title, must, more, tip):
        out = ["### " + title, ""]
        out.append("**先做：** " + "、".join(ref(d) for d in must if d in by))
        if more:
            out += ["", "**再做：** " + "、".join(ref(d) for d in more if d in by)]
        out += ["", tip, ""]
        return out

    L = []
    a = L.append
    a("# Directories — the master table")
    a("")
    a("> Machine-readable versions: [`directories.csv`](directories.csv) (source of truth) · "
      "[`directories.jsonl`](directories.jsonl) (one JSON object per line, for agents) · "
      "[`SCHEMA.md`](SCHEMA.md) (field dictionary).")
    a("> Generated from the CSV by `python3 tools/gen_md.py` — **do not edit this file by hand**.")
    a("> Snapshot of %d sites, of which %d were opened or actually submitted. Notes are in Chinese on purpose: "
      "they carry the real field IDs, captcha types and traps. See `SCHEMA.md` for an English glossary." % (len(rows), verified_n))
    a("")
    a("## 0. 三分钟上手")
    a("")
    a("1. 先判断项目形态，去第 2 节挑对应路线（A 通用 / B 开源 / C 桌面 / D 扩展 / E AI / F 中文）。")
    a("2. 路线里列出的 `#序号` 就是本表行号，直接按顺序做；每条都写了入口、账号要求、费用和坑。")
    a("3. 每投完一条，在**自己的台账**里记一行（日期 / 状态 / 回执或条目 URL），模板见 `templates/ledger.md`。")
    a("4. P0 做完再从 P1 → P2 往下补；**P3 和 X 不要默认做**，前者要商业决策，后者是明确不投。")
    a("5. 用 agent 干活的，直接把 [`AGENTS.md`](../AGENTS.md) 丢给它，或跑 "
      "`python3 tools/query.py --shape generic --free --no-badge --json` 拿候选站。")
    a("")
    a("## 1. 优先级与统计")
    a("")
    a("| 档位 | 含义 | 数量 | 怎么用 |")
    a("| --- | --- | --- | --- |")
    a("| **P0** | 已实测跑通：免费、无回链、可自助提交 | %d | 新项目开工就做，成功率最高 |" % cnt["P0"])
    a("| **P1** | 相关且值得做，但需账号 / 需现场核验 | %d | P0 做完接着做 |" % cnt["P1"])
    a("| **P2** | 低价值、nofollow 或门槛高 | %d | 补量用，别指望权重 |" % cnt["P2"])
    a("| **P3** | 需商业决策：互换链接 / 付费 / 榜单 Top3 | %d | 先问要不要做，再执行 |" % cnt["P3"])
    a("| **U** | 未核验池（批量收录，信息不足） | %d | 按品类筛，做前现场核验 |" % cnt["U"])
    a("| **X** | 不投：品类不符 / 硬门槛 / 入口失效 / 非目录 | %d | 看第 7 节原因，别浪费时间 |" % cnt["X"])
    a("")
    a("已实测（打开过页面、跑过表单）**%d** 条。`priority` 是投递优先级，不是质量评分；"
      "`verified` 才是“哪天亲眼看过”的证据。" % verified_n)
    a("")
    a("## 2. 按项目形态选路线")
    a("")
    L += route("A｜通用在线工具 / SaaS（有官网 + 截图就能投）",
               ["indiehackers.com", "saashub.com", "peerpush.com", "uneed.best", "pitchwall.co", "awesomeindie.com"],
               ["tinystartups.com", "launchingnext.com", "activesearchresults.com", "startupstash.com",
                "peerlist.io", "toolradar.com", "f6s.com", "10015.io", "somuch.com"],
               "先做 6 个 P0 打底（每条 10–20 分钟），再补第二批。第 1 天就能拿到 3–4 条已提交记录。")
    L += route("B｜开源项目（有 GitHub 仓库）",
               ["libhunt.com", "appsgit.com", "osalt.com"],
               ["github.com", "sourceforge.net", "openalternative.co"],
               "开源是最好投的一类：LibHunt 自动批准、appsgit 一周内审、osalt 免登录。仓库要有 LICENSE + README + docker-compose（如有服务端）。OpenAlternative 要 ≥50 star，不够先攒。")
    L += route("C｜桌面客户端（有安装包）",
               ["filehorse.com", "majorgeeks.com"],
               ["softonic.com", "techspot.com", "videohelp.com", "uptodown.dev", "sourceforge.net"],
               "下载站基本都走邮件/人工，要备好安装包直链、版本号、许可证、VirusTotal 干净的包。Softpedia 若代码用过 AI 就跳过（要签“无 AI 参与”声明）。")
    L += route("D｜浏览器扩展",
               ["chrome.google.com"], [],
               "扩展类只有 Chrome Web Store 这一条真正有量；准备好 zip、商店素材（1280×800 截图 ×5）、隐私政策 URL、$5 开发者注册。其余“扩展目录”多为低质，本表未收录。")
    L += route("E｜AI 产品",
               ["toolscout.ai", "futurepedia.io", "toolify.ai"],
               ["theresanaiforthat.com"],
               "U 档里有 %d 条 AI 目录，只收 AI 产品，非 AI 项目整段跳过。先做 3 个有排名的：ToolScout 已核验；Futurepedia、Toolify 未实测，投前先核验免费档。TAAFT 基本要付费。" % ai_u)
    L += route("F｜中文产品 / 中文社区",
               ["bbs.ss", "meta.appinn.net"], [],
               "中文站最容易被忽略但转化最好。出海栈、小众软件都免费且已跑通；另有少数派/电鸭/LINUX DO 需自建账号或新号限权，见台账。")

    a("## 3. P0：%d 条已验证，直接照做" % cnt["P0"])
    a("")
    a("这些站都实际跑通过：免费档能提交、不要求在自己网站放徽章、不需要买加速。坑都写在最后一列。")
    a("")
    a(table(rows, "P0"))
    a("")
    a("## 4. P1：%d 条，P0 之后接着做" % cnt["P1"])
    a("")
    a(table(rows, "P1"))
    a("")
    a("## 5. P2：%d 条补充盘" % cnt["P2"])
    a("")
    a("特点是“能投，但要么 nofollow、要么人工审核、要么要先有客户评价/仓库 star”。用来铺量，别当主力。")
    a("")
    a(table(rows, "P2"))
    a("")
    a("## 6. P3：%d 条，需要先做商业决策" % cnt["P3"])
    a("")
    a("这一档的共同点：**免费档要你把它的链接放到自己网站**（互换），或者只给付费用户 dofollow，或者只在榜单 Top3 才给外链。做不做是产品/SEO 策略问题，不是执行问题。")
    a("")
    a(table(rows, "P3"))
    a("")
    a("## 7. X：%d 条不投，按原因分组" % cnt["X"])
    a("")
    a("不是“以后再说”，是**确认不值得花时间**。新项目开工前扫一眼，省下最贵的成本：时间。")
    a("")
    a("> 注：twelve.tools、Fazier、Startup Fast、TinyLaunch、Better Launch 也要求徽章或互换，但“要不要做”属于策略决定，所以放在第 6 节 P3，不在这里。")
    a("")
    for g, doms in XGROUP.items():
        ds = [d for d in doms if d in by and by[d]["priority"] == "X"]
        if not ds:
            continue
        a("**" + g + "**（%d）" % len(ds))
        a("")
        for d in ds:
            r = by[d]
            a("- `#%s` **%s** — %s" % (r["id"], r["site"], cell(r["notes"], 110)))
        a("")
    rest_x = [r for r in rows if r["priority"] == "X" and r["domain"] not in XSEEN]
    if rest_x:
        a("**其余（标记为功能异常/失效，未实测）**")
        a("")
        for r in rest_x:
            a("- `#%s` **%s** — %s" % (r["id"], r["site"], cell(r["notes"], 90)))
        a("")

    a("## 8. U：%d 条未核验池怎么用" % cnt["U"])
    a("")
    a("其中 **%d 条是 AI 工具目录**（只收 AI 产品，非 AI 项目直接跳过），其余 %d 条是批量收录的综合/SaaS/发布站，信息只有“免费提交 / 需登录”这一级。" % (ai_u, cnt["U"] - ai_u))
    a("")
    a("用法：不要一条条盲投。按下面的方式筛：")
    a("")
    a("1. 跑 `python3 tools/query.py --priority U --tag 通用 --min-dr 40`，或直接筛 CSV 的 `tags` 列；")
    a("2. 按 DR 从高到低，先看 DR≥40 的（有 DR 的约占三成）；")
    a("3. 每个站 30 秒核验三件事：有没有 Add/Submit 入口、免费档是否要徽章、是否有你的品类；")
    a("4. 通过就现场投，投完把这行改成 P0/P1/P2 并把结论写进 `notes`（下次别的项目直接复用）。")
    a("")
    a("## 9. 字段说明")
    a("")
    a("字段字典（含英文对照与枚举值）见 [`SCHEMA.md`](SCHEMA.md)。最常用的几列：")
    a("")
    a("| 字段 | 含义 |")
    a("| --- | --- |")
    a("| `priority` | P0/P1/P2/P3/U/X，定义见第 1 节 |")
    a("| `submit_url` | 已验证的直达提交页；只有主页说明还没找到提交页 |")
    a("| `fit` | 该站**只收**什么类型的产品；“通用”才是任何产品都能投 |")
    a("| `tags` | 归一化后的筛选标签（多值用 / 分隔），筛站先看这一列 |")
    a("| `link_rel` | dofollow / nofollow。`待核验` = 没实测过，别当承诺 |")
    a("| `badge` | 是否要求在自己网站放它的链接或徽章。**这是最主要的取舍点** |")
    a("| `account` | 免账号 / Google 登录 / 仅邮箱密码 / 需域名邮箱… |")
    a("| `review` | 从提交到公开的等待时间；“人工”= 不可预期 |")
    a("| `notes` | 实际踩过的坑，含字段 id、验证码、抓取错位这类只有做过才知道的细节 |")
    a("| `verified` | 实测日期；`未核验` = 来自公开清单，未验证 |")
    a("")
    a("## 10. 维护规则")
    a("")
    a("- **投之前**重新看一眼目标站：费用、徽章、入口三件事都可能变，本表是快照。")
    a("- **投之后**回填两处：自己的台账记这次投递；本表 `notes` 补新踩的坑，并把 `priority` 调准。")
    a("- 新发现的站追加到 CSV（`priority` 先填 U），核验过再升级；改完跑 `python3 tools/gen_md.py`。")
    a("- 每月抽 10 条 P0/P1 复检入口是否还活着；失效的改成 X 并注明日期。")
    a("")
    a("---")
    a("")
    a("Site data: CC0-1.0 · Generated by `tools/gen_md.py` from `directories.csv`.")
    a("")
    return "\n".join(L)


def build_jsonl(rows):
    out = []
    for r in rows:
        d = dict(r)
        d["id"] = int(d["id"]) if d["id"].isdigit() else d["id"]
        try:
            d["dr"] = float(d["dr"]) if d["dr"] else None
        except ValueError:
            d["dr"] = None
        d = {k: (v.strip() if isinstance(v, str) else v) for k, v in d.items()}
        out.append(json.dumps(d, ensure_ascii=False))
    return "\n".join(out) + "\n"


def build_stats(rows):
    def count(col):
        return dict(collections.Counter((r[col] or "").strip() for r in rows).most_common())

    tags = collections.Counter()
    for r in rows:
        for t in (r["tags"] or "").split("/"):
            t = t.strip()
            if t:
                tags[t] += 1
    drs = [float(r["dr"]) for r in rows if r["dr"] and r["dr"].replace(".", "").isdigit()]
    return {
        "total": len(rows),
        "verified": sum(1 for r in rows if r["verified"] and r["verified"] != "未核验"),
        "by_priority": count("priority"),
        "by_tag": dict(tags.most_common()),
        "by_type": dict(collections.Counter((r["type"] or "").strip() for r in rows).most_common(30)),
        "with_dr": len(drs),
        "dr_median": sorted(drs)[len(drs) // 2] if drs else None,
        "updated": max((r["verified"] for r in rows if r["verified"] and r["verified"] != "未核验"), default=""),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 if generated files are out of date")
    args = ap.parse_args()

    rows = load()
    md = build_md(rows)
    jsonl = build_jsonl(rows)
    stats = json.dumps(build_stats(rows), ensure_ascii=False, indent=2) + "\n"

    if args.check:
        stale = []
        for path, content in ((MD_PATH, md), (JSONL_PATH, jsonl), (STATS_PATH, stats)):
            current = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
            if current != content:
                stale.append(os.path.relpath(path, ROOT))
        if stale:
            print("stale: " + ", ".join(stale) + "\nrun: python3 tools/gen_md.py", file=sys.stderr)
            return 1
        print("up to date")
        return 0

    for path, content in ((MD_PATH, md), (JSONL_PATH, jsonl), (STATS_PATH, stats)):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote", os.path.relpath(path, ROOT), len(content), "chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
