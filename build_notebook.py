"""生成 godot_repos_matrix.ipynb:从 godot.db 读全部仓库,渲染一张完整数据表,红绿色阶。

形式参考 best-of-everything.consensus/shanghai-housing/shanghai_communities.ipynb:
- 一张完整数据表(全部记录,不分页/不截断)
- 数值列红绿色阶(RdYlGn:低=红、高=绿)
- 着色用每个 <td> 的 inline style="background-color:rgba(...)",不用 <style> 块,
  这样 GitHub 在线查看 .ipynb 时颜色不会被剥掉。
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell(
    "# Godot 生态仓库 · 完整数据表(红绿色阶)\n"
    "\n"
    "数据来自本仓库 `godot.db`(5 个 topic、`star ≥ 1000`、最近 3 个月有推送,去重后 **51 个仓库**,全部列出)。\n"
    "\n"
    "维度:**full_name / url / stars / forks / open_issues / 月均新增 star**。\n"
    "\n"
    "> 月均新增 star = `stars ÷ 从创建到最后更新的月数`,衡量仓库历史上的平均涨星速度。\n"
    "> 数值列按列做**红绿色阶**(RdYlGn:同列内越低越红、越高越绿)。\n"
    "> 着色用每个单元格的 inline 样式,**GitHub 在线查看即可看到颜色**。"
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
    "print(f'{len(df)} 个仓库')\n"
    "df.head()"
))

# 单元2:红绿色阶 + inline-style HTML 渲染
cells.append(nbf.v4.new_code_cell(
    "# 数值列统一红绿色阶(RdYlGn):同列内归一化,低=红、高=绿\n"
    "NUM_COLS = ['stars', 'forks', 'open_issues', 'stars_per_month']\n"
    "CMAP = matplotlib.colormaps['RdYlGn']\n"
    "ALPHA = 0.55\n"
    "\n"
    "def _cell_bg(value, vmin, vmax):\n"
    "    t = 0.0 if vmax == vmin else (value - vmin) / (vmax - vmin)\n"
    "    r, g, b, _ = CMAP(t)\n"
    "    return f'rgba({int(r*255)},{int(g*255)},{int(b*255)},{ALPHA})'\n"
    "\n"
    "def render_table(frame, caption):\n"
    "    bounds = {c: (frame[c].min(), frame[c].max()) for c in NUM_COLS if c in frame.columns}\n"
    "    head_style = ('background-color:#222;color:#fff;padding:6px 10px;'\n"
    "                  'text-align:left;position:sticky;top:0')\n"
    "    html = [f'<table style=\"border-collapse:collapse;font-family:system-ui,Arial,sans-serif;'\n"
    "            f'font-size:13px\"><caption style=\"font-size:16px;font-weight:bold;'\n"
    "            f'padding:8px;text-align:left\">{caption}</caption>']\n"
    "    html.append('<tr><th style=\"' + head_style + '\">#</th>' + ''.join(\n"
    "        f'<th style=\"{head_style}\">{col}</th>' for col in frame.columns) + '</tr>')\n"
    "    for rank, (_, row) in enumerate(frame.iterrows(), start=1):\n"
    "        base = 'padding:4px 10px;border-bottom:1px solid #eee'\n"
    "        cells_html = [f'<td style=\"{base};color:#888\">{rank}</td>']\n"
    "        for col in frame.columns:\n"
    "            v = row[col]\n"
    "            if col == 'full_name':\n"
    "                cells_html.append(f'<td style=\"{base};font-weight:bold\">{v}</td>')\n"
    "            elif col == 'url':\n"
    "                cells_html.append(\n"
    "                    f'<td style=\"{base}\"><a href=\"{v}\" target=\"_blank\">link</a></td>')\n"
    "            elif col in NUM_COLS:\n"
    "                vmin, vmax = bounds[col]\n"
    "                bg = _cell_bg(v, vmin, vmax)\n"
    "                txt = f'{v:,.1f}' if col == 'stars_per_month' else f'{int(v):,}'\n"
    "                cells_html.append(\n"
    "                    f'<td style=\"{base};background-color:{bg};text-align:right\">{txt}</td>')\n"
    "            else:\n"
    "                cells_html.append(f'<td style=\"{base}\">{v}</td>')\n"
    "        html.append('<tr>' + ''.join(cells_html) + '</tr>')\n"
    "    html.append('</table>')\n"
    "    return HTML('\\n'.join(html))\n"
    "\n"
    "# 完整数据表:全部 51 个仓库,按 stars 降序\n"
    "render_table(df, f'Godot 生态完整数据表 — 共 {len(df)} 个仓库,数值列红绿色阶')"
))

nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python'},
}

with open('godot_repos_matrix.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('wrote godot_repos_matrix.ipynb')
