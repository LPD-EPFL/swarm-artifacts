#!/bin/bash

set -u

EXP_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/ )"

"$EXP_DIR"/fig5-latency-cdf.sh
"$EXP_DIR"/fig6-limited-cache.sh
"$EXP_DIR"/fig7-tput-latency.sh
"$EXP_DIR"/fig8-scaling-clients.sh
"$EXP_DIR"/fig9-value-sizes.sh
"$EXP_DIR"/fig10-replication-factor.sh
"$EXP_DIR"/fig11-failure.sh
"$EXP_DIR"/fig12-single-key.sh
"$EXP_DIR"/fig13-metadata-buffers.sh
