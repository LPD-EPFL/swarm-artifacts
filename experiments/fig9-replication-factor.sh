#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/../scripts )"

for M in {2,3,4}; do
    REPLICAS=$((2 * $M - 1))
    # # You can uncomment the lines bellow to also run with YCSB workload A
    # "$SCRIPT_DIR"/run.sh swarmkv fig9-replication-factor/workload-A/SWARM-KV/${REPLICAS}replicas oops-workloada $M 4 -m $M -T 0 -d=true
    # "$SCRIPT_DIR"/run.sh swarmkv fig9-replication-factor/workload-A/DM-ABD/${REPLICAS}replicas oops-workloada $M 4 -m $M -d=true -g=false --in_place=false
    "$SCRIPT_DIR"/run.sh swarmkv fig9-replication-factor/workload-B/SWARM-KV/${REPLICAS}replicas oops-workloadb $M 4 -m $M -T 0 -d=true
    "$SCRIPT_DIR"/run.sh swarmkv fig9-replication-factor/workload-B/DM-ABD/${REPLICAS}replicas oops-workloadb $M 4 -m $M -d=true -g=false --in_place=false
done