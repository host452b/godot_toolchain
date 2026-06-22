import sqlite3
import json
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
