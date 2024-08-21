#!/bin/bash
set -e

SCRIPT_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"

cd "$SCRIPT_DIR"

for i in {1..8}; do
  ssh w$i "rm -r deployment.zip swarm-artifacts" | true
done
