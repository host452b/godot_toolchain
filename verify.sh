#!/usr/bin/env bash
# 验收:确认 5 个 topic 都真的采集成功且数据完整。任一检查失败 -> 退出码 1。
set -uo pipefail

TOPICS=(godot-engine godot4 godot godot-addon gdscript)
OUT_DIR="data/raw"
ERR_LOG="$OUT_DIR/errors.log"
DB="godot.db"
fail=0

red()  { printf "  \033[31m✗ %s\033[0m\n" "$1"; fail=1; }
green(){ printf "  \033[32m✓ %s\033[0m\n" "$1"; }

echo "== 检查 1:错误日志 =="
if [[ -s "$ERR_LOG" ]]; then
  red "errors.log 非空,采集中有 topic 失败:"; cat "$ERR_LOG"
else
  green "errors.log 为空"
fi

echo "== 检查 2:每个 topic 的 JSONL 存在且有数据 =="
for topic in "${TOPICS[@]}"; do
  f="$OUT_DIR/${topic}.jsonl"
  if [[ ! -f "$f" ]]; then
    red "$topic: JSONL 缺失 ($f)"
    continue
  fi
  n=$(wc -l < "$f" | tr -d ' ')
  if [[ "$n" -lt 1 ]]; then
    red "$topic: JSONL 为空(0 行)"
    continue
  fi
  if head -1 "$f" | jq -e '.fullName and .url and (.stargazersCount >= 1000)' >/dev/null 2>&1; then
    green "$topic: $n repos,字段与 star 阈值校验通过"
  else
    red "$topic: 首行 JSON 缺关键字段或 star<1000"
  fi
done

echo "== 检查 3:SQLite 表存在且 5 个 topic 都有数据 =="
if [[ ! -f "$DB" ]]; then
  red "$DB 不存在(未执行 load.py?)"
else
  for topic in "${TOPICS[@]}"; do
    c=$(sqlite3 "$DB" "SELECT COUNT(*) FROM repo_topics WHERE topic='$topic';" 2>/dev/null)
    if [[ "${c:-0}" -ge 1 ]]; then
      green "$topic: SQLite 中 $c 条 repo_topics"
    else
      red "$topic: SQLite 中无记录"
    fi
  done
  total=$(sqlite3 "$DB" "SELECT COUNT(*) FROM repos;" 2>/dev/null)
  echo "  repos 去重后总数:${total:-0}"
fi

echo
if [[ "$fail" -eq 0 ]]; then
  printf "\033[32m全部检查通过 ✅\033[0m\n"; exit 0
else
  printf "\033[31m有检查未通过 ❌\033[0m\n"; exit 1
fi
