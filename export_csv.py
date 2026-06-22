"""从 godot.db 导出 godot_repos.csv(utf-8-sig),供 notebook 读取渲染。

CSV 自带计算列 stars_per_month(月均新增 star),notebook 只负责读取与着色。
"""
import sqlite3
import pandas as pd

# 领域分类(与 README 生态导览一致;含引擎本体)。键=领域顺序,值=该领域仓库列表。
CATEGORIES = {
    "引擎与发行版": [
        "godotengine/godot", "Redot-Engine/redot-engine",
    ],
    "AI 辅助开发与 LLM 集成": [
        "Donchitos/Claude-Code-Game-Studios", "htdt/godogen",
        "KsanaDock/Microverse", "Coding-Solo/godot-mcp", "nobodywho-ooo/nobodywho",
    ],
    "游戏 AI 与行为": [
        "bitbrain/beehave", "limbonaut/limboai", "edbeeching/godot_rl_agents",
    ],
    "对话与叙事": [
        "dialogic-godot/dialogic", "nathanhoad/godot_dialogue_manager",
    ],
    "网络与多人": [
        "heroiclabs/nakama", "zfoo-project/zfoo", "foxssake/netfox",
    ],
    "美术与创作工具": [
        "Orama-Interactive/Pixelorama", "RodZill4/material-maker",
        "gdquest-demos/godot-shaders", "MewPurPur/GodSVG",
        "elringus/sprite-dicing", "gdquest-demos/godot-visual-effects",
    ],
    "地形与世界生成": [
        "TokisanGames/Terrain3D", "Zylann/godot_heightmap_plugin",
        "gdquest-demos/godot-4-procedural-generation", "SirRamEsq/SmartShape2D",
        "gaea-godot/gaea", "TheDuckCow/godot-road-generator",
    ],
    "编辑器、开发工具与语言绑定": [
        "godot-rust/gdext", "focus-creative-games/luban", "MattParkerDev/SharpIDE",
        "GodotSteam/GodotSteam", "bitwes/Gut", "CraterCrash/godot-orchestrator",
        "godot-gdunit-labs/gdUnit4", "abarichello/godot-ci",
        "DmitriySalnikov/godot_debug_draw_3d", "Maran23/script-ide",
    ],
    "框架与游戏系统": [
        "liangxiegame/QFramework", "ramokz/phantom-camera",
        "KoBeWi/Metroidvania-System", "bitbrain/pandora",
    ],
    "学习资源、模板与示例项目": [
        "godotengine/awesome-godot", "0xFA11/MultiplayerNetworkingResources",
        "godotengine/godot-docs", "Revolutionary-Games/Thrive",
        "gdquest-demos/godot-open-rpg", "GDQuest/learn-gdscript",
        "nezvers/Godot-GameTemplate", "Maaack/Godot-Game-Template",
        "drwhut/tabletop-club", "gdquest-demos/godot-2d-space-game",
    ],
}
_REPO_TO_CAT = {repo: cat for cat, repos in CATEGORIES.items() for repo in repos}

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
df["category"] = df["full_name"].map(_REPO_TO_CAT)

missing = df[df["category"].isna()]["full_name"].tolist()
if missing:
    raise SystemExit(f"未分类的仓库,请补进 CATEGORIES: {missing}")

df.to_csv("godot_repos.csv", index=False, encoding="utf-8-sig")
print(f"wrote godot_repos.csv ({len(df)} rows, {df['category'].nunique()} 个类别)")
