# godot.db — 数据字典 / 内容说明

`godot.db` 是本仓库采集管线的 SQLite 产物,由 `load.py` 读取 `data/raw/*.jsonl` 装载生成。本文件描述其结构与内容,**随数据重跑可能变化,统计口径以生成时为准**。

- 生成方式:`CUTOFF=2026-06-22 ./collect.sh && python3 load.py`(基于上次节点 `2026-06-22` 增量采集至 `2026-11-26`,产出 `data/raw/*.jsonl` 再装载)
- 数据来源:
  - **自动增量采集 60 个**:GitHub 搜索 API,5 个 topic(`godot-engine`、`godot4`、`godot`、`godot-addon`、`gdscript`),筛选 `stars >= 1000` 且 `pushed_at >= 2026-06-22`(另将上游更名的 `godotengine/awesome-godot` 对齐为 `Calinou/awesome-godot`)
  - **历史保留 5 个**:来源标记为 `retained`(见 `data/raw/retained.jsonl`),保留上一批(`2026-06-22`)自动采集仓库中近期无推送但仍在生态中的仓库,并刷新最新 star 数据
  - **手动补充 13 个**:来源标记为 `manual`(见 `data/raw/manual.jsonl`),同步刷新至 `2026-11-26` 最新 star 数据

## 概览

| 指标 | 值 |
|---|---|
| `repos` 行数(去重后唯一仓库) | 78(自动 60 + 历史保留 5 + 手动 13) |
| `repo_topics` 行数(仓库 × topic 命中) | 133 |
| star 范围 | 9 ~ 120803(手动补充含低 star 项) |
| `pushed_at` 范围 | 2025-09-05 ~ 2026-11-25(手动/历史保留含较旧推送) |

## 表:`repos`

每行一个**去重后**的仓库,主键 `full_name`。跨多个 topic 命中的仓库在此只存一行。

| 列 | 类型 | 含义 | 备注 |
|---|---|---|---|
| `full_name` | TEXT **PK** | `owner/name`,仓库唯一标识 | |
| `name` | TEXT | 仓库名 | |
| `owner` | TEXT | owner 登录名 | |
| `url` | TEXT | 仓库地址(https) | |
| `homepage` | TEXT | 项目主页 URL | 可为 NULL(本次 32/78 为空) |
| `description` | TEXT | 仓库描述 | 本次无 NULL |
| `stars` | INTEGER | stargazers 数 | 已建索引 `idx_repos_stars` |
| `forks` | INTEGER | fork 数 | |
| `open_issues` | INTEGER | open issue 数 | |
| `language` | TEXT | 主语言 | 可为 NULL(本次 2/78 为空) |
| `license` | TEXT | 许可证 SPDX key | |
| `is_archived` | INTEGER | 是否已归档 | 0/1 |
| `is_fork` | INTEGER | 是否为 fork | 0/1 |
| `is_disabled` | INTEGER | 是否已停用 | 0/1 |
| `default_branch` | TEXT | 默认分支 | |
| `size` | INTEGER | 仓库大小 | 单位 KB |
| `created_at` | TEXT | 创建时间 | ISO 8601 |
| `updated_at` | TEXT | 最后更新时间 | ISO 8601 |
| `pushed_at` | TEXT | 最后推送时间 | ISO 8601,活跃度依据 |
| `collected_at` | TEXT | 本次采集装载时间戳 | ISO 8601 |

## 表:`repo_topics`

仓库与 topic 的多对多关联,主键 `(full_name, topic)`。保留每个仓库在各 topic 内按 star 的名次。

| 列 | 类型 | 含义 |
|---|---|---|
| `full_name` | TEXT | 外键 → `repos.full_name` |
| `topic` | TEXT | 5 个 topic 之一,或 `manual`(手动补充来源) |
| `rank_in_topic` | INTEGER | 该 topic 内按 star 降序的名次(1 起),已建索引 `idx_rt_topic` |

### 各 topic 命中数

| topic | 命中仓库数 |
|---|---|
| godot | 55 |
| godot-engine | 27 |
| godot4 | 16 |
| manual | 13 |
| gdscript | 12 |
| godot-addon | 5 |
| retained | 5 |
| **合计** | **133** |

> `manual` 与 `retained` 为仓库维护来源标记(非 GitHub topic)。

### 跨 topic 命中分布

| 命中 topic 数 | 仓库数 |
|---|---|
| 1 个 topic | 41 |
| 2 个 topic | 22 |
| 3 个 topic | 12 |
| 4 个 topic | 3 |

> 78 个仓库共产生 133 条命中(41×1 + 22×2 + 12×3 + 3×4 = 133),无仓库同时命中全部 5 个 topic。

## 索引

| 索引 | 列 | 用途 |
|---|---|---|
| `idx_repos_stars` | `repos(stars)` | 按 star 排序 / 范围筛选 |
| `idx_repos_language` | `repos(language)` | 按语言聚合 |
| `idx_rt_topic` | `repo_topics(topic)` | 按 topic 过滤 |

## 常用查询

```sql
-- Top 20(按 star)
SELECT full_name, stars, language FROM repos ORDER BY stars DESC LIMIT 20;

-- 某 topic 的前 10
SELECT r.full_name, r.stars, t.rank_in_topic
FROM repo_topics t JOIN repos r USING(full_name)
WHERE t.topic='gdscript' ORDER BY t.rank_in_topic LIMIT 10;

-- 跨多个 topic 命中的仓库
SELECT full_name, COUNT(*) AS topic_hits FROM repo_topics
GROUP BY full_name HAVING topic_hits > 1 ORDER BY topic_hits DESC;

-- 语言分布
SELECT COALESCE(language,'(none)') AS lang, COUNT(*) n
FROM repos GROUP BY lang ORDER BY n DESC;
```
