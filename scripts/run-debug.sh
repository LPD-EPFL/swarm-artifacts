#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )" )"
source "$SCRIPT_DIR"/config.sh

BINARY=$1
FOLDER=$2
WORKLOAD=$3
NBSERVERS=$4
NBCLIENTS=$5
ARGS="-y "$YCSB_BIN" -w "$WORKLOAD_DIR/$WORKLOAD" -s $NBSERVERS -c $NBCLIENTS ${@:6}"

echo "Debugging exp $FOLDER: $BINARY -w $WORKLOAD -s $NBSERVERS -c $NBCLIENTS ${@:6}"

"$SCRIPT_DIR"/setup-all-tmux.sh

echo -n "Starting"

"$SCRIPT_DIR"/remote-memc.sh $REGISTRY_MACHINE
sleep 0.1

for s in $(seq 1 $NBSERVERS); do
  echo -n "."
  MACHINE=machine$(($FIRST_SERVER + ($s - 1) % $SERVER_MACHINES))
  CORE=$(((($s - 1) / $SERVER_MACHINES) * 2))
  "$SCRIPT_DIR"/remote-invoker.sh $MACHINE "$FOLDER" server$s $CORE "$BIN_DIR/$BINARY" -i $s $ARGS
done

echo "Run: "
for c in $(seq 1 $NBCLIENTS); do
  MACHINE=machine$(($FIRST_CLIENT + ($c - 1) % $CLIENT_MACHINES))
  CORE=$(((($c - 1) / $CLIENT_MACHINES) * 2))
  i=$((c + $NBSERVERS))
  # "$SCRIPT_DIR"/remote-invoker.sh $MACHINE "$FOLDER" client$c $CORE "$BIN_DIR/$BINARY" -i $i $ARGS
  echo "On $MACHINE: source \"$SCRIPT_DIR\"/config.sh; numactl -m 0 -N 0 -C $CORE gdb --args $BIN_DIR/$BINARY $ARGS -i $i"
done
# echo " ✓"
echo "✓"

# c=1
# c=$NBCLIENTS
# CORE=$(((($c - 1) / $CLIENT_MACHINES) * 2))
# i=$((c + $NBSERVERS))