#!/bin/bash
set -e

SCRIPT_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"

cd "$SCRIPT_DIR"

for i in {1..8}; do
  ssh w$i "cd swarm-artifacts; rm -rf logs.zip; zip -r logs.zip logs/"
  scp w$i:~/swarm-artifacts/logs.zip w$i-logs.zip
  unzip -o w$i-logs.zip
done
