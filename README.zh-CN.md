# backlink-submission-kit

**一份「真跑过」的免费外链目录合集 + 一套能让 AI 直接执行的外链投递打法。**

[![directories](https://img.shields.io/badge/站点-452-2f6fed)](data/directories.md)
[![verified](https://img.shields.io/badge/实测-262-1a9c6b)](data/stats.json)
[![code](https://img.shields.io/badge/代码-MIT-blue)](LICENSE)
[![data](https://img.shields.io/badge/数据-CC0-lightgrey)](LICENSE-DATA)
[![English](https://img.shields.io/badge/README-English-informational)](README.md)

不是那种「5000 个外链站一键提交」的清单。这里 **452 条**，其中 **262 条**是真在浏览器里打开过、甚至走完过提交流程的；每条都写清了哪个字段会崩、哪个「免费」其实要你挂横幅、哪个站根本不收你这个品类。

## 它解决什么问题

每个外链清单都让你投 300 个站，没人告诉你：

- SaaSFame 的 `$0` 档要你把它的 badge **永久**挂在自己站点上 —— 这是互换链接，不是免费收录；
- 10015.io 免费队列是 nofollow，还要排 3–4 个月；
- Softpedia 的表单第一项是「本应用不含 AI 编写的代码」—— 这是事实性声明，你不一定签得了；
- Uneed 的免费条目要当天拿到 10 个赞才不被删；
- 一份没人维护的清单，一年后有一半是 404。

这个仓库是把这些站**真投一遍**之后剩下的东西：一张记着坑的表、一套不会让你浪费审核机会的流程、一个能让下一个项目不用从零摸的记账格式。

## 里面有什么

| 组件 | 内容 |
| --- | --- |
| **452 个站点** | `P0` 27 条已验证「免费 + 不要回链 + 可自助」 · `P1` 13 条需账号 · `P2` 44 条补量 · `P3` 22 条需商业决策 · `U` 243 条待核验 · `X` 103 条明确不投（都写了原因） |
| **一套打法** | 13 项物料清单、排批策略、单站 5 步、7 条红线、表单/站点/浏览器的坑速查 |
| **一个 skill** | `skill/backlink-submission-assistant/`，丢进 Claude Code / WorkBuddy 就能让它按流程跑一批 |
| **给 AI 的接口** | `AGENTS.md`（规则与输出格式）、`data/directories.jsonl`、`tools/query.py --json`、示例物料包与台账 |
| **工具** | 零依赖 Python：筛站、重渲文档、校验数据 |

```
backlink-submission-kit/
├── AGENTS.md              ← AI 从这里开始（硬规则 + 记账格式）
├── README.md / README.zh-CN.md
├── data/                  ← CSV（唯一数据源）+ 渲染版 MD/JSONL/统计 + 字段字典
├── playbook/              ← 物料清单 / 排批 / 单站流程 / 通用坑 / 维护
├── skill/backlink-submission-assistant/   ← SKILL.md + agent 配置
├── templates/             ← 台账模板 / 物料包模板 / agent 提示词
├── examples/example-product/  ← 一个填好的示例物料包 + 一份真实形态的台账
├── tools/                 ← query.py / gen_md.py / validate.py
├── docs/                  ← ai-usage / faq / data-notes（数据来源与脱敏）
└── llms.txt               ← 给 AI 的入口索引
```

## 60 秒上手

```bash
git clone https://github.com/oiov/backlink-submission-kit
cd backlink-submission-kit

python3 tools/query.py --shapes                                      # 有哪几种项目形态
python3 tools/query.py --shape generic --free --no-badge --limit 12  # 拉第一批候选站
```

每条结果直接给提交入口、账号要求、审核时长，和「通常会卡在哪」。

然后：

1. 复制 `templates/product-pack.md`，按 `playbook/materials.md` 的 13 项物料填齐。**定价、平台、分类这三项说不准就别猜。**
2. 复制 `templates/ledger.md` 建这个项目的台账。
3. 照 `playbook/per-site-flow.md` 单站推进；表单卡住先翻 `playbook/gotchas.md`。
4. 每投完一个站立刻记一行，再开下一个。`已提交` 不等于 `已上线`。

## 表格长什么样

| # | 站点 | 优先级 | DR | 费用 | 回链 | 账号 | 现场备注（摘要） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | LibHunt | P0 | – | 免费 | 无 | 仓库 URL | 真入口是 `/repo/submit`，只填仓库 URL，自动批准；重复提交会提示「已提交过」，那是成功不是失败 |
| 3 | Uneed | P0 | 74 | 免费队列（约 4 个月） | 无 | Google | 自动抓取的文案和标签会错；免费条目当天 ≥10 赞才保留、≥20 赞才保 dofollow |
| 378 | Softpedia | X | – | 免费 | 无 | – | 要签「无 AI 参与编写」声明 + 32×32 图标 + 图片验证码 —— 声明不成立就别投 |
| 68 | Fazier | P3 | 82 | 「免费」 | **要** | – | 免费档要你在页脚挂它的链接，属互换，默认不做 |

完整表：[`data/directories.md`](data/directories.md)｜字段说明：[`data/SCHEMA.md`](data/SCHEMA.md)｜数据来源、删了什么、改过哪几行：[`docs/data-notes.md`](docs/data-notes.md)

## 让 AI 来干

```bash
export BACKLINK_KIT=~/backlink-submission-kit
ln -s "$BACKLINK_KIT/skill/backlink-submission-assistant" ~/.claude/skills/backlink-submission-assistant
ln -s "$BACKLINK_KIT/skill/backlink-submission-assistant" ~/.workbuddy/skills/backlink-submission-assistant
```

然后一句话：*「读 $BACKLINK_KIT 里的 AGENTS.md，按里面的规则把〈我的产品〉投到前 10 个符合条件的免费目录。」*

它拿到的是「**别干这四件事**」的规则：别瞎编定价档位、别替用户接受挂 badge、别把视频工具塞进 AI 目录、别把待审状态写成已上线。接入细节和提示词模板： [`docs/ai-usage.md`](docs/ai-usage.md)、[`templates/agent-prompt.md`](templates/agent-prompt.md)

## 实践心得：用 WorkBuddy 真跑起来是什么样

这套东西不是先写好再去用的，是反过来的：五个产品、262 个站在浏览器里真开过，填表的大部分活儿是 WorkBuddy 开着一个已登录的浏览器窗口干的。下面六条，是决定「这一轮有没有白干」的关键。

**1. 把仓库指给 agent，别把规则粘给它。** 一句话就够：*「读 `$BACKLINK_KIT` 里的 `AGENTS.md`，然后把 `./pack.md` 这份物料包投到接下来 10 个符合条件的 P0 站。」* 规则写在文件里，改一次，以后每一轮都继承；粘在 prompt 里，下一轮就没了，还会越粘越走形。

**2. 一批 8–12 个，别一次给 30 个。** 每批必然会撞上一个收验证邮件、一个图片验证码、一个跳到你没见过的控制台。超过十几个之后，agent 会为了「跑完这一批」开始省掉记账那一步 —— 这是最坏的交换：台账丢了，没核实的「已提交」全留着。

**3. 已登录的浏览器是整套流程的关键。** 一半以上的免费目录把表单藏在 Google / GitHub 登录后面。有持久的浏览器会话，agent 直接到表单；没有的话，每批前二十分钟都在过 OAuth，剩下一半时间在「请先登录」。

**4. 一个专用邮箱，并且让 agent 能读它。** 所有投递统一用一个通用邮箱；站点发确认链接过来，就让它在同一个浏览器里打开那个收件箱把闭环走完。如果 agent 一遇到「验证邮件已发送」就停下，瓶颈就变成了你，这一批基本死在那。两个相关的坑：少数目录把域名邮箱当成自我推广信号、审得更严；还有几家要 DNS TXT 证明域名归属 —— 最后一个确实得你自己来。

**5. 台账才是交付物，收录不是。** agent 会在点下提交按钮的那一刻愉快地报告「完成」。所以要求它每投完一个站在开下一个表单之前写一行：状态、入口 URL、填了什么、还差什么。`已提交` ≠ `已过审` ≠ `已上线`。两周之后，那个文件是唯一能告诉你「四十个提交里哪些还压在队列里」的东西。

**6. 有四件事必须交回给人：** 要挂 badge、要签声明（比如 Softpedia 那句「无 AI 编写代码」）、伪装成免费但要付费、要域名归属证明。这四种 agent 只停下问，不做决定 —— 这是 `AGENTS.md` 里的硬规则，也是其余部分还能算「正当曝光」而不是 spam 的原因。

这些跟 WorkBuddy 本身没多大关系，任何带浏览器和文件系统的 agent 都适用。只是这张表是在这套环境里长出来的。如果你也用 WorkBuddy，skill 的安装方式和上一节一样（`~/.workbuddy/skills/`），`docs/ai-usage.md` 里有实测有效的提示词写法。

## 四条最要紧的规则

1. **`$0` 不等于免费** —— 价格页要翻到底看 badge 条款。
2. **品类不匹配就不投** —— 表单再免费也不硬塞。
3. **投前 30 秒现场复核** —— 费用、回链、入口、品类四件事都会变，表只是快照。
4. **记回执，不记愿望** —— `已提交` ≠ `已过审` ≠ `已上线`。

## 参与

站点挂了、涨价了、发现新站、把备注翻成英文，都欢迎。见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。一句话版本：改 `data/directories.csv`，然后

```bash
python3 tools/gen_md.py && python3 tools/validate.py
```

## 许可证

- 代码、文档、打法、skill：**MIT**（[LICENSE](LICENSE)）
- 站点数据（`data/`）：**CC0-1.0**（[LICENSE-DATA](LICENSE-DATA)），商用、二改、二次分发都随意，无需署名

## 一句实话

这套东西只做**正当**的曝光：免费收录、品类正确、不刷不买不互换。它不承诺排名，表里的数字只是「当时为真」，不是「永远为真」。投之前自己再看一眼——这就是全部方法。
