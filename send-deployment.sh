#!/bin/bash
set -e

BASE_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"

cd "$BASE_DIR"

for i in {1..8}; do
  echo "Sending deployment to w$i"
  ssh w$i "mkdir -p \"$BASE_DIR\""
  scp deployment.zip w$i:"$BASE_DIR/deployment.zip"
  ssh w$i "unzip -o \"$BASE_DIR/deployment.zip\" -d \"$BASE_DIR\"; cd \"$BASE_DIR\"; tar -xf ycsb-0.12.0.tar.gz; rm -r YCSB/ 2> /dev/null;  mv ycsb-0.12.0 YCSB; cd bin; unzip -o bin.zip;"
done
