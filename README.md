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
collect.sh                 # 阶段 A 采集脚本(gh → JSONL)
load.py                    # 阶段 B 装载脚本(JSONL → godot.db)
verify.sh                  # 验收脚本
tests/test_load.py         # load.py 单元测试
data/raw/*.jsonl           # 采集产出:5 个 topic + manual.jsonl(手动补充)
godot.db                   # SQLite 输出(已入库)
godot.db.meta.md           # godot.db 数据字典 / 内容说明
export_csv.py              # godot.db → godot_repos.csv(含 category、独立游戏开发指数)
godot_repos.csv            # 扁平数据表(utf-8-sig),供 notebook 读取
build_notebook.py          # godot_repos.csv → 渲染 notebook(纯 HTML、无代码)
godot_repos_matrix.ipynb   # 颜色矩阵 + 排行榜 + 按类型分类对比(GitHub 在线可渲染)
visual_style_画面风格参考/  # 画面 / 美术风格参考资料目录
docs/superpowers/specs/    # 原始设计文档(自动采集管线)
docs/superpowers/plans/    # 原始实现计划
```

## 重跑与限制

- **重跑安全**:JSONL 覆盖写;SQLite `INSERT OR REPLACE`。
- **API 配额**:GitHub 搜索 API 每查询最多 1000 条、限速约 30 次/分钟;5 个 topic 各 1 次调用,远低于限制。
- **数据时效**:star/活跃度随时间变化,建议定期手动重跑 `./collect.sh && python3 load.py && ./verify.sh`。

## 生态导览(按领域分类)

下表来自本仓库 `godot.db`,共 **64 个仓库**。其中 51 个来自 5 个 topic(`godot-engine`、`godot4`、`godot`、`godot-addon`、`gdscript`)的自动采集(`star ≥ 1000` 且最近 3 个月有推送);另有 13 个为**手动补充**(在 `godot.db` 里以来源 `manual` 标注):它们多用于 2D / 模拟经营 / 手感 / 特效,虽未达自动采集门槛(star 偏低、无 topic 标签、或不在活跃窗口),但实用价值高,故单独纳入。按"插件 / 工具链的实际用途"归类,每个领域内按 star 降序。引擎本体 `godotengine/godot` 不是插件 / 工具,已从导览中略去,故下列 **63 个**。手动补充项在「独特领先性」列以 `[手动补充]` 标注。

### 发行版

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [Redot-Engine/redot-engine](https://github.com/Redot-Engine/redot-engine) | 5880 | C++ | Godot 的社区分叉发行版 Redot | 唯一形成规模的 Godot 分叉,为有治理/品牌独立诉求的团队提供"非基金会"替代 |

### AI 辅助开发与 LLM 集成

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | 22010 | Shell | 把 Claude Code 变成完整游戏工作室:多 AI agent + 工作流技能协同 | 把开发拆成 49 个 AI agent + 72 技能、模拟真实工作室层级,协同规模本领域最大 |
| [htdt/godogen](https://github.com/htdt/godogen) | 3583 | Python | 用 Claude Code / Codex 为 Godot、Bevy 做自主游戏开发 | 少见地同时支持 Godot 与 Bevy,且 Claude / Codex 双后端可切换 |
| [KsanaDock/Microverse](https://github.com/KsanaDock/Microverse) | 2375 | GDScript | 基于 Godot 4 的多智能体 AI 社会模拟沙盒 | 不是工具而是把 LLM 当"居民":AI 有独立思考、记忆与自发社交关系 |
| [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp) | 4319 | JavaScript | 让 AI 通过 MCP 协议操控 Godot 编辑器、运行项目、抓调试输出 | 最早一批 Godot 的 MCP 桥,让 AI 直接驱动编辑器并回读运行/调试结果 |
| [nobodywho-ooo/nobodywho](https://github.com/nobodywho-ooo/nobodywho) | 1010 | Rust | 在本地设备上高效运行 LLM 的推理引擎,可接入游戏 | 把本地 LLM 做成游戏运行时插件,离线、保护隐私、可跑在玩家设备 |

### 游戏 AI 与行为

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [bitbrain/beehave](https://github.com/bitbrain/beehave) | 3141 | GDScript | 纯 GDScript 行为树 AI,带可视化调试器 | 零依赖纯 GDScript + 运行时可视化调试,GDScript 生态里最易上手的行为树 |
| [limbonaut/limboai](https://github.com/limbonaut/limboai) | 2817 | C++ | 行为树 + 状态机的 C++ 扩展,带可视化编辑器 | C++ 原生性能 + 行为树与层级状态机二合一 + 接近官方品质的可视化编辑器 |
| [edbeeching/godot_rl_agents](https://github.com/edbeeching/godot_rl_agents) | 1508 | Python | 用强化学习训练 NPC / agent 复杂行为的开源框架 | 把 Godot 变成 RL 训练环境并打通 Gym/SB3/PettingZoo,学界用 Godot 做 RL 的主流选择 |

### 对话与叙事

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [dialogic-godot/dialogic](https://github.com/dialogic-godot/dialogic) | 5726 | GDScript | 对话、视觉小说、角色管理一体化插件 | 可视化时间轴编辑器 + 角色/立绘/分支一体,叙事插件里功能最全 |
| [nathanhoad/godot_dialogue_manager](https://github.com/nathanhoad/godot_dialogue_manager) | 3654 | GDScript | 面向非线性剧情的强大对话系统 | 用类脚本纯文本写非线性对话、可内嵌表达式,对程序员最友好、最轻量 |
| [mhgolkar/Arrow](https://github.com/mhgolkar/Arrow) | 1307 | GDScript | 节点式游戏叙事 / 互动小说设计工具 | [手动补充] 可视化节点流程做分支叙事,独立编辑器,适合互动小说 / 文字冒险 |

### 网络与多人

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [heroiclabs/nakama](https://github.com/heroiclabs/nakama) | 12778 | Go | 可扩展的开源游戏后端:多人、匹配、排行榜、聊天、社交 | 工业级开源后端的事实标准,功能广度远超任何纯 Godot 网络插件 |
| [zfoo-project/zfoo](https://github.com/zfoo-project/zfoo) | 2003 | Java | 极速企业级服务器框架,适用于 RPC / 游戏服 / Web 服 | 序列化/RPC 跑分领先,面向大并发游戏服的高性能 Java 框架 |
| [foxssake/netfox](https://github.com/foxssake/netfox) | 1011 | GDScript | 构建 Godot 多人游戏的网络同步插件集 | 专做客户端预测 + 回滚,补齐官方多人 API 缺失的高级同步能力 |

### 美术与创作工具

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [Orama-Interactive/Pixelorama](https://github.com/Orama-Interactive/Pixelorama) | 9771 | GDScript | 跨平台开源像素画 / 精灵 / 动画创作工具 | 用 Godot 自身打造、最成熟的开源像素画工具,含动画/瓦片/网页版 |
| [RodZill4/material-maker](https://github.com/RodZill4/material-maker) | 5554 | GDScript | 程序化材质制作与 3D 模型贴图绘制工具 | 开源版 Substance Designer:节点式程序纹理 + 3D 绘制,免费替代商业工具 |
| [gdquest-demos/godot-shaders](https://github.com/gdquest-demos/godot-shaders) | 4008 | GDShader | 大量免费开源的 2D/3D 着色器库,含可玩示例 | 最大的免费 Godot 着色器库,每个都带可玩 demo,即拿即用 |
| [MewPurPur/GodSVG](https://github.com/MewPurPur/GodSVG) | 2537 | GDScript | 跨平台的结构化 SVG 矢量图编辑器 | 罕见地直接编辑 SVG 源码结构而非栅格,矢量精确可控 |
| [elringus/sprite-dicing](https://github.com/elringus/sprite-dicing) | 1502 | Rust | 跨引擎的精灵无损压缩工具(复用相同区域) | 独门的精灵切块去重算法,无损且跨引擎,显著节省显存 |
| [viniciusgerevini/godot-aseprite-wizard](https://github.com/viniciusgerevini/godot-aseprite-wizard) | 1314 | GDScript | 把 Aseprite 动画批量导入 Godot(AnimationPlayer / SpriteFrames 等) | [手动补充] 像素动画工作流标杆,Aseprite→Godot 一键同步,省去手切帧 |
| [gdquest-demos/godot-visual-effects](https://github.com/gdquest-demos/godot-visual-effects) | 1262 | GDScript | 用 Godot 制作的开源视觉特效合集 | GDQuest 出品的成体系 VFX 范例,配套教学课程 |

### 地形与世界生成

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [TokisanGames/Terrain3D](https://github.com/TokisanGames/Terrain3D) | 3988 | C++ | Godot 4 的高性能可编辑地形系统 | C++ + clipmap 实现,Godot 4 性能最强、可做大世界的地形系统 |
| [HungryProton/scatter](https://github.com/HungryProton/scatter) | 2896 | GDScript | 基于规则的程序化物体散布(草木 / 石头等) | [手动补充] 用规则批量散布并自动避让,关卡美术铺面神器,远胜手动摆放 |
| [Zylann/godot_heightmap_plugin](https://github.com/Zylann/godot_heightmap_plugin) | 2209 | GDScript | 基于高度图的地形插件(纯 GDScript) | 老牌纯 GDScript 高度图地形,无需编译、开箱跨平台 |
| [gdquest-demos/godot-4-procedural-generation](https://github.com/gdquest-demos/godot-4-procedural-generation) | 1862 | GDScript | 程序化生成算法与示例合集 | GDQuest 整理的成体系程序生成算法,既能学也能直接复用 |
| [SirRamEsq/SmartShape2D](https://github.com/SirRamEsq/SmartShape2D) | 1707 | GDScript | 2D 地形 / 形状绘制工具 | 2D 领域少见的样条地形绘制,边缘自动贴图,补 2D 地形空白 |
| [gaea-godot/gaea](https://github.com/gaea-godot/gaea) | 1592 | GDScript | Godot 4 的程序化生成插件 | 节点式程序生成、2D/3D 通用,可在编辑器内可视化调参 |
| [TheDuckCow/godot-road-generator](https://github.com/TheDuckCow/godot-road-generator) | 1069 | GDScript | 生成 3D 道路 / 街道并支持车道跟随交通的插件 | 专攻 3D 道路 + 车道跟随交通,这个细分需求几乎独一份 |
| [Portponky/better-terrain](https://github.com/Portponky/better-terrain) | 737 | GDScript | 更灵活的 2D autotile / 地形绘制插件 | [手动补充] 比内置 TileMapLayer 地形更顺手的 2D autotile 方案,适合农田/道路/墙体 |
| [Kiamo2/YATI](https://github.com/Kiamo2/YATI) | 287 | GDScript | 把 Tiled(.tmx/.tmj)地图导入 Godot 4 | [手动补充] Tiled 地图导入最全的方案,支持层/对象/碰撞/动画/自定义属性 |

### 编辑器、开发工具与语言绑定

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [godot-rust/gdext](https://github.com/godot-rust/gdext) | 4904 | Rust | Godot 4 的 Rust 绑定 | 社区主力的 Godot 4 Rust 绑定,内存安全 + 接近原生性能 |
| [focus-creative-games/luban](https://github.com/focus-creative-games/luban) | 4455 | C# | 强大稳定的游戏配置数据解决方案 | 跨引擎配置中台:Excel→多语言代码/多格式,大厂级配置方案 |
| [MattParkerDev/SharpIDE](https://github.com/MattParkerDev/SharpIDE) | 3774 | C# | 用 .NET + Godot 构建的跨平台 .NET IDE | 罕见地用 Godot 自身做 UI 的跨平台 .NET IDE |
| [GodotSteam/GodotSteam](https://github.com/GodotSteam/GodotSteam) | 3705 | - | 对接 Steam 平台的 Godot 工具生态 | Steam 集成事实标准,覆盖成就/创意工坊/联机/输入等全套 API |
| [bitwes/Gut](https://github.com/bitwes/Gut) | 2600 | GDScript | Godot 单元测试工具(GUT) | GDScript 单测元老,生态最广、教程最多 |
| [CraterCrash/godot-orchestrator](https://github.com/CraterCrash/godot-orchestrator) | 1548 | C++ | 可视化脚本编辑器 Orchestrator | 把虚幻式蓝图可视化脚本带进 Godot,对非程序员友好 |
| [2shady4u/godot-sqlite](https://github.com/2shady4u/godot-sqlite) | 1395 | C++ | Godot 4.x 的 SQLite GDExtension 封装 | [手动补充] 把关系型数据库带进 Godot,适合大数据量/可查询的经营记录与报表 |
| [godot-gdunit-labs/gdUnit4](https://github.com/godot-gdunit-labs/gdUnit4) | 1117 | GDScript | Godot 4 内嵌单元测试框架,支持 GDScript 与 C# | 唯一同时覆盖 GDScript + C# 的内嵌测试框架,带 mock 与场景测试 |
| [abarichello/godot-ci](https://github.com/abarichello/godot-ci) | 1088 | Dockerfile | 导出 Godot 游戏的 Docker 镜像,含 CI 部署模板 | 一键 CI 导出镜像 + GitHub/GitLab 模板,直推 Pages / Itch.io |
| [DmitriySalnikov/godot_debug_draw_3d](https://github.com/DmitriySalnikov/godot_debug_draw_3d) | 1026 | C++ | 绘制 3D 调试图形与 2D 叠加层的插件 | 专做低开销 3D 调试可视化(射线/形状/图表),C++ 实现 |
| [Maran23/script-ide](https://github.com/Maran23/script-ide) | 1009 | GDScript | 把脚本界面改造成 IDE 体验的插件(多标签 / 大纲 / 快速跳转) | 把内置脚本面板升级为 IDE 体验,编码效率细节体验领先 |
| [don-tnowe/godot-resources-as-sheets-plugin](https://github.com/don-tnowe/godot-resources-as-sheets-plugin) | 1008 | GDScript | 像表格一样批量编辑 Godot Resources,支持 CSV | [手动补充] Resource 批量表格化编辑 + CSV 工作流,平衡数值 / 配置表必备 |
| [rsubtil/controller_icons](https://github.com/rsubtil/controller_icons) | 419 | GDScript | 手柄 / 键鼠按键图标,按输入设备自动切换 | [手动补充] 主流手柄 + 键鼠图标库,自动跟随当前输入设备切换提示 |

### 框架与游戏系统

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [liangxiegame/QFramework](https://github.com/liangxiegame/QFramework) | 5329 | C# | Godot / Unity 通用的系统设计架构框架 | 跨 Godot/Unity 的成体系架构方法论(配套书籍),中文社区影响力大 |
| [ramokz/phantom-camera](https://github.com/ramokz/phantom-camera) | 3410 | GDScript | Godot 4 相机插件,灵感来自 Cinemachine | Godot 版 Cinemachine:声明式相机与过渡、2D/3D 通用,相机插件标杆 |
| [derkork/godot-statecharts](https://github.com/derkork/godot-statecharts) | 1560 | GDScript | 状态图(statechart)扩展,比普通 FSM 更可控 | [手动补充] 层级 / 并行状态图,管理顾客 / 员工 / 建筑 / UI 多状态不易爆炸,经营模拟利器 |
| [KoBeWi/Metroidvania-System](https://github.com/KoBeWi/Metroidvania-System) | 1510 | GDScript | 制作银河恶魔城类游戏的通用框架 | 专攻银河恶魔城的地图/小地图/存档,细分品类唯一成熟方案 |
| [bitbrain/pandora](https://github.com/bitbrain/pandora) | 1059 | GDScript | RPG 数据管理插件:物品、背包、技能、怪物、任务、NPC | 编辑器内可视化的 RPG 数据建模,数据驱动、面向内容创作者 |
| [peter-kish/gloot](https://github.com/peter-kish/gloot) | 928 | GDScript | 通用库存系统(掉落 / 战利品 / 容器) | [手动补充] 高度通用、可自由拼装的库存框架 |
| [expressobits/inventory-system](https://github.com/expressobits/inventory-system) | 724 | C++ | 模块化库存系统,逻辑与 UI 分离,兼容多人 | [手动补充] 物品用 Resource、逻辑/UI 解耦、支持多人同步的成品库存模块 |
| [Kelpekk/Juicee](https://github.com/Kelpekk/Juicee) | 40 | GDScript | 90 种 game-feel 手感效果,带可视化图编辑器 | [手动补充] 屏幕震动/hit-stop/伤害数字/弹簧等手感效果集大成,可视化编辑 |
| [neohex-interactive/sparkelite](https://github.com/neohex-interactive/sparkelite) | 9 | GDScript | 轻量 game-feel 反馈序列,一个 play() 触发 | [手动补充] 把震屏/顿帧/闪白/缩放打击堆成序列,一键触发,极简 |

### 学习资源、模板与示例项目

| 仓库 | ★ | 语言 | 简介 | 独特领先性 |
|---|---|---|---|---|
| [godotengine/awesome-godot](https://github.com/godotengine/awesome-godot) | 10210 | - | 精选的 Godot 免费插件 / 脚本 / 扩展清单 | 官方维护的生态总入口,最权威的资源清单 |
| [0xFA11/MultiplayerNetworkingResources](https://github.com/0xFA11/MultiplayerNetworkingResources) | 8556 | C | 多人游戏网络编程资源精选清单 | 跨引擎的多人网络编程权威书单,垂直主题里 star 最高 |
| [godotengine/godot-docs](https://github.com/godotengine/godot-docs) | 5430 | reStructuredText | Godot 引擎官方文档 | 官方文档源,最权威、最及时 |
| [Revolutionary-Games/Thrive](https://github.com/Revolutionary-Games/Thrive) | 3580 | C# | 开源进化模拟游戏 Thrive 的主仓库(可参考的完整项目) | 体量最大的开源 Godot 游戏之一,复杂模拟系统的工程参考 |
| [gdquest-demos/godot-open-rpg](https://github.com/gdquest-demos/godot-open-rpg) | 2831 | GDScript | 回合制战斗 RPG 开源教学示例 | GDQuest 出品的回合制 RPG 完整教学项目,系统拆解清晰 |
| [GDQuest/learn-gdscript](https://github.com/GDQuest/learn-gdscript) | 2694 | GDScript | 浏览器内从零学习 GDScript 的免费课程 | 浏览器内交互式学 GDScript,零环境门槛 |
| [nezvers/Godot-GameTemplate](https://github.com/nezvers/Godot-GameTemplate) | 1598 | GDScript | 俯视角射击游戏模板,含多种常见问题解法 | 内含联机/存档等"硬骨头"现成解法的成品模板 |
| [Maaack/Godot-Game-Template](https://github.com/Maaack/Godot-Game-Template) | 1497 | GDScript | 含主菜单 / 选项 / 暂停 / 场景加载等的游戏模板 | 菜单/选项/暂停/场景加载开箱即用,接近可发布的骨架 |
| [drwhut/tabletop-club](https://github.com/drwhut/tabletop-club) | 1443 | GDScript | 基于物理的 3D 桌游平台(可参考的完整项目) | 物理驱动的开源桌游平台,完整可玩、可改造 |
| [gdquest-demos/godot-2d-space-game](https://github.com/gdquest-demos/godot-2d-space-game) | 1075 | GDScript | 2D 太空探索 / 采矿示例游戏 | 带 AI 框架的 2D 太空游戏范例,演示自研 AI 用法 |
