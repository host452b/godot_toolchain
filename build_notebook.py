"""生成 godot_repos_matrix.ipynb:从 godot.db 读数据,渲染颜色矩阵。
仅用于构建 notebook;notebook 本身自包含,不依赖本文件。"""
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
    "数值列按列做热力着色(颜色越深 = 数值越高)。"
))

cells.append(nbf.v4.new_code_cell(
    "import sqlite3\n"
    "import pandas as pd\n"
    "\n"
    "conn = sqlite3.connect('godot.db')\n"
    "df = pd.read_sql_query(\n"
    "    'SELECT full_name, url, stars, forks, open_issues, created_at, updated_at FROM repos',\n"
    "    conn,\n"
    ")\n"
    "conn.close()\n"
    "len(df)"
))

cells.append(nbf.v4.new_code_cell(
    "# 月均新增 star = stars / 从创建到最后更新的月数(至少按 1 个月计,避免除零)\n"
    "created = pd.to_datetime(df['created_at'], utc=True)\n"
    "updated = pd.to_datetime(df['updated_at'], utc=True)\n"
    "active_months = ((updated - created).dt.days / 30.44).clip(lower=1.0)\n"
    "df['stars_per_month'] = (df['stars'] / active_months).round(1)\n"
    "df = df.drop(columns=['created_at', 'updated_at'])\n"
    "df = df.sort_values('stars', ascending=False).reset_index(drop=True)\n"
    "df.head()"
))

cells.append(nbf.v4.new_code_cell(
    "# 颜色矩阵:数值列逐列热力着色;url 渲染为可点击链接\n"
    "num_cols = ['stars', 'forks', 'open_issues', 'stars_per_month']\n"
    "\n"
    "styled = (\n"
    "    df.style\n"
    "      .background_gradient(cmap='YlGnBu', subset=['stars'])\n"
    "      .background_gradient(cmap='OrRd', subset=['forks'])\n"
    "      .background_gradient(cmap='Purples', subset=['open_issues'])\n"
    "      .background_gradient(cmap='Greens', subset=['stars_per_month'])\n"
    "      .format({'stars': '{:,}', 'forks': '{:,}', 'open_issues': '{:,}',\n"
    "               'stars_per_month': '{:.1f}'})\n"
    "      .format({'url': lambda u: f'<a href=\"{u}\" target=\"_blank\">link</a>'})\n"
    "      .set_caption('Godot 生态仓库颜色矩阵 — 按 stars 降序')\n"
    "      .set_properties(subset=['full_name'], **{'text-align': 'left',\n"
    "                                               'font-weight': 'bold'})\n"
    "      .set_table_styles([\n"
    "          {'selector': 'caption',\n"
    "           'props': [('font-size', '16px'), ('font-weight', 'bold'),\n"
    "                     ('padding', '8px')]},\n"
    "          {'selector': 'th',\n"
    "           'props': [('background-color', '#222'), ('color', 'white'),\n"
    "                     ('padding', '6px 10px')]},\n"
    "          {'selector': 'td', 'props': [('padding', '4px 10px')]},\n"
    "      ])\n"
    ")\n"
    "styled"
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
    "top_growth = df.sort_values('stars_per_month', ascending=False).head(15).reset_index(drop=True)\n"
    "(top_growth[['full_name', 'stars', 'stars_per_month']]\n"
    "    .style\n"
    "    .background_gradient(cmap='Greens', subset=['stars_per_month'])\n"
    "    .format({'stars': '{:,}', 'stars_per_month': '{:.1f}'})\n"
    "    .set_caption('月均新增 star Top 15'))"
))

nb['cells'] = cells
nb['metadata'] = {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python'},
}

with open('godot_repos_matrix.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('wrote godot_repos_matrix.ipynb')
