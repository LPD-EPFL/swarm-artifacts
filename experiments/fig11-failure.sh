#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/../scripts )"

"$SCRIPT_DIR"/run.sh swarmkv fig11-failure/workload-A/crash oops-workloada-op6000000 3 4 -m 2 -T 0 -d=true -l=5000000 -I=4000000 -B=true -D=6500000000

# # You can uncomment the lines bellow to also run with YCSB workload B
# "$SCRIPT_DIR"/run.sh swarmkv fig11-failure/workload-B/crash oops-workloadb-op6000000 3 4 -m 2 -T 0 -d=true -l=5000000 -I=4000000 -B=true -D=5000000000