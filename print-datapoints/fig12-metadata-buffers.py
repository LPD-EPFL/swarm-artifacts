#!/usr/bin/env python3

import os
from logparser import parse

ptiles = [0.1] + list(range(1,100)) + [99.9]

# workload = "workload-B"
for workload in ["workload-B"]:
    print(f'{workload}:')
    for op in ['GET', 'UPDATE']:
        print(f'- {op}s:')
        # Uncomment to also display workload-A:

        for bufs in [1,4,16,64]:
            print(f'  - Latency percentiles of {op}s with {bufs} buffers:')

            path = os.path.join('logs',
                f'fig12-metadata-buffers/{workload}/64clients/{bufs}buffers/client1.txt',
            )
            data = parse(path)[op]

            for ptile in ptiles:
                print(f'    - {ptile}%: {data[ptile]}μs')
print("This is for workload-B as shown in the figure. If you want to print the datapoints for workload-A, check the print-datapoints/extra directory.")
