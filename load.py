"""阶段 B:把 data/raw/*.jsonl 装载进 SQLite godot.db。"""
import sqlite3
import json
import glob
import os
from datetime import datetime, timezone


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
