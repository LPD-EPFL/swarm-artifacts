#!/bin/bash
set -e

BASE_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"
PARENT_DIR="$( realpath -sm  "${BASE_DIR}/..")"

cd "$BASE_DIR"

for i in {1..8}; do
  ssh w$i "rm -r \"$PARENT_DIR/deployment.zip\" \"$BASE_DIR\"" | true
done
