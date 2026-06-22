"""生成 godot_repos_matrix.ipynb(nbformat 4)。

渲染规范(适配自 best-of-everything.consensus/shanghai-housing):
- 读取 CSV(utf-8-sig 编码)
- 完整数据表分页(50 行/页),字号 8-9px,nowrap,标题 <h4>第X-Y/总数</h4>
- 评分列注入红→黄→绿色阶(higher 越绿);价格类数字列右对齐不着色;名称列加粗
- 排行榜:字号 11px,Top 15,标题 <h3>
- 着色用每个 <td> 的 inline style="background-color:rgba(...)",不用 <style> 块,
  这样 GitHub 在线查看 .ipynb 时颜色不会被剥掉。

godot 数据无 0-10 主观评分,故评分列(stars / forks / stars_per_month)先按列
min-max 归一到 0-10,再代入色阶公式。
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell(
    "# Godot 生态仓库 · 完整数据表 + 排行榜\n"
    "\n"
    "数据来自 `godot_repos.csv`(由 `export_csv.py` 从 `godot.db` 导出,utf-8-sig)。"
    "覆盖 5 个 topic、`star ≥ 1000`、最近 3 个月有推送,去重后 51 个仓库。\n"
    "\n"
    "**色阶规则**:评分列(`stars` / `forks` / `月均涨星`)按列归一到 0–10 后,"
    "红(低)→黄→绿(高);`open_issues` 视为中性计数,右对齐不着色;`full_name` 加粗。\n"
    "着色用单元格 inline 样式,**GitHub 在线即可见颜色**。"
))

# ── 单元1:读取 CSV + 着色函数 ───────────────────────────────
cells.append(nbf.v4.new_code_cell(
    "import pandas as pd\n"
    "from IPython.display import HTML, display\n"
    "\n"
    "df = pd.read_csv('godot_repos.csv', encoding='utf-8-sig')\n"
    "TOTAL = len(df)\n"
    "\n"
    "# 评分列(higher 越好,着红→黄→绿);价格类数字列(右对齐不着色);名称/链接列\n"
    "SCORE_COLS = ['stars', 'forks', 'stars_per_month']\n"
    "NUM_PLAIN  = ['open_issues']        # 中性计数,右对齐不着色\n"
    "BOUNDS = {c: (df[c].min(), df[c].max()) for c in SCORE_COLS}\n"
    "\n"
    "def score_bg(score):\n"
    "    \"\"\"score 为 0-10,返回红→黄→绿的 rgba 背景(套用规范公式)。\"\"\"\n"
    "    ratio = max(0.0, min(1.0, (score - 3) / 7))\n"
    "    if ratio < 0.5:\n"
    "        r, g, b = 220, int(60 + ratio * 2 * 180), 60          # 红→黄\n"
    "    else:\n"
    "        r = int(220 - (ratio - 0.5) * 2 * 180)\n"
    "        g = 200\n"
    "        b = int(60 + (ratio - 0.5) * 2 * 40)                  # 黄→绿\n"
    "    return f'background-color: rgba({r},{g},{b}, 0.35)'\n"
    "\n"
    "def to_score10(col, value):\n"
    "    \"\"\"把原始指标按列 min-max 归一到 0-10。\"\"\"\n"
    "    lo, hi = BOUNDS[col]\n"
    "    return 0.0 if hi == lo else (value - lo) / (hi - lo) * 10\n"
    "print(f'{TOTAL} 行已载入')"
))

# ── 单元2:完整数据表(分页 50 行/页,8-9px)──────────────────
cells.append(nbf.v4.new_code_cell(
    "PAGE = 50    # 每页行数(规范 50-80)\n"
    "DISPLAY_COLS = ['full_name', 'url', 'language', 'stars', 'forks',\n"
    "                'open_issues', 'stars_per_month']\n"
    "\n"
    "def render_full_page(frame, start, end, total):\n"
    "    th = ('background-color:#222;color:#fff;padding:3px 6px;'\n"
    "          'white-space:nowrap;text-align:left')\n"
    "    td = 'padding:2px 6px;white-space:nowrap;border-bottom:1px solid #eee'\n"
    "    out = [f'<h4>第 {start}-{end} / {total}</h4>',\n"
    "           '<table style=\"border-collapse:collapse;font-size:9px;'\n"
    "           'font-family:system-ui,Arial,sans-serif\">']\n"
    "    out.append('<tr><th style=\"' + th + '\">#</th>' +\n"
    "               ''.join(f'<th style=\"{th}\">{c}</th>' for c in DISPLAY_COLS) + '</tr>')\n"
    "    for rank, (_, row) in enumerate(frame.iterrows(), start=start):\n"
    "        cells = [f'<td style=\"{td};color:#888\">{rank}</td>']\n"
    "        for c in DISPLAY_COLS:\n"
    "            v = row[c]\n"
    "            if c == 'full_name':\n"
    "                cells.append(f'<td style=\"{td}\"><b>{v}</b></td>')\n"
    "            elif c == 'url':\n"
    "                cells.append(f'<td style=\"{td}\"><a href=\"{v}\">link</a></td>')\n"
    "            elif c in SCORE_COLS:\n"
    "                bg = score_bg(to_score10(c, v))\n"
    "                txt = f'{v:,.1f}' if c == 'stars_per_month' else f'{int(v):,}'\n"
    "                cells.append(f'<td style=\"{td};{bg};text-align:right\">{txt}</td>')\n"
    "            elif c in NUM_PLAIN:\n"
    "                cells.append(f'<td style=\"{td};text-align:right\">{int(v):,}</td>')\n"
    "            else:\n"
    "                cells.append(f'<td style=\"{td}\">{v}</td>')\n"
    "        out.append('<tr>' + ''.join(cells) + '</tr>')\n"
    "    out.append('</table>')\n"
    "    return '\\n'.join(out)\n"
    "\n"
    "html_pages = []\n"
    "for s in range(0, TOTAL, PAGE):\n"
    "    page = df.iloc[s:s + PAGE]\n"
    "    html_pages.append(render_full_page(page, s + 1, min(s + PAGE, TOTAL), TOTAL))\n"
    "display(HTML('<hr>'.join(html_pages)))"
))

# ── 单元3:排行榜(11px,Top 15)────────────────────────────
cells.append(nbf.v4.new_code_cell(
    "def render_ranking(frame, title):\n"
    "    th = ('background-color:#222;color:#fff;padding:6px 10px;'\n"
    "          'white-space:nowrap;text-align:left')\n"
    "    td = 'padding:4px 10px;white-space:nowrap;border-bottom:1px solid #eee'\n"
    "    cols = ['full_name', 'language', 'stars', 'stars_per_month', 'forks']\n"
    "    out = [f'<h3>{title}</h3>',\n"
    "           '<table style=\"border-collapse:collapse;font-size:11px;'\n"
    "           'font-family:system-ui,Arial,sans-serif\">']\n"
    "    out.append('<tr><th style=\"' + th + '\">#</th>' +\n"
    "               ''.join(f'<th style=\"{th}\">{c}</th>' for c in cols) + '</tr>')\n"
    "    for rank, (_, row) in enumerate(frame.iterrows(), start=1):\n"
    "        cells = [f'<td style=\"{td};color:#888\">{rank}</td>']\n"
    "        for c in cols:\n"
    "            v = row[c]\n"
    "            if c == 'full_name':\n"
    "                cells.append(f'<td style=\"{td}\"><b>{v}</b></td>')\n"
    "            elif c in SCORE_COLS:\n"
    "                bg = score_bg(to_score10(c, v))\n"
    "                txt = f'{v:,.1f}' if c == 'stars_per_month' else f'{int(v):,}'\n"
    "                cells.append(f'<td style=\"{td};{bg};text-align:right\">{txt}</td>')\n"
    "            else:\n"
    "                cells.append(f'<td style=\"{td}\">{v}</td>')\n"
    "        out.append('<tr>' + ''.join(cells) + '</tr>')\n"
    "    out.append('</table>')\n"
    "    return HTML('\\n'.join(out))\n"
    "\n"
    "top_stars = df.sort_values('stars', ascending=False).head(15)\n"
    "render_ranking(top_stars, '★ Stars 排行 Top 15')"
))

cells.append(nbf.v4.new_code_cell(
    "top_growth = df.sort_values('stars_per_month', ascending=False).head(15)\n"
    "render_ranking(top_growth, '📈 月均涨星 排行 Top 15')"
))

nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python'},
}

with open('godot_repos_matrix.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('wrote godot_repos_matrix.ipynb')
