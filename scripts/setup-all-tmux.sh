#!/bin/bash

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )" )"
source "$SCRIPT_DIR"/config.sh

echo -n "Setup $MACHINE_COUNT $TMUX_SESSION tmux"
for i in $(seq $FIRST_MACHINE $(($FIRST_MACHINE + $MACHINE_COUNT - 1))); do
    echo -n "."
    MACHINE=$(machine2ssh machine$i)
    ssh -o LogLevel=QUIET -t $MACHINE \
        "tmux kill-session -t $TMUX_SESSION 2> /dev/null; \
         tmux new-session -d -s $TMUX_SESSION && \
         tmux set-option -g remain-on-exit on"
    # echo "Setup tmux session $TMUX_SESSION for $MACHINE"
done
echo " ✓"
