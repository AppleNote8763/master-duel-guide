#!/usr/bin/env bash
# 결과 전용 브랜치(data)를 갱신한다. 기록을 남기지 않도록 매번 커밋 하나짜리로 덮어쓴다.
#   data-put.sh <명령...>   : ./pub/batch 를 고치는 명령을 받아 실행한 뒤 올린다. 그 사이 다른 작업이 먼저 올렸으면 처음부터 다시 한다.
set -u
URL="https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
for i in 1 2 3 4 5; do
  rm -rf pub
  old=""
  if git clone -q --depth 1 --branch data "$URL" pub 2>/dev/null; then old=$(git -C pub rev-parse HEAD); else mkdir -p pub && git -C pub init -q && git -C pub remote add origin "$URL"; fi
  mkdir -p pub/batch
  "$@" || exit 1
  cd pub
  git config user.name "github-actions[bot]"; git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
  git checkout -q --orphan fresh
  git add -A
  git commit -qm "일괄 계산 결과 ($(date -u +%Y-%m-%dT%H:%MZ))"
  if [ -n "$old" ]; then git push -q --force-with-lease=data:"$old" origin HEAD:data && exit 0; else git push -q origin HEAD:data && exit 0; fi
  cd ..; echo "다른 작업이 먼저 올림, 다시 시도 ($i)"; sleep $((RANDOM % 10 + 5))
done
exit 1
