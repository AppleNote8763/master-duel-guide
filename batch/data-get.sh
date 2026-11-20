#!/usr/bin/env bash
# 결과 전용 브랜치(data)의 내용을 ./databr 로 받는다. 브랜치가 없으면 빈 폴더를 만든다.
set -u
URL="https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
rm -rf databr
git clone -q --depth 1 --branch data "$URL" databr 2>/dev/null || mkdir -p databr
mkdir -p databr/batch
ls databr/batch | wc -l
