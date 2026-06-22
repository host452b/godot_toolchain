"""从 godot.db 导出 godot_repos.csv(utf-8-sig),供 notebook 读取渲染。

CSV 自带计算列 stars_per_month(月均新增 star),notebook 只负责读取与着色。
"""
import sqlite3
import pandas as pd

conn = sqlite3.connect("godot.db")
df = pd.read_sql_query(
    "SELECT full_name, url, language, stars, forks, open_issues, "
    "created_at, updated_at FROM repos",
    conn,
)
conn.close()

created = pd.to_datetime(df["created_at"], utc=True)
updated = pd.to_datetime(df["updated_at"], utc=True)
active_months = ((updated - created).dt.days / 30.44).clip(lower=1.0)
df["stars_per_month"] = (df["stars"] / active_months).round(1)

df = (df.drop(columns=["created_at", "updated_at"])
        .sort_values("stars", ascending=False)
        .reset_index(drop=True))
df["language"] = df["language"].fillna("-")

df.to_csv("godot_repos.csv", index=False, encoding="utf-8-sig")
print(f"wrote godot_repos.csv ({len(df)} rows)")
