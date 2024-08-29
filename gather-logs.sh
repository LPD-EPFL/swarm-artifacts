#!/bin/bash
set -e

BASE_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"

cd "$BASE_DIR"

for i in {1..8}; do
  ssh w$i "cd \"$BASE_DIR\"; rm -rf logs.zip; zip -r logs.zip logs/"
  scp w$i:"$BASE_DIR/logs.zip" w$i-logs.zip
  unzip -o w$i-logs.zip
  rm -rf w?-logs.zip
done
