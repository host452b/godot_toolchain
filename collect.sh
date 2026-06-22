#!/usr/bin/env bash
# 阶段 A:遍历 Godot topic,采集 star>=1000 且最近 3 个月有 push 的 repo 基础元数据。
# 不去重:每个 topic 各自落盘 data/raw/<topic>.jsonl。
set -uo pipefail

TOPICS=(godot-engine godot4 godot godot-addon gdscript)
OUT_DIR="data/raw"
ERR_LOG="$OUT_DIR/errors.log"
CUTOFF=$(date -v-3m +%Y-%m-%d)   # macOS:今天往前推 3 个月
FIELDS="fullName,name,owner,description,url,homepage,stargazersCount,forksCount,openIssuesCount,language,license,isArchived,isFork,isDisabled,defaultBranch,size,createdAt,updatedAt,pushedAt"

mkdir -p "$OUT_DIR"
: > "$ERR_LOG"   # 清空错误日志

echo "活跃截止日(pushed >=): $CUTOFF"

for topic in "${TOPICS[@]}"; do
  out="$OUT_DIR/${topic}.jsonl"
  echo "==> 采集 topic: $topic"
  if gh search repos "pushed:>=$CUTOFF" \
       --topic "$topic" \
       --stars '>=1000' \
       --sort stars --order desc \
       --limit 1000 \
       --json "$FIELDS" \
     | jq -c '.[]' > "$out"; then
    count=$(wc -l < "$out" | tr -d ' ')
    echo "    OK: $count repos -> $out"
  else
    echo "$(date '+%Y-%m-%dT%H:%M:%S') FAILED topic=$topic" >> "$ERR_LOG"
    echo "    FAILED: 见 $ERR_LOG,继续下一个"
  fi
done

echo "采集完成。"
