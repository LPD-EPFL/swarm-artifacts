#!/bin/bash

set -e

SCRIPT_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"
source "$SCRIPT_DIR"/config.sh

cd $ROOT_DIR
zip -ru logs.zip logs/
scp logs.zip gateway:zyf/oops-graphs/
ssh gateway "cd zyf/oops-graphs; unzip -uo logs.zip"