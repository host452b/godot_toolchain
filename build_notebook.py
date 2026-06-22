"""生成 godot_repos_matrix.ipynb:从 godot.db 读数据,渲染 inline-style 颜色矩阵。

关键:用每个 <td> 的 inline style="background-color:rgba(...)" 着色,
不用 <style> 块 —— 这样 GitHub 在线查看 .ipynb 时颜色不会被剥掉。
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell(
    "# Godot 生态仓库 · 颜色矩阵\n"
    "\n"
    "数据来自本仓库 `godot.db`(5 个 topic、`star ≥ 1000`、最近 3 个月有推送,去重后 51 个仓库)。\n"
    "\n"
    "矩阵维度:**full_name / url / stars / forks / open_issues / 月均新增 star**。\n"
    "\n"
    "> 月均新增 star = `stars ÷ 从创建到最后更新的月数`,衡量仓库历史上的平均涨星速度。\n"
    "> 数值列按列做热力着色;着色用每个单元格的 inline 样式,**GitHub 在线查看即可看到颜色**。"
))

# 单元1:加载 + 计算
cells.append(nbf.v4.new_code_cell(
    "import sqlite3\n"
    "import pandas as pd\n"
    "import matplotlib\n"
    "from IPython.display import HTML\n"
    "\n"
    "conn = sqlite3.connect('godot.db')\n"
    "df = pd.read_sql_query(\n"
    "    'SELECT full_name, url, stars, forks, open_issues, created_at, updated_at FROM repos',\n"
    "    conn,\n"
    ")\n"
    "conn.close()\n"
    "\n"
    "# 月均新增 star = stars / 从创建到最后更新的月数(至少按 1 个月计,避免除零)\n"
    "created = pd.to_datetime(df['created_at'], utc=True)\n"
    "updated = pd.to_datetime(df['updated_at'], utc=True)\n"
    "active_months = ((updated - created).dt.days / 30.44).clip(lower=1.0)\n"
    "df['stars_per_month'] = (df['stars'] / active_months).round(1)\n"
    "df = (df.drop(columns=['created_at', 'updated_at'])\n"
    "        .sort_values('stars', ascending=False)\n"
    "        .reset_index(drop=True))\n"
    "len(df)"
))

# 单元2:inline-style 着色 HTML 生成函数
cells.append(nbf.v4.new_code_cell(
    "# 把数值按列归一化映射到 colormap,生成 inline background-color(rgba,半透明保证文字可读)\n"
    "NUM_COLS = {\n"
    "    'stars': 'YlGnBu',\n"
    "    'forks': 'OrRd',\n"
    "    'open_issues': 'Purples',\n"
    "    'stars_per_month': 'Greens',\n"
    "}\n"
    "ALPHA = 0.45\n"
    "\n"
    "def _cell_bg(value, vmin, vmax, cmap_name):\n"
    "    if vmax == vmin:\n"
    "        t = 0.0\n"
    "    else:\n"
    "        t = (value - vmin) / (vmax - vmin)\n"
    "    r, g, b, _ = matplotlib.colormaps[cmap_name](t)\n"
    "    return f'rgba({int(r*255)},{int(g*255)},{int(b*255)},{ALPHA})'\n"
    "\n"
    "def render_matrix(frame, caption):\n"
    "    bounds = {c: (frame[c].min(), frame[c].max()) for c in NUM_COLS if c in frame.columns}\n"
    "    head_style = ('background-color:#222;color:#fff;padding:6px 10px;'\n"
    "                  'text-align:left;position:sticky;top:0')\n"
    "    html = [f'<table style=\"border-collapse:collapse;font-family:system-ui,Arial,sans-serif;'\n"
    "            f'font-size:13px\"><caption style=\"font-size:16px;font-weight:bold;'\n"
    "            f'padding:8px;text-align:left\">{caption}</caption>']\n"
    "    # 表头\n"
    "    html.append('<tr>' + ''.join(\n"
    "        f'<th style=\"{head_style}\">{col}</th>' for col in frame.columns) + '</tr>')\n"
    "    # 数据行\n"
    "    for _, row in frame.iterrows():\n"
    "        cells_html = []\n"
    "        for col in frame.columns:\n"
    "            v = row[col]\n"
    "            base = 'padding:4px 10px;border-bottom:1px solid #eee'\n"
    "            if col == 'full_name':\n"
    "                cells_html.append(f'<td style=\"{base};font-weight:bold\">{v}</td>')\n"
    "            elif col == 'url':\n"
    "                cells_html.append(\n"
    "                    f'<td style=\"{base}\"><a href=\"{v}\" target=\"_blank\">link</a></td>')\n"
    "            elif col in NUM_COLS:\n"
    "                vmin, vmax = bounds[col]\n"
    "                bg = _cell_bg(v, vmin, vmax, NUM_COLS[col])\n"
    "                txt = f'{v:,.1f}' if col == 'stars_per_month' else f'{int(v):,}'\n"
    "                cells_html.append(\n"
    "                    f'<td style=\"{base};background-color:{bg};text-align:right\">{txt}</td>')\n"
    "            else:\n"
    "                cells_html.append(f'<td style=\"{base}\">{v}</td>')\n"
    "        html.append('<tr>' + ''.join(cells_html) + '</tr>')\n"
    "    html.append('</table>')\n"
    "    return HTML('\\n'.join(html))\n"
    "\n"
    "render_matrix(df, 'Godot 生态仓库颜色矩阵 — 按 stars 降序')"
))

cells.append(nbf.v4.new_markdown_cell(
    "## 维度速览\n"
    "\n"
    "- **stars / forks / open_issues**:GitHub 即时指标,采集时快照。\n"
    "- **stars_per_month(月均新增 star)**:用 `stars` 除以「创建→最后更新」跨度的月数,"
    "近似该仓库生命周期内的平均涨星速度。注意这是历史平均,不等于当前热度——"
    "老牌项目即便现在仍火,均值也会被早期低速期摊薄;新项目则可能偏高。"
))

cells.append(nbf.v4.new_code_cell(
    "# 月均涨星 Top 15(换个角度看“增长效率”而非绝对体量)\n"
    "top_growth = (df.sort_values('stars_per_month', ascending=False)\n"
    "                .head(15)\n"
    "                [['full_name', 'url', 'stars', 'stars_per_month']]\n"
    "                .reset_index(drop=True))\n"
    "render_matrix(top_growth, '月均新增 star Top 15')"
))

nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python'},
}

with open('godot_repos_matrix.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('wrote godot_repos_matrix.ipynb')
