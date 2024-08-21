#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/../scripts )"


for CLIENTS in {16,32}; do
    "$SCRIPT_DIR"/run.sh swarmkv fig11-single-key/workload-A/${CLIENTS}clients/SWARM-KV oops-workloada-singlekey 2 $CLIENTS -m 2 -d=true -I 200000 -T 0
    "$SCRIPT_DIR"/run.sh swarmkv fig11-single-key/workload-A/${CLIENTS}clients/DM-ABD oops-workloada-singlekey 2 $CLIENTS -m 2 -d=true -I 200000 -g=false --in_place=false
    
    # # You can uncomment the lines bellow to also run with YCSB workload B
    # "$SCRIPT_DIR"/run.sh swarmkv fig11-single-key/workload-B/${CLIENTS}clients/SWARM-KV oops-workloada-singlekey 2 $CLIENTS -m 2 -d=true -I 200000 -T 0
    # "$SCRIPT_DIR"/run.sh swarmkv fig11-single-key/workload-B/${CLIENTS}clients/DM-ABD oops-workloada-singlekey 2 $CLIENTS -m 2 -d=true -I 200000 -g=false --in_place=false
done