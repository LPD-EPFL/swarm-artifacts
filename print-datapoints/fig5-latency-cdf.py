#!/usr/bin/env python3

import os
from logparser import parse

ptiles = [0.1] + list(range(1,100)) + [99.9]

for workload in ["workload-A", "workload-B"]:
    print(f'{workload}:')

    for op in ['GET', 'UPDATE']:
        print(f'- {op}s:')

        for s in ['RAW', 'SWARM-KV', 'DM-ABD', 'FUSEE']:
            print(f'  - Latency percentiles of {op}s for {s}:')

            path = os.path.join('logs',
                f'fig5-latency-cdf/{workload}/{s}/client1.txt',
            )
            data = parse(path)[op]

            for ptile in ptiles:
                print(f'    - {ptile}%: {data[ptile]}μs')
print("Note that the graph only shows the experiment on workload-B")