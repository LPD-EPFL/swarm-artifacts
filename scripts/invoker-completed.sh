#!/bin/bash

set -e

SCRIPT_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )")"
source "$SCRIPT_DIR"/config.sh

WIN_NAME=$1

tmux capture-pane -t $TMUX_SESSION:${WIN_NAME} -pS -10 | grep -q "###DONE###"
