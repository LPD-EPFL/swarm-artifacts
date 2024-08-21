#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/../scripts )"

for OUTSTANDING in {1,2,3,4,5,6,7,8}; do
    "$SCRIPT_DIR"/run.sh swarmkv fig6-tput-latency/workload-A/SWARM-KV/${OUTSTANDING}parallelOps oops-workloada 2 4 -m 2 -d=true -a $OUTSTANDING -T 0
    "$SCRIPT_DIR"/run.sh swarmkv fig6-tput-latency/workload-B/SWARM-KV/${OUTSTANDING}parallelOps oops-workloadb 2 4 -m 2 -d=true -a $OUTSTANDING -T 0
    "$SCRIPT_DIR"/run.sh swarmkv fig6-tput-latency/workload-A/DM-ABD/${OUTSTANDING}parallelOps oops-workloada 2 4 -m 2 -d=true -g=false --in_place=false -a $OUTSTANDING
    "$SCRIPT_DIR"/run.sh swarmkv fig6-tput-latency/workload-B/DM-ABD/${OUTSTANDING}parallelOps oops-workloadb 2 4 -m 2 -d=true -g=false --in_place=false -a $OUTSTANDING
done