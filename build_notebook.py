"""从 godot_repos.csv 生成 godot_repos_matrix.ipynb(nbformat 4)。

特点:notebook 里**不含可见代码**——HTML 在本脚本里算好,直接烘焙进各单元的
输出(text/html),每块渲染各自独立。GitHub 在线打开只显示彩色表格。

渲染规范(适配自 best-of-everything.consensus/shanghai-housing):
- 完整数据表分页(50 行/页),字号 9px,nowrap,标题 <h4>第X-Y/总数</h4>
- 排行榜字号 11px,Top 15,标题 <h3>
- 评分列红→黄→绿色阶;价格类数字右对齐不着色;名称列加粗
- 着色用每个 <td> 的 inline style,不用 <style> 块。

godot 无 0-10 主观评分,评分列(stars / forks / stars_per_month)先按列
min-max 归一到 0-10 再代入色阶公式。
"""
import csv
import bisect
import nbformat as nbf

# ── 读取 CSV(utf-8-sig)──────────────────────────────────────
with open("godot_repos.csv", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

INT_COLS = ["stars", "forks", "open_issues", "indie_game_index"]
for r in rows:
    for c in INT_COLS:
        r[c] = int(r[c])
    r["stars_per_month"] = float(r["stars_per_month"])

TOTAL = len(rows)
SCORE_COLS = ["stars", "forks", "stars_per_month"]   # 评分列:红(低)→黄→绿(高),按分位归一
ABS100_COLS = ["indie_game_index"]                   # 0-100 绝对评分:红(低)→黄→绿(高)
VAR_COLS = ["open_issues"]                            # 方差/风险列:绿(低)→红(高),反向

# 指标偏态严重(如 stars 跨 1e3~1e5),直接 min-max 会把多数值挤到一端、颜色分块。
# 改用按排名分位(percentile)归一,让色阶沿排序行平滑铺开。
_SORTED = {c: sorted(r[c] for r in rows) for c in SCORE_COLS + VAR_COLS}


def _percentile(col, value):
    vals = _SORTED[col]
    n = len(vals)
    if n <= 1:
        return 0.0
    lo = bisect.bisect_left(vals, value)
    hi = bisect.bisect_right(vals, value)
    rank = (lo + hi - 1) / 2          # 并列取平均名次
    return rank / (n - 1)             # 0..1


def score_bg(score):
    """score 为 0-10,返回红→黄→绿的 rgba 背景(规范公式)。"""
    ratio = max(0.0, min(1.0, (score - 3) / 7))
    if ratio < 0.5:
        r, g, b = 220, int(60 + ratio * 2 * 180), 60          # 红→黄
    else:
        r = int(220 - (ratio - 0.5) * 2 * 180)
        g = 200
        b = int(60 + (ratio - 0.5) * 2 * 40)                  # 黄→绿
    return f"background-color: rgba({r},{g},{b}, 0.35)"


def variance_bg(v5):
    """v5 为 0-5(反向),平滑过渡:低=绿(健康)→黄→高=红(风险)。

    复用评分列的连续色阶曲线,把输入反过来(v5 越大 ≈ 分数越低 = 越红),
    保证与评分列同一条平滑渐变,不分硬档。"""
    return score_bg(10 - 2 * v5)


def to_score10(col, value):
    return _percentile(col, value) * 10


def to_var5(col, value):
    return _percentile(col, value) * 5


def fmt(col, v):
    return f"{v:,.1f}" if col == "stars_per_month" else f"{int(v):,}"


# ── 完整数据表(分页,9px)────────────────────────────────────
FULL_COLS = ["full_name", "category", "url", "language", "stars", "forks",
             "open_issues", "stars_per_month", "indie_game_index"]


def render_full_page(page_rows, start, end):
    th = ("background-color:#222;color:#fff;padding:3px 6px;"
          "white-space:nowrap;text-align:left")
    td = "padding:2px 6px;white-space:nowrap;border-bottom:1px solid #eee"
    out = [f"<h4>第 {start}-{end} / {TOTAL}</h4>",
           '<table style="border-collapse:collapse;font-size:9px;'
           'font-family:system-ui,Arial,sans-serif">']
    out.append('<tr><th style="' + th + '">#</th>' +
               "".join(f'<th style="{th}">{c}</th>' for c in FULL_COLS) + "</tr>")
    for rank, row in enumerate(page_rows, start=start):
        cells = [f'<td style="{td};color:#888">{rank}</td>']
        for c in FULL_COLS:
            v = row[c]
            if c == "full_name":
                cells.append(f'<td style="{td}"><b>{v}</b></td>')
            elif c == "url":
                cells.append(f'<td style="{td}"><a href="{v}">link</a></td>')
            elif c in SCORE_COLS:
                bg = score_bg(to_score10(c, v))
                cells.append(f'<td style="{td};{bg};text-align:right">{fmt(c, v)}</td>')
            elif c in VAR_COLS:
                bg = variance_bg(to_var5(c, v))
                cells.append(f'<td style="{td};{bg};text-align:right">{int(v):,}</td>')
            elif c in ABS100_COLS:
                bg = score_bg(v / 10)        # 0-100 绝对评分 → 0-10 → 红黄绿
                cells.append(f'<td style="{td};{bg};text-align:right">{int(v)}</td>')
            else:
                cells.append(f'<td style="{td}">{v}</td>')
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


# ── 排行榜(11px,Top 15)────────────────────────────────────
RANK_COLS = ["full_name", "language", "stars", "stars_per_month", "forks"]


def render_ranking(rank_rows, title):
    th = ("background-color:#222;color:#fff;padding:6px 10px;"
          "white-space:nowrap;text-align:left")
    td = "padding:4px 10px;white-space:nowrap;border-bottom:1px solid #eee"
    out = [f"<h3>{title}</h3>",
           '<table style="border-collapse:collapse;font-size:11px;'
           'font-family:system-ui,Arial,sans-serif">']
    out.append('<tr><th style="' + th + '">#</th>' +
               "".join(f'<th style="{th}">{c}</th>' for c in RANK_COLS) + "</tr>")
    for rank, row in enumerate(rank_rows, start=1):
        cells = [f'<td style="{td};color:#888">{rank}</td>']
        for c in RANK_COLS:
            v = row[c]
            if c == "full_name":
                cells.append(f'<td style="{td}"><b>{v}</b></td>')
            elif c in SCORE_COLS:
                bg = score_bg(to_score10(c, v))
                cells.append(f'<td style="{td};{bg};text-align:right">{fmt(c, v)}</td>')
            else:
                cells.append(f'<td style="{td}">{v}</td>')
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


# ── 按类型分类对比(每类一表,<hr> 横线分隔)──────────────────
CMP_COLS = ["full_name", "language", "stars", "forks", "open_issues",
            "stars_per_month", "indie_game_index"]


def render_category(cat, cat_rows):
    th = ("background-color:#333;color:#fff;padding:4px 8px;"
          "white-space:nowrap;text-align:left")
    td = "padding:3px 8px;white-space:nowrap;border-bottom:1px solid #eee"
    out = [f"<h3>{cat} <span style='color:#888;font-weight:normal'>"
           f"({len(cat_rows)})</span></h3>",
           '<table style="border-collapse:collapse;font-size:11px;'
           'font-family:system-ui,Arial,sans-serif">']
    out.append('<tr><th style="' + th + '">#</th>' +
               "".join(f'<th style="{th}">{c}</th>' for c in CMP_COLS) + "</tr>")
    for rank, row in enumerate(cat_rows, start=1):
        cells = [f'<td style="{td};color:#888">{rank}</td>']
        for c in CMP_COLS:
            v = row[c]
            if c == "full_name":
                cells.append(f'<td style="{td}"><b>{v}</b></td>')
            elif c in SCORE_COLS:
                bg = score_bg(to_score10(c, v))
                cells.append(f'<td style="{td};{bg};text-align:right">{fmt(c, v)}</td>')
            elif c in VAR_COLS:
                bg = variance_bg(to_var5(c, v))
                cells.append(f'<td style="{td};{bg};text-align:right">{int(v):,}</td>')
            elif c in ABS100_COLS:
                bg = score_bg(v / 10)
                cells.append(f'<td style="{td};{bg};text-align:right">{int(v)}</td>')
            else:
                cells.append(f'<td style="{td}">{v}</td>')
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def html_cell(html):
    """构造一个无源码、只含 HTML 渲染输出的代码单元。"""
    cell = nbf.v4.new_code_cell(source="")
    cell["execution_count"] = None
    cell["outputs"] = [nbf.v4.new_output("display_data", data={"text/html": html})]
    return cell


# ── 组装 notebook ───────────────────────────────────────────
cells = []
cells.append(nbf.v4.new_markdown_cell(
    "# Godot 生态仓库 · 完整数据表 + 排行榜\n"
    "\n"
    f"数据 {TOTAL} 个仓库,来自 `godot_repos.csv`(5 个 topic、`star ≥ 1000`、最近 3 个月有推送)。"
    "**红绿色阶**:评分列(`stars` / `forks` / `月均涨星`)红(低)→黄→绿(高);"
    "`open_issues` 为风险/健康度列,**反向**——少=绿(健康)、多=红(积压风险);"
    "`indie_game_index`(独立游戏开发指数,0–100,独立开发者刚需程度)按绝对分着色,高=绿;"
    "`full_name` 加粗。下方仅为 HTML 渲染结果(无代码)。"
))

# 完整数据表分页(50 行/页)
PAGE = 50
for s in range(0, TOTAL, PAGE):
    cells.append(html_cell(render_full_page(rows[s:s + PAGE], s + 1, min(s + PAGE, TOTAL))))

# 排行榜
top_stars = sorted(rows, key=lambda r: r["stars"], reverse=True)[:15]
top_growth = sorted(rows, key=lambda r: r["stars_per_month"], reverse=True)[:15]
cells.append(html_cell(render_ranking(top_stars, "★ Stars 排行 Top 15")))
cells.append(html_cell(render_ranking(top_growth, "📈 月均涨星 排行 Top 15")))

# 按类型分类对比:类别按首次出现顺序(CSV 已按 stars 降序),类内按 stars 降序,<hr> 分隔
cat_order = []
cat_rows = {}
for r in rows:
    cat = r["category"]
    if cat not in cat_rows:
        cat_order.append(cat)
        cat_rows[cat] = []
    cat_rows[cat].append(r)
cmp_blocks = [render_category(cat, cat_rows[cat]) for cat in cat_order]
cells.append(nbf.v4.new_markdown_cell("# 按类型分类对比"))
cells.append(html_cell("\n<hr>\n".join(cmp_blocks)))

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}

with open("godot_repos_matrix.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print(f"wrote godot_repos_matrix.ipynb ({len(cells)} cells, no visible code)")
