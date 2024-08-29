#!/bin/bash
set -e

BASE_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"

for i in {1..8}; do
  ssh w$i "rm -r \"$BASE_DIR\"" | true
done
