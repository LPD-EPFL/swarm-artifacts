#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/../scripts )"

CLIENTS=64

for BUFS in {64,16,4,1}; do
    "$SCRIPT_DIR"/run.sh swarmkv fig13-metadata-buffers/workload-A/${CLIENTS}clients/${BUFS}buffers oops-workloada 2 $CLIENTS -m 2 -d=true -T ${BUFS}
    "$SCRIPT_DIR"/run.sh swarmkv fig13-metadata-buffers/workload-B/${CLIENTS}clients/${BUFS}buffers oops-workloadb 2 $CLIENTS -m 2 -d=true -T ${BUFS}
done