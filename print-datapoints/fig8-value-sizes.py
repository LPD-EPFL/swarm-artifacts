#!/usr/bin/env python3

import os
from logparser import parse

client_counts = list(range(1,9)) + [10, 12, 14] + list(range(16, 68, 4))
vsizes = [2**i for i in range(4,14)]

for workload in ["workload-A", "workload-B"]:
    print(f'{workload}:')

    for s in ['In-n-Out','Out-P']:
        print(f'- {s}:')

        for vsize in vsizes:
            getavg = 0
            updavg = 0
            tputavg = 0
            for c in range(1, 5):
                path = os.path.join('logs',
                    f'fig8-value-sizes/{workload}/SWARM-KV/{s}/values-of-{vsize}B/client{c}.txt',
                )
                data = parse(path)
                getavg += data['GET']['psum'] / (4 * data['GET']['pcount'])
                updavg += data['UPDATE']['psum'] / (4 * data['UPDATE']['pcount'])
                tputavg += data['local tput']
            # opavg = ((getavg + updavg) / 2) if workload == "workload-A" else (getavg * 0.95 + updavg * 0.05)
            print(f'  - values of {vsize}B -> GETs average latency: {round(getavg, 3)}μs, UPDATEs average latency: {round(updavg, 3)}μs, throughput: {round(tputavg / 1000, 2)}Mops')
