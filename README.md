# godot_toolchain

采集 Godot 生态 GitHub 仓库元数据的轻量管线。遍历多个 Godot 相关 topic,筛出 **star ≥ 1000 且最近 3 个月有 commit 推送**(可持续维护)的仓库,落盘为 JSONL 并装载进 SQLite,供后续数据分析。

## 采集范围

| 维度 | 值 |
|---|---|
| Topics | `godot-engine`、`godot4`、`godot`、`godot-addon`、`gdscript` |
| 硬筛选 | `stars >= 1000` |
| 活跃筛选 | `pushed >= 运行日往前 3 个月` |
| 去重 | 采集阶段**不去重**(每 topic 独立落盘);装载阶段按 `full_name` 去重,保留 topic 归属 |
| 元数据深度 | 基础字段(`gh search repos` 一次调用返回) |

## 依赖

- [`gh`](https://cli.github.com/) CLI(已登录:`gh auth status`)
- [`jq`](https://jqlang.github.io/jq/)
- `sqlite3`
- Python 3(仅标准库)

> `collect.sh` 的日期计算已跨平台(macOS `date -v` / Linux `date -d` 自动回退)。

## 快速开始

```bash
# 1. 采集(5 个 topic 依次跑,结果 -> data/raw/<topic>.jsonl)
./collect.sh

# 2. 装载(JSONL -> godot.db)
python3 load.py

# 3. 验收(断言 5 个 topic 都真的采集+装载成功;失败则非零退出)
./verify.sh
```

一行跑完整链路:

```bash
./collect.sh && python3 load.py && ./verify.sh
```

## 架构

```
阶段 A 采集(不去重)              阶段 B 装载(去重 + 可查询)
gh search repos  ──►  data/raw/<topic>.jsonl  ──►  load.py  ──►  godot.db (SQLite)
   (5 个 topic 依次跑)            每行一个 repo                     repos 表 + repo_topics 关联表
```

- **`collect.sh`** — 阶段 A。遍历 topic,每个一次 `gh search repos`,`jq` 转 JSONL 落盘。单个 topic 失败记入 `data/raw/errors.log` 并继续。
- **`load.py`** — 阶段 B。读所有 `data/raw/*.jsonl`,装入 SQLite。`repos` 表按 `full_name` 去重(`INSERT OR REPLACE`),`repo_topics` 关联表保留每个 repo 在每个 topic 内的 star 排名。
- **`verify.sh`** — 验收。三类断言:错误日志为空 / 每个 topic JSONL 有数据且字段+star 阈值合法 / SQLite 各 topic 都有记录。

原始 JSONL 永久保留,可随时重跑装载,不丢数据。

## 数据结构(SQLite `godot.db`)

### `repos`(主键 `full_name`,跨 topic 去重)

| 列 | 类型 | 说明 |
|---|---|---|
| `full_name` | TEXT PK | `owner/name` |
| `name` / `owner` | TEXT | |
| `url` / `homepage` | TEXT | repo 地址 / 主页 |
| `description` | TEXT | |
| `stars` / `forks` / `open_issues` | INTEGER | |
| `language` | TEXT | 主语言 |
| `license` | TEXT | SPDX key |
| `is_archived` / `is_fork` / `is_disabled` | INTEGER | 0/1 |
| `default_branch` / `size` | TEXT / INTEGER | size 单位 KB |
| `created_at` / `updated_at` / `pushed_at` | TEXT | ISO 时间 |
| `collected_at` | TEXT | 装载时间戳 |

### `repo_topics`(多对多,主键 `(full_name, topic)`)

| 列 | 类型 | 说明 |
|---|---|---|
| `full_name` | TEXT | 外键 → `repos.full_name` |
| `topic` | TEXT | 5 个 topic 之一 |
| `rank_in_topic` | INTEGER | 该 topic 内按 star 降序的名次(1 起) |

索引:`repos(stars)`、`repos(language)`、`repo_topics(topic)`。

## 分析示例

```bash
# Top 20(按 star)
sqlite3 -column -header godot.db \
  "SELECT full_name, stars, forks, language FROM repos ORDER BY stars DESC LIMIT 20;"

# 跨多个 topic 命中的 repo
sqlite3 -column -header godot.db \
  "SELECT full_name, COUNT(*) AS topic_hits FROM repo_topics
   GROUP BY full_name HAVING topic_hits > 1 ORDER BY topic_hits DESC;"

# 语言分布
sqlite3 -column -header godot.db \
  "SELECT COALESCE(language,'(none)') AS lang, COUNT(*) n FROM repos
   GROUP BY lang ORDER BY n DESC;"

# 某 topic 的 Top 10
sqlite3 -column -header godot.db \
  "SELECT r.full_name, r.stars, t.rank_in_topic FROM repo_topics t
   JOIN repos r USING(full_name) WHERE t.topic='gdscript'
   ORDER BY t.rank_in_topic LIMIT 10;"
```

## 测试

```bash
python3 -m pytest tests/ -v
```

## 项目结构

```
collect.sh                 # 阶段 A 采集脚本
load.py                    # 阶段 B 装载脚本
verify.sh                  # 验收脚本
tests/test_load.py         # load.py 单元测试
data/raw/                  # 采集产出(JSONL + errors.log,gitignore)
godot.db                   # SQLite 输出(gitignore)
docs/superpowers/specs/    # 设计文档
docs/superpowers/plans/    # 实现计划
```

## 重跑与限制

- **重跑安全**:JSONL 覆盖写;SQLite `INSERT OR REPLACE`。
- **API 配额**:GitHub 搜索 API 每查询最多 1000 条、限速约 30 次/分钟;5 个 topic 各 1 次调用,远低于限制。
- **数据时效**:star/活跃度随时间变化,建议定期手动重跑 `./collect.sh && python3 load.py && ./verify.sh`。
