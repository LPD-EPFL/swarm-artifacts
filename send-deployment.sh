#!/bin/bash
set -e

SCRIPT_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"

cd "$SCRIPT_DIR"

for i in {1..8}; do
  echo "Sending deployment to w$i"
  scp deployment.zip w$i:~
  ssh w$i "unzip -o deployment.zip -d swarm-artifacts; cd swarm-artifacts; tar -xf ycsb-0.12.0.tar.gz; mv ycsb-0.12.0 YCSB; cd bin; unzip -o bin.zip;"
done
