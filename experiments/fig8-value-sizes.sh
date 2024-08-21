#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/../scripts )"

for SIZE in {16,32,64,128,256,512,1024,2048,4096,8192}; do
    "$SCRIPT_DIR"/run.sh swarmkv fig8-value-sizes/workload-A/SWARM-KV/In-n-Out/values-of-${SIZE}B oops-workloada-$SIZE 2 4 -m 2 -T 0 -d=true -v $SIZE
    "$SCRIPT_DIR"/run.sh swarmkv fig8-value-sizes/workload-B/SWARM-KV/In-n-Out/values-of-${SIZE}B oops-workloadb-$SIZE 2 4 -m 2 -T 0 -d=true -v $SIZE
    "$SCRIPT_DIR"/run.sh swarmkv fig8-value-sizes/workload-A/SWARM-KV/Out-P/values-of-${SIZE}B oops-workloada-$SIZE 2 4 -m 2 -T 0 --in_place=false -d=true -v $SIZE
    "$SCRIPT_DIR"/run.sh swarmkv fig8-value-sizes/workload-B/SWARM-KV/Out-P/values-of-${SIZE}B oops-workloadb-$SIZE 2 4 -m 2 -T 0 --in_place=false -d=true -v $SIZE
done