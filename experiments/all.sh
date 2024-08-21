#!/bin/bash

set -u

EXP_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )"/ )"

#"$EXP_DIR"/fig10-failure.sh
#"$EXP_DIR"/fig11-single-key.sh
"$EXP_DIR"/fig12-metadata-buffers.sh
#"$EXP_DIR"/fig5-latency-cdf.sh
"$EXP_DIR"/fig6-tput-latency.sh
"$EXP_DIR"/fig7-scaling-clients.sh
"$EXP_DIR"/fig8-value-sizes.sh
"$EXP_DIR"/fig9-replication-factor.sh
