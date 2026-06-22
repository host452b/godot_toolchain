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

## 生态导览(按领域分类)

下表来自本仓库 `godot.db`,覆盖 `godot-engine`、`godot4`、`godot`、`godot-addon`、`gdscript` 五个 topic 中 **star ≥ 1000 且最近 3 个月有推送** 的仓库,跨 topic 去重后共 51 个。这里按"插件 / 工具链的实际用途"而非原始 topic 重新归类,方便按领域找工具;每个领域内按 star 降序。引擎本体 `godotengine/godot` 不是插件 / 工具,已从导览中略去,故下列 **50 个**。

### 发行版

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [Redot-Engine/redot-engine](https://github.com/Redot-Engine/redot-engine) | 5880 | C++ | Godot 的社区分叉发行版 Redot |

### AI 辅助开发与 LLM 集成

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | 22010 | Shell | 把 Claude Code 变成完整游戏工作室:多 AI agent + 工作流技能协同 |
| [htdt/godogen](https://github.com/htdt/godogen) | 3583 | Python | 用 Claude Code / Codex 为 Godot、Bevy 做自主游戏开发 |
| [KsanaDock/Microverse](https://github.com/KsanaDock/Microverse) | 2375 | GDScript | 基于 Godot 4 的多智能体 AI 社会模拟沙盒 |
| [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp) | 4319 | JavaScript | 让 AI 通过 MCP 协议操控 Godot 编辑器、运行项目、抓调试输出 |
| [nobodywho-ooo/nobodywho](https://github.com/nobodywho-ooo/nobodywho) | 1010 | Rust | 在本地设备上高效运行 LLM 的推理引擎,可接入游戏 |

### 游戏 AI 与行为

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [bitbrain/beehave](https://github.com/bitbrain/beehave) | 3141 | GDScript | 纯 GDScript 行为树 AI,带可视化调试器 |
| [limbonaut/limboai](https://github.com/limbonaut/limboai) | 2817 | C++ | 行为树 + 状态机的 C++ 扩展,带可视化编辑器 |
| [edbeeching/godot_rl_agents](https://github.com/edbeeching/godot_rl_agents) | 1508 | Python | 用强化学习训练 NPC / agent 复杂行为的开源框架 |

### 对话与叙事

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [dialogic-godot/dialogic](https://github.com/dialogic-godot/dialogic) | 5726 | GDScript | 对话、视觉小说、角色管理一体化插件 |
| [nathanhoad/godot_dialogue_manager](https://github.com/nathanhoad/godot_dialogue_manager) | 3654 | GDScript | 面向非线性剧情的强大对话系统 |

### 网络与多人

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [heroiclabs/nakama](https://github.com/heroiclabs/nakama) | 12778 | Go | 可扩展的开源游戏后端:多人、匹配、排行榜、聊天、社交 |
| [zfoo-project/zfoo](https://github.com/zfoo-project/zfoo) | 2003 | Java | 极速企业级服务器框架,适用于 RPC / 游戏服 / Web 服 |
| [foxssake/netfox](https://github.com/foxssake/netfox) | 1011 | GDScript | 构建 Godot 多人游戏的网络同步插件集 |

### 美术与创作工具

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [Orama-Interactive/Pixelorama](https://github.com/Orama-Interactive/Pixelorama) | 9771 | GDScript | 跨平台开源像素画 / 精灵 / 动画创作工具 |
| [RodZill4/material-maker](https://github.com/RodZill4/material-maker) | 5554 | GDScript | 程序化材质制作与 3D 模型贴图绘制工具 |
| [gdquest-demos/godot-shaders](https://github.com/gdquest-demos/godot-shaders) | 4008 | GDShader | 大量免费开源的 2D/3D 着色器库,含可玩示例 |
| [MewPurPur/GodSVG](https://github.com/MewPurPur/GodSVG) | 2537 | GDScript | 跨平台的结构化 SVG 矢量图编辑器 |
| [elringus/sprite-dicing](https://github.com/elringus/sprite-dicing) | 1502 | Rust | 跨引擎的精灵无损压缩工具(复用相同区域) |
| [gdquest-demos/godot-visual-effects](https://github.com/gdquest-demos/godot-visual-effects) | 1262 | GDScript | 用 Godot 制作的开源视觉特效合集 |

### 地形与世界生成

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [TokisanGames/Terrain3D](https://github.com/TokisanGames/Terrain3D) | 3988 | C++ | Godot 4 的高性能可编辑地形系统 |
| [Zylann/godot_heightmap_plugin](https://github.com/Zylann/godot_heightmap_plugin) | 2209 | GDScript | 基于高度图的地形插件(纯 GDScript) |
| [gdquest-demos/godot-4-procedural-generation](https://github.com/gdquest-demos/godot-4-procedural-generation) | 1862 | GDScript | 程序化生成算法与示例合集 |
| [SirRamEsq/SmartShape2D](https://github.com/SirRamEsq/SmartShape2D) | 1707 | GDScript | 2D 地形 / 形状绘制工具 |
| [gaea-godot/gaea](https://github.com/gaea-godot/gaea) | 1592 | GDScript | Godot 4 的程序化生成插件 |
| [TheDuckCow/godot-road-generator](https://github.com/TheDuckCow/godot-road-generator) | 1069 | GDScript | 生成 3D 道路 / 街道并支持车道跟随交通的插件 |

### 编辑器、开发工具与语言绑定

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [godot-rust/gdext](https://github.com/godot-rust/gdext) | 4904 | Rust | Godot 4 的 Rust 绑定 |
| [focus-creative-games/luban](https://github.com/focus-creative-games/luban) | 4455 | C# | 强大稳定的游戏配置数据解决方案 |
| [MattParkerDev/SharpIDE](https://github.com/MattParkerDev/SharpIDE) | 3774 | C# | 用 .NET + Godot 构建的跨平台 .NET IDE |
| [GodotSteam/GodotSteam](https://github.com/GodotSteam/GodotSteam) | 3705 | - | 对接 Steam 平台的 Godot 工具生态 |
| [bitwes/Gut](https://github.com/bitwes/Gut) | 2600 | GDScript | Godot 单元测试工具(GUT) |
| [CraterCrash/godot-orchestrator](https://github.com/CraterCrash/godot-orchestrator) | 1548 | C++ | 可视化脚本编辑器 Orchestrator |
| [godot-gdunit-labs/gdUnit4](https://github.com/godot-gdunit-labs/gdUnit4) | 1117 | GDScript | Godot 4 内嵌单元测试框架,支持 GDScript 与 C# |
| [abarichello/godot-ci](https://github.com/abarichello/godot-ci) | 1088 | Dockerfile | 导出 Godot 游戏的 Docker 镜像,含 CI 部署模板 |
| [DmitriySalnikov/godot_debug_draw_3d](https://github.com/DmitriySalnikov/godot_debug_draw_3d) | 1026 | C++ | 绘制 3D 调试图形与 2D 叠加层的插件 |
| [Maran23/script-ide](https://github.com/Maran23/script-ide) | 1009 | GDScript | 把脚本界面改造成 IDE 体验的插件(多标签 / 大纲 / 快速跳转) |

### 框架与游戏系统

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [liangxiegame/QFramework](https://github.com/liangxiegame/QFramework) | 5329 | C# | Godot / Unity 通用的系统设计架构框架 |
| [ramokz/phantom-camera](https://github.com/ramokz/phantom-camera) | 3410 | GDScript | Godot 4 相机插件,灵感来自 Cinemachine |
| [KoBeWi/Metroidvania-System](https://github.com/KoBeWi/Metroidvania-System) | 1510 | GDScript | 制作银河恶魔城类游戏的通用框架 |
| [bitbrain/pandora](https://github.com/bitbrain/pandora) | 1059 | GDScript | RPG 数据管理插件:物品、背包、技能、怪物、任务、NPC |

### 学习资源、模板与示例项目

| 仓库 | ★ | 语言 | 简介 |
|---|---|---|---|
| [godotengine/awesome-godot](https://github.com/godotengine/awesome-godot) | 10210 | - | 精选的 Godot 免费插件 / 脚本 / 扩展清单 |
| [0xFA11/MultiplayerNetworkingResources](https://github.com/0xFA11/MultiplayerNetworkingResources) | 8556 | C | 多人游戏网络编程资源精选清单 |
| [godotengine/godot-docs](https://github.com/godotengine/godot-docs) | 5430 | reStructuredText | Godot 引擎官方文档 |
| [Revolutionary-Games/Thrive](https://github.com/Revolutionary-Games/Thrive) | 3580 | C# | 开源进化模拟游戏 Thrive 的主仓库(可参考的完整项目) |
| [gdquest-demos/godot-open-rpg](https://github.com/gdquest-demos/godot-open-rpg) | 2831 | GDScript | 回合制战斗 RPG 开源教学示例 |
| [GDQuest/learn-gdscript](https://github.com/GDQuest/learn-gdscript) | 2694 | GDScript | 浏览器内从零学习 GDScript 的免费课程 |
| [nezvers/Godot-GameTemplate](https://github.com/nezvers/Godot-GameTemplate) | 1598 | GDScript | 俯视角射击游戏模板,含多种常见问题解法 |
| [Maaack/Godot-Game-Template](https://github.com/Maaack/Godot-Game-Template) | 1497 | GDScript | 含主菜单 / 选项 / 暂停 / 场景加载等的游戏模板 |
| [drwhut/tabletop-club](https://github.com/drwhut/tabletop-club) | 1443 | GDScript | 基于物理的 3D 桌游平台(可参考的完整项目) |
| [gdquest-demos/godot-2d-space-game](https://github.com/gdquest-demos/godot-2d-space-game) | 1075 | GDScript | 2D 太空探索 / 采矿示例游戏 |
