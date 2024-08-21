#!/bin/bash
set -e

BASE_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"

cd "$BASE_DIR"

for i in {1..8}; do
  ssh w$i "rm -r deployment.zip \"$BASE_DIR\"" | true
done
