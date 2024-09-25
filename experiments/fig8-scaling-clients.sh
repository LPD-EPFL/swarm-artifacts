#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/../scripts )"

for OUTSTANDING in {4,1}; do
    for CLIENTS in {1,2,3,4,5,6,7,8,10,12,14,16,20,24,28,32,36,40,44,48,52,56,60,64}; do
        # # You can uncomment the lines bellow to also run with YCSB workload A
        # "$SCRIPT_DIR"/run.sh swarmkv fig8-scaling-clients/workload-A/a$OUTSTANDING/SWARM-KV/${CLIENTS}clients oops-workloada 2 $CLIENTS -m 2 -d=true -a $OUTSTANDING -T 0
        # "$SCRIPT_DIR"/run.sh swarmkv fig8-scaling-clients/workload-A/a$OUTSTANDING/DM-ABD/${CLIENTS}clients oops-workloada 2 $CLIENTS -m 2 -d=true -g=false --in_place=false -a $OUTSTANDING
        
        "$SCRIPT_DIR"/run.sh swarmkv fig8-scaling-clients/workload-B/${OUTSTANDING}parallelOps/SWARM-KV/${CLIENTS}clients oops-workloadb 2 $CLIENTS -m 2 -d=true -a $OUTSTANDING -T 0
        "$SCRIPT_DIR"/run.sh swarmkv fig8-scaling-clients/workload-B/${OUTSTANDING}parallelOps/DM-ABD/${CLIENTS}clients oops-workloadb 2 $CLIENTS -m 2 -d=true -g=false --in_place=false -a $OUTSTANDING
    done
done