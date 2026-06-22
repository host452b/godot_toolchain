# Godot 生态 Repo 元数据采集 — 设计文档

- 日期:2026-06-22
- 状态:已确认,待实现

## 1. 目标

利用 `gh` CLI 遍历 5 个 Godot 相关 GitHub topic,采集其中 **star ≥ 1000 且最近 3 个月内有 commit 推送(可持续维护)** 的 repo 的基础元数据,供后续数据分析使用。

目标 topic:

- `godot-engine`
- `godot4`
- `godot`
- `godot-addon`
- `gdscript`

## 2. 范围与约束

- **筛选条件(硬性,在采集阶段就过滤)**
  - `stars >= 1000`
  - `pushed_at >= 运行日往前推 3 个月`(活跃 / 未烂尾信号)
- **不去重**:采集阶段保留跨 topic 的重复 repo,每个 topic 的结果各自落盘。去重只发生在后续装载 / 分析阶段。
- **元数据深度**:仅采集 `gh search repos` 一次调用即可返回的基础字段(不做每 repo 的额外 API 请求)。
- **必须记录 repo 地址**(`url` 字段)。
- GitHub 搜索 API 每个查询最多返回 1000 条;`--limit 1000` 兜底(实际带 star≥1000 过滤后通常远少于 1000)。
- 搜索 API 限速约 30 次/分钟;5 个 topic 各 1 次调用,远低于限制。

## 3. 架构(两阶段)

```
阶段 A 采集(不去重)              阶段 B 装载(去重 + 可查询)
gh search repos  ──►  data/raw/<topic>.jsonl  ──►  load.py  ──►  godot.db (SQLite)
   (5 个 topic 依次跑)            每行一个 repo                     repos 表 + repo_topics 关联表
```

- **`collect.sh`**:依次遍历 5 个 topic,每个 topic 一次 `gh search repos` 调用,结果原样写入 `data/raw/<topic>.jsonl`(一行一个 repo JSON,保留跨 topic 重复)。失败记录到 `data/raw/errors.log` 并继续下一个 topic。
- **`load.py`**:读取所有 `data/raw/*.jsonl`,装入 SQLite `godot.db`。`repos` 表按 `full_name` 去重(`INSERT OR REPLACE`);`repo_topics` 关联表记录每个 repo 在每个 topic 下的命中与排名。
- 原始 JSONL 永久保留,可随时重跑装载,不丢数据。

## 4. 采集命令(核心)

```bash
CUTOFF=$(date -v-3m +%Y-%m-%d)   # macOS;今天跑 = 2026-03-22

gh search repos "pushed:>=$CUTOFF" \
  --topic <topic> \
  --stars '>=1000' \
  --sort stars --order desc \
  --limit 1000 \
  --json fullName,name,owner,description,url,homepage,\
stargazersCount,forksCount,openIssuesCount,language,license,\
isArchived,isFork,isDisabled,defaultBranch,size,\
createdAt,updatedAt,pushedAt
```

说明:

- `url` 字段即完整 https repo 地址。
- 活跃过滤用 GitHub 搜索语法的位置参数 `pushed:>=$CUTOFF`,而非 `--pushed` 旗标(`gh search repos` 无此旗标)。
- `gh search repos` 的 JSON 不直接返回 topics 字段,因此 "repo ↔ topic" 归属由采集循环中已知的当前 topic 决定,写入 `repo_topics` 表。
- 输出为 JSON 数组;`collect.sh` 用 `jq -c '.[]'` 转成每行一个对象(JSONL)落盘。

## 5. 数据结构(SQLite)

### `repos` 表(主键 `full_name`,跨 topic 去重)

| 列 | 类型 | 说明 |
|---|---|---|
| full_name | TEXT PK | `owner/name`,唯一标识 |
| name | TEXT | repo 名 |
| owner | TEXT | owner 登录名 |
| url | TEXT | repo 地址(https) |
| homepage | TEXT | 主页 URL |
| description | TEXT | 描述 |
| stars | INTEGER | stargazers 数 |
| forks | INTEGER | fork 数 |
| open_issues | INTEGER | open issue 数 |
| language | TEXT | 主语言 |
| license | TEXT | SPDX key |
| is_archived | INTEGER | 0/1 |
| is_fork | INTEGER | 0/1 |
| is_disabled | INTEGER | 0/1 |
| default_branch | TEXT | 默认分支 |
| size | INTEGER | 仓库大小(KB) |
| created_at | TEXT | ISO 时间 |
| updated_at | TEXT | ISO 时间 |
| pushed_at | TEXT | ISO 时间 |
| collected_at | TEXT | 采集时间戳(装载时写入) |

### `repo_topics` 表(多对多,保留 topic 归属与排名)

| 列 | 类型 | 说明 |
|---|---|---|
| full_name | TEXT | 外键 → repos.full_name |
| topic | TEXT | 5 个 topic 之一 |
| rank_in_topic | INTEGER | 在该 topic 内按 star 降序的名次(1 起) |
| 主键 | (full_name, topic) | |

索引建议:`repos(stars)`、`repos(language)`、`repo_topics(topic)`。

## 6. 错误处理 / 重跑

- 单个 topic 调用失败 → 写 `data/raw/errors.log`,不中断,继续下一个。
- 重跑安全:JSONL 覆盖写;SQLite `INSERT OR REPLACE`(repos)/ `INSERT OR REPLACE`(repo_topics)。

## 7. 产出文件

```
collect.sh                    # 阶段 A 采集脚本
load.py                       # 阶段 B 装载脚本
data/raw/godot-engine.jsonl
data/raw/godot4.jsonl
data/raw/godot.jsonl
data/raw/godot-addon.jsonl
data/raw/gdscript.jsonl
data/raw/errors.log
godot.db                      # SQLite,供后续分析
```

## 8. 后续分析(超出本 spec,仅说明数据可支持)

- 按 star/fork 排名、语言分布、license 分布、活跃度(pushed_at)分析。
- 通过 `repo_topics` 做 topic 交叉与重叠分析。
