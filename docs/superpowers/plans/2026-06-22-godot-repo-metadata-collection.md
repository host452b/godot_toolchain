# Godot Repo 元数据采集 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用 `gh` CLI 采集 5 个 Godot topic 中 star≥1000 且最近 3 个月有 push 的 repo 基础元数据,落盘为按 topic 分离的 JSONL,再装载进 SQLite 供分析。

**Architecture:** 两阶段。阶段 A 用 bash 脚本 `collect.sh` 依次遍历 topic,每个 topic 一次 `gh search repos` 调用,`jq` 转 JSONL 写入 `data/raw/<topic>.jsonl`,失败记日志继续。阶段 B 用 Python `load.py` 读所有 JSONL,装入 SQLite `godot.db`(`repos` 表按 full_name 去重,`repo_topics` 关联表保留 topic 归属与排名)。

**Tech Stack:** bash, `gh` CLI (v2.83), `jq`, Python 3 标准库(`sqlite3`, `json`, `glob`, `datetime`)。

参考 spec: `docs/superpowers/specs/2026-06-22-godot-repo-metadata-collection-design.md`

---

## File Structure

- `collect.sh` — 阶段 A 采集脚本(bash)。唯一职责:调 gh 抓 5 个 topic → JSONL。
- `load.py` — 阶段 B 装载脚本(Python)。唯一职责:JSONL → SQLite。
- `verify.sh` — 验收脚本(bash)。唯一职责:断言 5 个 topic 都真的采集+装载成功。
- `data/raw/<topic>.jsonl` — 每个 topic 的原始结果(脚本产出,不手写)。
- `data/raw/errors.log` — 采集错误日志(脚本产出)。
- `godot.db` — SQLite 输出(脚本产出)。
- `tests/test_load.py` — `load.py` 的单元测试(pytest)。
- `.gitignore` — 忽略产出物(data/、godot.db)。

---

## Task 1: 项目骨架与 .gitignore

**Files:**
- Create: `.gitignore`
- Create: `data/raw/.gitkeep`

- [ ] **Step 1: 写 .gitignore**

```
# 采集产出物 —— 不入库
/data/raw/*.jsonl
/data/raw/errors.log
/godot.db

# Python
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 2: 建 data/raw 目录占位**

Run:
```bash
mkdir -p data/raw && touch data/raw/.gitkeep
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore data/raw/.gitkeep
git commit -m "chore: project skeleton and gitignore"
```

---

## Task 2: 采集脚本 collect.sh

**Files:**
- Create: `collect.sh`

- [ ] **Step 1: 写 collect.sh**

```bash
#!/usr/bin/env bash
# 阶段 A:遍历 Godot topic,采集 star>=1000 且最近 3 个月有 push 的 repo 基础元数据。
# 不去重:每个 topic 各自落盘 data/raw/<topic>.jsonl。
set -uo pipefail

TOPICS=(godot-engine godot4 godot godot-addon gdscript)
OUT_DIR="data/raw"
ERR_LOG="$OUT_DIR/errors.log"
CUTOFF=$(date -v-3m +%Y-%m-%d)   # macOS:今天往前推 3 个月
FIELDS="fullName,name,owner,description,url,homepage,stargazersCount,forksCount,openIssuesCount,language,license,isArchived,isFork,isDisabled,defaultBranch,size,createdAt,updatedAt,pushedAt"

mkdir -p "$OUT_DIR"
: > "$ERR_LOG"   # 清空错误日志

echo "活跃截止日(pushed >=): $CUTOFF"

for topic in "${TOPICS[@]}"; do
  out="$OUT_DIR/${topic}.jsonl"
  echo "==> 采集 topic: $topic"
  if gh search repos "pushed:>=$CUTOFF" \
       --topic "$topic" \
       --stars '>=1000' \
       --sort stars --order desc \
       --limit 1000 \
       --json "$FIELDS" \
     | jq -c '.[]' > "$out"; then
    count=$(wc -l < "$out" | tr -d ' ')
    echo "    OK: $count repos -> $out"
  else
    echo "$(date '+%Y-%m-%dT%H:%M:%S') FAILED topic=$topic" >> "$ERR_LOG"
    echo "    FAILED: 见 $ERR_LOG,继续下一个"
  fi
done

echo "采集完成。"
```

- [ ] **Step 2: 加可执行权限**

Run:
```bash
chmod +x collect.sh
```

- [ ] **Step 3: 校验语法**

Run: `bash -n collect.sh`
Expected: 无输出(语法正确),退出码 0。

- [ ] **Step 4: 实跑一个 topic 冒烟验证**(确认 gh/jq 链路通)

Run:
```bash
gh search repos "pushed:>=$(date -v-3m +%Y-%m-%d)" --topic gdscript --stars '>=1000' --sort stars --order desc --limit 5 --json fullName,url,stargazersCount | jq -c '.[]'
```
Expected: 输出若干行 JSON,每行含 `fullName`/`url`/`stargazersCount`。若报 `jq: command not found`,先 `brew install jq`。

- [ ] **Step 5: Commit**

```bash
git add collect.sh
git commit -m "feat: add collect.sh to fetch godot repo metadata via gh"
```

---

## Task 3: 装载脚本 load.py — 建表与 schema

**Files:**
- Create: `load.py`
- Test: `tests/test_load.py`

- [ ] **Step 1: 写失败测试(建表)**

```python
# tests/test_load.py
import sqlite3
import load


def test_init_db_creates_tables(tmp_path):
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    load.init_db(conn)
    names = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    assert "repos" in names
    assert "repo_topics" in names
    conn.close()


def test_repos_has_full_name_pk(tmp_path):
    db = tmp_path / "t.db"
    conn = sqlite3.connect(db)
    load.init_db(conn)
    cols = {row[1]: row for row in conn.execute("PRAGMA table_info(repos)")}
    assert cols["full_name"][5] == 1  # pk flag
    conn.close()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_load.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'load'` 或 `AttributeError: init_db`。

- [ ] **Step 3: 写 load.py 的 init_db**

```python
# load.py
"""阶段 B:把 data/raw/*.jsonl 装载进 SQLite godot.db。"""
import sqlite3


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS repos (
            full_name      TEXT PRIMARY KEY,
            name           TEXT,
            owner          TEXT,
            url            TEXT,
            homepage       TEXT,
            description    TEXT,
            stars          INTEGER,
            forks          INTEGER,
            open_issues    INTEGER,
            language       TEXT,
            license        TEXT,
            is_archived    INTEGER,
            is_fork        INTEGER,
            is_disabled    INTEGER,
            default_branch TEXT,
            size           INTEGER,
            created_at     TEXT,
            updated_at     TEXT,
            pushed_at      TEXT,
            collected_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS repo_topics (
            full_name     TEXT,
            topic         TEXT,
            rank_in_topic INTEGER,
            PRIMARY KEY (full_name, topic)
        );

        CREATE INDEX IF NOT EXISTS idx_repos_stars    ON repos(stars);
        CREATE INDEX IF NOT EXISTS idx_repos_language ON repos(language);
        CREATE INDEX IF NOT EXISTS idx_rt_topic       ON repo_topics(topic);
        """
    )
    conn.commit()
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_load.py -v`
Expected: 2 passed。

- [ ] **Step 5: Commit**

```bash
git add load.py tests/test_load.py
git commit -m "feat: add load.py init_db with repos and repo_topics schema"
```

---

## Task 4: load.py — 解析单条 gh JSON 记录

`gh` 返回的字段是嵌套/驼峰的(如 `owner.login`、`license.key`、`stargazersCount`),需映射到扁平列。

**Files:**
- Modify: `load.py`
- Test: `tests/test_load.py`

- [ ] **Step 1: 写失败测试(字段映射)**

```python
# 追加到 tests/test_load.py
def test_parse_record_maps_fields():
    raw = {
        "fullName": "godotengine/godot",
        "name": "godot",
        "owner": {"login": "godotengine"},
        "url": "https://github.com/godotengine/godot",
        "homepage": "https://godotengine.org",
        "description": "Game engine",
        "stargazersCount": 90000,
        "forksCount": 20000,
        "openIssuesCount": 9000,
        "language": "C++",
        "license": {"key": "mit"},
        "isArchived": False,
        "isFork": False,
        "isDisabled": False,
        "defaultBranch": "master",
        "size": 1234,
        "createdAt": "2014-01-01T00:00:00Z",
        "updatedAt": "2026-06-01T00:00:00Z",
        "pushedAt": "2026-06-20T00:00:00Z",
    }
    row = load.parse_record(raw)
    assert row["full_name"] == "godotengine/godot"
    assert row["owner"] == "godotengine"
    assert row["license"] == "mit"
    assert row["stars"] == 90000
    assert row["forks"] == 20000
    assert row["open_issues"] == 9000
    assert row["is_archived"] == 0


def test_parse_record_handles_missing_optionals():
    raw = {
        "fullName": "a/b",
        "name": "b",
        "owner": {"login": "a"},
        "url": "https://github.com/a/b",
        "stargazersCount": 1000,
        "forksCount": 1,
        "openIssuesCount": 0,
        "isArchived": False,
        "isFork": False,
        "isDisabled": False,
        "size": 1,
    }
    row = load.parse_record(raw)
    assert row["homepage"] is None
    assert row["description"] is None
    assert row["language"] is None
    assert row["license"] is None
    assert row["default_branch"] is None
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_load.py::test_parse_record_maps_fields -v`
Expected: FAIL — `AttributeError: module 'load' has no attribute 'parse_record'`。

- [ ] **Step 3: 实现 parse_record**

```python
# 追加到 load.py 顶部 import
import json
import glob
import os
from datetime import datetime, timezone


# 追加函数
def _login(owner):
    if isinstance(owner, dict):
        return owner.get("login")
    return owner


def _license_key(lic):
    if isinstance(lic, dict):
        return lic.get("key")
    return lic


def parse_record(raw: dict) -> dict:
    """把 gh search repos 的一条 JSON 映射成 repos 表的扁平行。"""
    return {
        "full_name": raw.get("fullName"),
        "name": raw.get("name"),
        "owner": _login(raw.get("owner")),
        "url": raw.get("url"),
        "homepage": raw.get("homepage") or None,
        "description": raw.get("description") or None,
        "stars": raw.get("stargazersCount"),
        "forks": raw.get("forksCount"),
        "open_issues": raw.get("openIssuesCount"),
        "language": raw.get("language") or None,
        "license": _license_key(raw.get("license")),
        "is_archived": 1 if raw.get("isArchived") else 0,
        "is_fork": 1 if raw.get("isFork") else 0,
        "is_disabled": 1 if raw.get("isDisabled") else 0,
        "default_branch": raw.get("defaultBranch") or None,
        "size": raw.get("size"),
        "created_at": raw.get("createdAt") or None,
        "updated_at": raw.get("updatedAt") or None,
        "pushed_at": raw.get("pushedAt") or None,
    }
```

注意:`gh` 对空字符串 homepage/description 返回 `""`,`"" or None` → `None`,符合测试。

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_load.py -v`
Expected: 4 passed。

- [ ] **Step 5: Commit**

```bash
git add load.py tests/test_load.py
git commit -m "feat: add parse_record field mapping in load.py"
```

---

## Task 5: load.py — upsert 一个 topic 的记录

**Files:**
- Modify: `load.py`
- Test: `tests/test_load.py`

- [ ] **Step 1: 写失败测试(装载 + 去重 + 排名)**

```python
# 追加到 tests/test_load.py
def _sample(full_name, stars):
    return {
        "fullName": full_name,
        "name": full_name.split("/")[1],
        "owner": {"login": full_name.split("/")[0]},
        "url": f"https://github.com/{full_name}",
        "stargazersCount": stars,
        "forksCount": 0,
        "openIssuesCount": 0,
        "isArchived": False,
        "isFork": False,
        "isDisabled": False,
        "size": 1,
    }


def test_load_topic_inserts_repos_and_topics(tmp_path):
    conn = sqlite3.connect(tmp_path / "t.db")
    load.init_db(conn)
    records = [_sample("a/one", 5000), _sample("a/two", 3000)]
    load.load_topic(conn, "godot", records, collected_at="2026-06-22T00:00:00Z")

    repos = conn.execute("SELECT full_name, stars FROM repos ORDER BY stars DESC").fetchall()
    assert repos == [("a/one", 5000), ("a/two", 3000)]

    rt = conn.execute(
        "SELECT full_name, topic, rank_in_topic FROM repo_topics ORDER BY rank_in_topic"
    ).fetchall()
    assert rt == [("a/one", "godot", 1), ("a/two", "godot", 2)]
    conn.close()


def test_load_topic_dedupes_repo_across_topics(tmp_path):
    conn = sqlite3.connect(tmp_path / "t.db")
    load.init_db(conn)
    load.load_topic(conn, "godot", [_sample("a/one", 5000)], collected_at="t")
    load.load_topic(conn, "godot4", [_sample("a/one", 5000)], collected_at="t")

    assert conn.execute("SELECT COUNT(*) FROM repos").fetchone()[0] == 1
    topics = {r[0] for r in conn.execute(
        "SELECT topic FROM repo_topics WHERE full_name='a/one'"
    )}
    assert topics == {"godot", "godot4"}
    conn.close()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_load.py::test_load_topic_inserts_repos_and_topics -v`
Expected: FAIL — `AttributeError: ... 'load_topic'`。

- [ ] **Step 3: 实现 load_topic**

```python
# 追加到 load.py
_REPO_COLS = [
    "full_name", "name", "owner", "url", "homepage", "description",
    "stars", "forks", "open_issues", "language", "license",
    "is_archived", "is_fork", "is_disabled", "default_branch", "size",
    "created_at", "updated_at", "pushed_at", "collected_at",
]


def load_topic(conn, topic, records, collected_at):
    """装载一个 topic 的记录列表(已按 star 降序)。repos 去重,repo_topics 记排名。"""
    placeholders = ",".join("?" for _ in _REPO_COLS)
    repo_sql = f"INSERT OR REPLACE INTO repos ({','.join(_REPO_COLS)}) VALUES ({placeholders})"
    rt_sql = (
        "INSERT OR REPLACE INTO repo_topics (full_name, topic, rank_in_topic) "
        "VALUES (?, ?, ?)"
    )
    for rank, raw in enumerate(records, start=1):
        row = parse_record(raw)
        row["collected_at"] = collected_at
        conn.execute(repo_sql, [row[c] for c in _REPO_COLS])
        conn.execute(rt_sql, [row["full_name"], topic, rank])
    conn.commit()
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_load.py -v`
Expected: 6 passed。

- [ ] **Step 5: Commit**

```bash
git add load.py tests/test_load.py
git commit -m "feat: add load_topic with dedup and per-topic ranking"
```

---

## Task 6: load.py — main 入口(读 JSONL 文件)

**Files:**
- Modify: `load.py`
- Test: `tests/test_load.py`

- [ ] **Step 1: 写失败测试(读文件 → 装载)**

```python
# 追加到 tests/test_load.py
def test_run_reads_jsonl_files(tmp_path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    (raw_dir / "godot.jsonl").write_text(
        json.dumps(_sample("a/one", 5000)) + "\n" +
        json.dumps(_sample("a/two", 3000)) + "\n"
    )
    (raw_dir / "godot4.jsonl").write_text(
        json.dumps(_sample("a/one", 5000)) + "\n"
    )
    db = tmp_path / "out.db"
    load.run(str(raw_dir), str(db), collected_at="2026-06-22T00:00:00Z")

    conn = sqlite3.connect(db)
    assert conn.execute("SELECT COUNT(*) FROM repos").fetchone()[0] == 2
    assert conn.execute("SELECT COUNT(*) FROM repo_topics").fetchone()[0] == 3
    conn.close()


def test_run_skips_blank_lines(tmp_path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    (raw_dir / "godot.jsonl").write_text(
        json.dumps(_sample("a/one", 5000)) + "\n\n"
    )
    db = tmp_path / "out.db"
    load.run(str(raw_dir), str(db), collected_at="t")
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT COUNT(*) FROM repos").fetchone()[0] == 1
    conn.close()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_load.py::test_run_reads_jsonl_files -v`
Expected: FAIL — `AttributeError: ... 'run'`。

- [ ] **Step 3: 实现 run + __main__**

```python
# 追加到 load.py
def run(raw_dir, db_path, collected_at):
    """读 raw_dir 下所有 <topic>.jsonl,装载进 db_path。文件名(去扩展名)即 topic。"""
    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)
        for path in sorted(glob.glob(os.path.join(raw_dir, "*.jsonl"))):
            topic = os.path.splitext(os.path.basename(path))[0]
            records = []
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    records.append(json.loads(line))
            load_topic(conn, topic, records, collected_at)
            print(f"loaded {len(records):>5} repos from topic '{topic}'")
    finally:
        conn.close()


if __name__ == "__main__":
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run("data/raw", "godot.db", collected_at=now)
    print("装载完成 -> godot.db")
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_load.py -v`
Expected: 8 passed。

- [ ] **Step 5: Commit**

```bash
git add load.py tests/test_load.py
git commit -m "feat: add run entrypoint to load all topic JSONL into godot.db"
```

---

## Task 7: 端到端实跑与验证

**Files:** 无新增(运行已有脚本)

- [ ] **Step 1: 跑采集**

Run: `./collect.sh`
Expected: 打印每个 topic 的 OK + repo 数;`data/raw/` 下出现 5 个 `.jsonl`;`errors.log` 为空。

- [ ] **Step 2: 抽查一个 JSONL**

Run: `head -1 data/raw/godot.jsonl | jq '{fullName, url, stargazersCount, pushedAt}'`
Expected: 一条 JSON,`stargazersCount >= 1000`,`url` 是合法 github 地址。

- [ ] **Step 3: 跑装载**

Run: `python load.py`
Expected: 打印每个 topic 的 loaded 行数 + "装载完成 -> godot.db"。

- [ ] **Step 4: 验证 SQLite 数据**

Run:
```bash
sqlite3 godot.db "SELECT COUNT(*) AS repos FROM repos; SELECT topic, COUNT(*) FROM repo_topics GROUP BY topic; SELECT full_name, stars FROM repos ORDER BY stars DESC LIMIT 5;"
```
Expected: repos 总数 > 0;每个 topic 有计数;top5 按 star 降序合理(godotengine/godot 居前)。

- [ ] **Step 5: 验证去重生效**

Run:
```bash
sqlite3 godot.db "SELECT full_name, COUNT(*) c FROM repo_topics GROUP BY full_name HAVING c > 1 LIMIT 5;"
```
Expected: 出现跨多个 topic 的 repo(说明 repos 去重、repo_topics 保留多归属)。

- [ ] **Step 6: 最终 commit**

```bash
git add -A
git commit -m "chore: end-to-end verified godot repo metadata pipeline"
```

---

## Task 8: 验收脚本 verify.sh — 保证 5 个 topic 都真的执行

**目的:** 执行过程管理。独立校验"5 个 topic 是否都真的跑了搜索、是否真的 dump 了期望数据、SQLite 是否齐全"。任一项不达标即非零退出,便于人工/CI 卡口。

**Files:**
- Create: `verify.sh`

- [ ] **Step 1: 写 verify.sh**

```bash
#!/usr/bin/env bash
# 验收:确认 5 个 topic 都真的采集成功且数据完整。任一检查失败 -> 退出码 1。
set -uo pipefail

TOPICS=(godot-engine godot4 godot godot-addon gdscript)
OUT_DIR="data/raw"
ERR_LOG="$OUT_DIR/errors.log"
DB="godot.db"
fail=0

red()  { printf "  \033[31m✗ %s\033[0m\n" "$1"; fail=1; }
green(){ printf "  \033[32m✓ %s\033[0m\n" "$1"; }

echo "== 检查 1:错误日志 =="
if [[ -s "$ERR_LOG" ]]; then
  red "errors.log 非空,采集中有 topic 失败:"; cat "$ERR_LOG"
else
  green "errors.log 为空"
fi

echo "== 检查 2:每个 topic 的 JSONL 存在且有数据 =="
for topic in "${TOPICS[@]}"; do
  f="$OUT_DIR/${topic}.jsonl"
  if [[ ! -f "$f" ]]; then
    red "$topic: JSONL 缺失 ($f)"
    continue
  fi
  n=$(wc -l < "$f" | tr -d ' ')
  if [[ "$n" -lt 1 ]]; then
    red "$topic: JSONL 为空(0 行)"
    continue
  fi
  # 校验首行是合法 JSON 且含关键字段且 star>=1000
  if head -1 "$f" | jq -e '.fullName and .url and (.stargazersCount >= 1000)' >/dev/null 2>&1; then
    green "$topic: $n repos,字段与 star 阈值校验通过"
  else
    red "$topic: 首行 JSON 缺关键字段或 star<1000"
  fi
done

echo "== 检查 3:SQLite 表存在且 5 个 topic 都有数据 =="
if [[ ! -f "$DB" ]]; then
  red "$DB 不存在(未执行 load.py?)"
else
  for topic in "${TOPICS[@]}"; do
    c=$(sqlite3 "$DB" "SELECT COUNT(*) FROM repo_topics WHERE topic='$topic';" 2>/dev/null)
    if [[ "${c:-0}" -ge 1 ]]; then
      green "$topic: SQLite 中 $c 条 repo_topics"
    else
      red "$topic: SQLite 中无记录"
    fi
  done
  total=$(sqlite3 "$DB" "SELECT COUNT(*) FROM repos;" 2>/dev/null)
  echo "  repos 去重后总数:${total:-0}"
fi

echo
if [[ "$fail" -eq 0 ]]; then
  printf "\033[32m全部检查通过 ✅\033[0m\n"; exit 0
else
  printf "\033[31m有检查未通过 ❌\033[0m\n"; exit 1
fi
```

- [ ] **Step 2: 加可执行权限 + 语法校验**

Run:
```bash
chmod +x verify.sh && bash -n verify.sh && echo OK
```
Expected: 打印 `OK`。

- [ ] **Step 3: 在采集+装载之后实跑验收**

Run: `./verify.sh; echo "exit=$?"`
Expected: 每个 topic 三类检查都打 ✓;末尾 `全部检查通过 ✅`,`exit=0`。
若某 topic 报 ✗,回到 Task 7 Step 1 重跑 `./collect.sh`(失败的 topic 会重新覆盖写),再 `python load.py`,再 verify。

- [ ] **Step 4: Commit**

```bash
git add verify.sh
git commit -m "feat: add verify.sh to assert all 5 topics collected and loaded"
```

---

## Self-Review 记录

- **Spec coverage:** 5 topic 遍历(T2)✅;star≥1000+最近3月push 过滤(T2 查询限定符)✅;不去重落盘(T2 每 topic 独立 JSONL)✅;基础字段(T2 FIELDS / T4 映射)✅;repo 地址 url(T4)✅;SQLite repos+repo_topics(T3/T5)✅;装载去重+排名(T5)✅;错误日志+重跑安全(T2 errors.log / T5 INSERT OR REPLACE)✅;产出文件(T1/T7)✅。
- **Placeholder scan:** 无 TBD/TODO,所有步骤含完整代码与命令。
- **Type consistency:** `init_db`/`parse_record`/`load_topic`/`run` 跨任务签名一致;`_REPO_COLS` 与 schema 列、parse_record 键三处一致;`load_topic(conn, topic, records, collected_at)` 调用处(T6 run)与定义(T5)一致。
- **执行过程管理:** Task 8 的 `verify.sh` 对 5 个 topic 逐一做三类断言(无错误日志 / JSONL 有数据且字段+star阈值合法 / SQLite 各 topic 有记录),不达标即非零退出 —— 保证"5 个 topic 都真的执行了搜索并 dump 了期望信息"。
