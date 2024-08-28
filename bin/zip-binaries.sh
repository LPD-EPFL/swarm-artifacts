#!/bin/bash
set -e

SCRIPT_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"

cd "$SCRIPT_DIR"

rm -rf bin.zip
zip -Dj bin.zip swarm-kv/{swarm-kv,fusee}/build/bin/*
