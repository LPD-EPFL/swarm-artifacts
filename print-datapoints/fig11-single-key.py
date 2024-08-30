#!/usr/bin/env python3

import os
from logparser import parse

ptiles = [0.1] + list(range(1,100)) + [99.9]

workload = "workload-A"
for cc in [16]:
    # Uncomment to also display workload-B:
    # for workload in ["workload-A", "workload-B"]:
        print(f'{cc} clients (on {workload}):')

        for op in ['GET', 'UPDATE']:
            print(f'- {op}s:')

            for s in ['SWARM-KV', 'DM-ABD']:
                print(f'  - Latency percentiles of {op}s for {s}:')

                path = os.path.join('logs',
                    f'fig11-single-key/{workload}/{cc}clients/{s}/client1.txt',
                )
                data = parse(path)[op]

                for ptile in ptiles:
                    print(f'    - {ptile}%: {data[ptile]}μs')
print("This is for 16 clients as shown in the figure. If you want to print the datapoints for 32 clients, check the print-datapoints/extra directory.")
