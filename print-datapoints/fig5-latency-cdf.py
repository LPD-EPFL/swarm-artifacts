#!/usr/bin/env python3

import os
from logparser import parse

schemes = {
    'RAW',
    'SWARM-KV',
    'DM-ABD',
    'FUSEE',
}

ops = [
    'GET',
    'UPDATE',
]

for workload in ["workload-B", "workload-A"]:
    print(f'{workload}:')

    ptiles = [0.1] + list(range(1,100)) + [99.9]

    for op in ops:
            print(f'  - Latency percentiles of {op}s:')
            for i, s in enumerate(schemes):
                    print(f'    - for {s}:')
                    path = os.path.join('logs',
                        f'fig5-latency-cdf/{workload}/{s}/client1.txt',
                    )
                    data = parse(path)[op]
                    for ptile in ptiles:
                        print(f'      - {ptile}%: {data[ptile]}μs')
