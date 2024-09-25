#!/bin/bash

set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/../scripts )"

"$SCRIPT_DIR"/run.sh swarmkv fig6-limited-cache/5MiB/workload-A/SWARM-KV oops-workloada-1M-keys 2 4 -n 1000000 -W 8000000 -t 5120 -m 2 -T 0 -d=true
"$SCRIPT_DIR"/run.sh swarmkv fig6-limited-cache/5MiB/workload-B/SWARM-KV oops-workloadb-1M-keys 2 4 -n 1000000 -W 8000000 -t 5120 -m 2 -T 0 -d=true
"$SCRIPT_DIR"/run.sh swarmkv fig6-limited-cache/5MiB/workload-A/DM-ABD oops-workloada-1M-keys 2 4 -n 1000000 -W 8000000 -t 5120 -m 2 -d=true -g=false --in_place=false
"$SCRIPT_DIR"/run.sh swarmkv fig6-limited-cache/5MiB/workload-B/DM-ABD oops-workloadb-1M-keys 2 4 -n 1000000 -W 8000000 -t 5120 -m 2 -d=true -g=false --in_place=false
"$SCRIPT_DIR"/run.sh fusee fig6-limited-cache/5MiB/workload-A/FUSEE oops-workloada-1M-keys 2 4 -n 1000000 -W 8000000 -t 5120
"$SCRIPT_DIR"/run.sh fusee fig6-limited-cache/5MiB/workload-B/FUSEE oops-workloadb-1M-keys 2 4 -n 1000000 -W 8000000 -t 5120

"$SCRIPT_DIR"/run.sh swarmkv fig6-limited-cache/10MiB/workload-A/SWARM-KV oops-workloada-1M-keys 2 4 -n 1000000 -W 8000000 -t 10240 -m 2 -T 0 -d=true
"$SCRIPT_DIR"/run.sh swarmkv fig6-limited-cache/10MiB/workload-B/SWARM-KV oops-workloadb-1M-keys 2 4 -n 1000000 -W 8000000 -t 10240 -m 2 -T 0 -d=true
"$SCRIPT_DIR"/run.sh swarmkv fig6-limited-cache/10MiB/workload-A/DM-ABD oops-workloada-1M-keys 2 4 -n 1000000 -W 8000000 -t 10240 -m 2 -d=true -g=false --in_place=false
"$SCRIPT_DIR"/run.sh swarmkv fig6-limited-cache/10MiB/workload-B/DM-ABD oops-workloadb-1M-keys 2 4 -n 1000000 -W 8000000 -t 10240 -m 2 -d=true -g=false --in_place=false
"$SCRIPT_DIR"/run.sh fusee fig6-limited-cache/10MiB/workload-A/FUSEE oops-workloada-1M-keys 2 4 -n 1000000 -W 8000000 -t 10240
"$SCRIPT_DIR"/run.sh fusee fig6-limited-cache/10MiB/workload-B/FUSEE oops-workloadb-1M-keys 2 4 -n 1000000 -W 8000000 -t 10240
