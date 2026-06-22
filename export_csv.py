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
        "KoBeWi/Metroidvania-System", "bitbrain/pandora", "Kelpekk/Juicee",
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

# 独立游戏开发指数(0-100):独立开发者对该工具的"刚需/依赖程度"主观评估。
# 高分=几乎人人要用的核心(引擎/文档/对话/像素画/相机/上架);
# 低分=企业级/研究向/小众工具,独立开发很少直接依赖。
INDIE_INDEX = {
    "godotengine/godot": 100, "godotengine/godot-docs": 95, "godotengine/awesome-godot": 85,
    "Redot-Engine/redot-engine": 30,
    "Donchitos/Claude-Code-Game-Studios": 45, "htdt/godogen": 40,
    "KsanaDock/Microverse": 20, "Coding-Solo/godot-mcp": 50, "nobodywho-ooo/nobodywho": 45,
    "bitbrain/beehave": 70, "limbonaut/limboai": 72, "edbeeching/godot_rl_agents": 35,
    "dialogic-godot/dialogic": 88, "nathanhoad/godot_dialogue_manager": 85,
    "heroiclabs/nakama": 50, "zfoo-project/zfoo": 25, "foxssake/netfox": 55,
    "Orama-Interactive/Pixelorama": 80, "RodZill4/material-maker": 70,
    "gdquest-demos/godot-shaders": 78, "MewPurPur/GodSVG": 45,
    "elringus/sprite-dicing": 50, "gdquest-demos/godot-visual-effects": 65,
    "TokisanGames/Terrain3D": 65, "Zylann/godot_heightmap_plugin": 55,
    "gdquest-demos/godot-4-procedural-generation": 60, "SirRamEsq/SmartShape2D": 62,
    "gaea-godot/gaea": 58, "TheDuckCow/godot-road-generator": 35,
    "godot-rust/gdext": 45, "focus-creative-games/luban": 40, "MattParkerDev/SharpIDE": 35,
    "GodotSteam/GodotSteam": 75, "bitwes/Gut": 68, "CraterCrash/godot-orchestrator": 60,
    "godot-gdunit-labs/gdUnit4": 65, "abarichello/godot-ci": 60,
    "DmitriySalnikov/godot_debug_draw_3d": 55, "Maran23/script-ide": 58,
    "liangxiegame/QFramework": 50, "ramokz/phantom-camera": 80,
    "KoBeWi/Metroidvania-System": 55, "bitbrain/pandora": 65, "Kelpekk/Juicee": 60,
    "0xFA11/MultiplayerNetworkingResources": 45, "Revolutionary-Games/Thrive": 25,
    "gdquest-demos/godot-open-rpg": 70, "GDQuest/learn-gdscript": 80,
    "nezvers/Godot-GameTemplate": 65, "Maaack/Godot-Game-Template": 70,
    "drwhut/tabletop-club": 25, "gdquest-demos/godot-2d-space-game": 55,
}

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
df["indie_game_index"] = df["full_name"].map(INDIE_INDEX)

missing = df[df["category"].isna()]["full_name"].tolist()
if missing:
    raise SystemExit(f"未分类的仓库,请补进 CATEGORIES: {missing}")
missing_idx = df[df["indie_game_index"].isna()]["full_name"].tolist()
if missing_idx:
    raise SystemExit(f"缺独立游戏开发指数,请补进 INDIE_INDEX: {missing_idx}")
df["indie_game_index"] = df["indie_game_index"].astype(int)

df.to_csv("godot_repos.csv", index=False, encoding="utf-8-sig")
print(f"wrote godot_repos.csv ({len(df)} rows, {df['category'].nunique()} 个类别)")
