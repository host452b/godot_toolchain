"""生成 art_styles.csv(utf-8-sig)与 art_styles_matrix.ipynb(nbformat 4)。

实现 2D 画风分析的颜色矩阵:
- 评分列(Steam欢迎度 / 商业安全性 / 独立适配度)红(低)→黄→绿(高)
- 制作难度为反向列:低=绿(对小团队友好)、高=红(成本风险)
- 着色用每个 <td> 的 inline style,不用 <style> 块 → GitHub 在线可渲染
- notebook 不含可见代码,HTML 烘焙进单元输出

评分为基于原始分析(制作难度 / 商业安全性 / Steam Top8 排名)派生的主观量化,0–100。
"""
import csv
import nbformat as nbf

# 15 个画风。score 字段(0-100):steam=Steam欢迎度, safe=商业安全性,
# diff=制作难度(反向着色), fit=独立团队适配度。
STYLES = [
    {"序号": 1, "中文画风": "像素风", "英文": "Pixel Art",
     "核心视觉特征": "低分辨率网格、清晰轮廓、有限色板、强符号化", "常见视角": "横版/俯视/等距",
     "适合类型": "平台跳跃/生存建造/RPG/roguelike", "代表作": "Terraria、Stardew Valley、Celeste、Vampire Survivors",
     "Prompt关键词": "pixel art, limited palette, crisp sprites",
     "steam": 95, "safe": 85, "diff": 50, "fit": 90},
    {"序号": 2, "中文画风": "高精度像素风", "英文": "High-detail Pixel Art",
     "核心视觉特征": "大尺寸像素角色、复杂材质、粒子、动态光影", "常见视角": "横版/等距/俯视",
     "适合类型": "metroidvania/动作 roguelite/ARPG", "代表作": "Dead Cells、Eastward、Noita",
     "Prompt关键词": "detailed pixel art, dynamic lighting, rich tileset",
     "steam": 88, "safe": 85, "diff": 85, "fit": 65},
    {"序号": 3, "中文画风": "复古街机风", "英文": "Retro Arcade",
     "核心视觉特征": "霓虹、CRT 扫描线、机台感、高对比 UI", "常见视角": "俯视/横版/固定屏",
     "适合类型": "弹幕/清版/街机动作/幸存者类", "代表作": "Vampire Survivors、Brotato、Downwell",
     "Prompt关键词": "retro arcade, CRT, neon score UI",
     "steam": 72, "safe": 70, "diff": 35, "fit": 85},
    {"序号": 4, "中文画风": "手绘卡通风", "英文": "Hand-drawn Cartoon",
     "核心视觉特征": "手绘轮廓、夸张形体、柔和变形动画、可读性强", "常见视角": "横版/俯视/等距",
     "适合类型": "roguelike/动作冒险/平台/解谜", "代表作": "Cuphead、Cult of the Lamb、Don't Starve",
     "Prompt关键词": "hand-drawn cartoon, expressive silhouettes",
     "steam": 78, "safe": 85, "diff": 85, "fit": 50},
    {"序号": 5, "中文画风": "暗黑手绘风", "英文": "Dark Hand-drawn",
     "核心视觉特征": "墨线、冷色、局部高亮、阴影压迫、怪诞生态", "常见视角": "横版/侧视/2.5D",
     "适合类型": "metroidvania/魂味动作/探索冒险", "代表作": "Hollow Knight、Darkest Dungeon",
     "Prompt关键词": "dark hand-drawn, moody ink linework",
     "steam": 82, "safe": 85, "diff": 85, "fit": 55},
    {"序号": 6, "中文画风": "哥特童话风", "英文": "Gothic Fairytale",
     "核心视觉特征": "童话比例 + 哥特建筑、尖拱、黑白灰、病态优雅", "常见视角": "横版/固定镜头",
     "适合类型": "解谜/叙事/metroidvania/恐怖童话", "代表作": "Fran Bow、Little Nightmares(2.5D)",
     "Prompt关键词": "gothic fairytale, eerie storybook",
     "steam": 50, "safe": 50, "diff": 85, "fit": 40},
    {"序号": 7, "中文画风": "日系二次元风", "英文": "Anime Style",
     "核心视觉特征": "大眼角色、清洁线稿、赛璐璐上色、角色吸引力强", "常见视角": "横版/俯视/视觉小说式",
     "适合类型": "RPG/galgame/动作/卡牌/养成", "代表作": "Omori、Muse Dash",
     "Prompt关键词": "anime style, cel shading, clean lineart",
     "steam": 65, "safe": 70, "diff": 65, "fit": 45},
    {"序号": 8, "中文画风": "可爱治愈风", "英文": "Cozy Cute",
     "核心视觉特征": "圆润角色、低威胁、暖色、柔软材质、生活感 UI", "常见视角": "俯视/等距/横版",
     "适合类型": "farming sim/收集/经营/轻度冒险", "代表作": "Stardew Valley、A Short Hike、Spiritfarer",
     "Prompt关键词": "cozy cute, warm palette, wholesome",
     "steam": 85, "safe": 85, "diff": 50, "fit": 75},
    {"序号": 9, "中文画风": "美式漫画风", "英文": "Comic Book Style",
     "核心视觉特征": "粗描边、网点、速度线、分镜式构图、夸张表情", "常见视角": "横版/俯视/卡牌桌面",
     "适合类型": "动作/卡牌/叙事/格斗", "代表作": "Darkest Dungeon、Monster Prom",
     "Prompt关键词": "comic book, bold ink, halftone",
     "steam": 55, "safe": 50, "diff": 65, "fit": 50},
    {"序号": 10, "中文画风": "极简几何风", "英文": "Minimalist Geometric",
     "核心视觉特征": "基础几何体、低细节、高动效反馈、UI 一体化", "常见视角": "俯视/固定屏/抽象空间",
     "适合类型": "解谜/策略/节奏/街机", "代表作": "Mini Metro、Thomas Was Alone、140",
     "Prompt关键词": "minimalist geometric, clean UI, abstract",
     "steam": 58, "safe": 50, "diff": 20, "fit": 80},
    {"序号": 11, "中文画风": "剪纸 / 皮影风", "英文": "Paper-cut / Shadow Puppet",
     "核心视觉特征": "分层纸片、侧影、材质边缘、舞台感", "常见视角": "横版/固定镜头",
     "适合类型": "解谜/叙事/平台/童话冒险", "代表作": "Papetura、The Procession to Calvary(局部)",
     "Prompt关键词": "paper cutout, layered diorama, shadow puppet",
     "steam": 42, "safe": 50, "diff": 85, "fit": 35},
    {"序号": 12, "中文画风": "水彩绘本风", "英文": "Watercolor Storybook",
     "核心视觉特征": "水彩晕染、纸纹、低对比、绘本构图", "常见视角": "横版/叙事镜头/固定场景",
     "适合类型": "叙事/解谜/轻冒险/亲子向", "代表作": "Gris、Dordogne、Child of Light(参考)",
     "Prompt关键词": "watercolor storybook, paper texture",
     "steam": 48, "safe": 50, "diff": 85, "fit": 35},
    {"序号": 13, "中文画风": "低饱和叙事风", "英文": "Muted Narrative Art",
     "核心视觉特征": "灰调、低饱和、写实简化、情绪留白", "常见视角": "横版/等距/固定镜头",
     "适合类型": "叙事/冒险/解谜/社会议题", "代表作": "Night in the Woods、Oxenfree、Norco",
     "Prompt关键词": "muted narrative art, subdued palette",
     "steam": 56, "safe": 50, "diff": 50, "fit": 60},
    {"序号": 14, "中文画风": "霓虹赛博 2D 风", "英文": "Neon Cyberpunk 2D",
     "核心视觉特征": "黑底霓虹、赛博 UI、强反射、紫青色调", "常见视角": "横版/俯视/等距",
     "适合类型": "动作/潜入/射击/解谜", "代表作": "Katana ZERO、ANNO: Mutationem(2.5D)",
     "Prompt关键词": "neon cyberpunk, magenta cyan lighting",
     "steam": 54, "safe": 50, "diff": 85, "fit": 45},
    {"序号": 15, "中文画风": "黑白高对比风", "英文": "Monochrome High Contrast",
     "核心视觉特征": "黑白剪影、硬边阴影、负空间、强构图", "常见视角": "横版/固定镜头/解谜视角",
     "适合类型": "解谜/恐怖/叙事/平台", "代表作": "Limbo、Return of the Obra Dinn、Minit",
     "Prompt关键词": "monochrome, high contrast, silhouette",
     "steam": 57, "safe": 50, "diff": 50, "fit": 65},
]

CSV_COLS = ["序号", "中文画风", "英文", "核心视觉特征", "常见视角", "适合类型",
            "代表作", "Prompt关键词", "steam", "safe", "diff", "fit"]

with open("art_styles.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=CSV_COLS)
    w.writeheader()
    for s in STYLES:
        w.writerow({k: s[k] for k in CSV_COLS})
print(f"wrote art_styles.csv ({len(STYLES)} styles)")


# ── 色阶 ────────────────────────────────────────────────────
def score_bg(score):
    """score 0-10:红→黄→绿(原始分析的色阶公式)。"""
    ratio = max(0.0, min(1.0, (score - 3) / 7))
    if ratio < 0.5:
        r, g, b = 220, int(60 + ratio * 2 * 180), 60
    else:
        r, g, b = int(220 - (ratio - 0.5) * 2 * 180), 200, int(60 + (ratio - 0.5) * 2 * 40)
    return f"background-color: rgba({r},{g},{b}, 0.4)"


def diff_bg(score10):
    """制作难度反向:低=绿、高=红。"""
    return score_bg(10 - score10)


SCORE_FIELDS = {"steam": "Steam欢迎度", "safe": "商业安全性", "fit": "独立适配度"}
DIFF_FIELD = ("diff", "制作难度")


def cell(style, fld):
    v = style[fld]
    bg = diff_bg(v / 10) if fld == "diff" else score_bg(v / 10)
    return f'<td style="{TD};{bg};text-align:right">{v}</td>'


TH = ("background-color:#222;color:#fff;padding:4px 8px;"
      "white-space:nowrap;text-align:left")
TD = "padding:3px 8px;white-space:nowrap;border-bottom:1px solid #eee"


def render_matrix(styles, title):
    cols_text = ["中文画风", "英文"]
    cols_score = ["steam", "safe", "diff", "fit"]
    cols_tail = ["常见视角", "适合类型", "代表作", "Prompt关键词"]
    head = (["#", "中文画风", "英文", "Steam欢迎度", "商业安全性", "制作难度↓",
             "独立适配度", "常见视角", "适合类型", "代表作", "Prompt关键词"])
    out = [f"<h3>{title}</h3>",
           '<table style="border-collapse:collapse;font-size:11px;'
           'font-family:system-ui,Arial,sans-serif">']
    out.append("<tr>" + "".join(f'<th style="{TH}">{h}</th>' for h in head) + "</tr>")
    for i, s in enumerate(styles, start=1):
        cells = [f'<td style="{TD};color:#888">{i}</td>',
                 f'<td style="{TD}"><b>{s["中文画风"]}</b></td>',
                 f'<td style="{TD}">{s["英文"]}</td>']
        for fld in cols_score:
            cells.append(cell(s, fld))
        for fld in cols_tail:
            cells.append(f'<td style="{TD}">{s[fld]}</td>')
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</table>")
    out.append('<p style="font-size:11px;color:#666">↓ 制作难度为反向色阶:'
               '<b>绿=低成本(小团队友好)</b>、红=高成本。其余列高=绿。'
               '评分为基于原始分析派生的主观量化(0–100)。</p>')
    return "\n".join(out)


def render_ranking(styles, title):
    head = ["#", "中文画风", "代表作", "Steam欢迎度", "商业安全性", "独立适配度"]
    out = [f"<h3>{title}</h3>",
           '<table style="border-collapse:collapse;font-size:12px;'
           'font-family:system-ui,Arial,sans-serif">']
    out.append("<tr>" + "".join(f'<th style="{TH}">{h}</th>' for h in head) + "</tr>")
    for i, s in enumerate(styles, start=1):
        cells = [f'<td style="{TD};color:#888">{i}</td>',
                 f'<td style="{TD}"><b>{s["中文画风"]}</b></td>',
                 f'<td style="{TD}">{s["代表作"]}</td>',
                 cell(s, "steam"), cell(s, "safe"), cell(s, "fit")]
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def html_cell(html):
    c = nbf.v4.new_code_cell(source="")
    c["execution_count"] = None
    c["outputs"] = [nbf.v4.new_output("display_data", data={"text/html": html})]
    return c


cells = []
cells.append(nbf.v4.new_markdown_cell(
    "# 2D 游戏画风 · 颜色矩阵\n"
    "\n"
    "15 种 Steam 常见 2D 画风的对比矩阵。数据来自 `art_styles.csv`。\n"
    "\n"
    "**色阶**:`Steam欢迎度 / 商业安全性 / 独立适配度` 越高越绿;`制作难度` 反向——"
    "越低越绿(对小团队越友好)。评分为基于原始分析(制作难度 / 商业安全性 / Steam Top8 排名)"
    "派生的主观量化(0–100)。详尽分析、Prompt 模板与开发建议见 `README.md`。"
))
cells.append(html_cell(render_matrix(STYLES, "全 15 种画风对比矩阵(按表序)")))
top8 = sorted(STYLES, key=lambda s: s["steam"], reverse=True)[:8]
cells.append(html_cell(render_ranking(top8, "★ Steam 欢迎度 Top 8")))
indie8 = sorted(STYLES, key=lambda s: s["fit"], reverse=True)[:8]
cells.append(html_cell(render_ranking(indie8, "🛠 独立团队适配度 Top 8")))

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}
with open("art_styles_matrix.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print(f"wrote art_styles_matrix.ipynb ({len(cells)} cells, no visible code)")
