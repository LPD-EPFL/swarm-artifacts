#!/usr/bin/env python3

import os
from logparser import parse

client_counts = list(range(1,9)) + [10, 12, 14] + list(range(16, 68, 4))
workload = "workload-B"

print(f'(with {workload})')

for p, pname  in zip([1, 4], ["sequential", "4 parallel operations"]):
    print(f'{pname}:')

    for s in ['SWARM-KV','DM-ABD']:
        print(f'- {s}:')

        for cc in client_counts:
            getavg = 0
            updavg = 0
            tputavg = 0
            for c in range(1, cc+1):
                path = os.path.join('logs',
                    f'fig8-scaling-clients/{workload}/{p}parallelOps/{s}/{cc}clients/client{c}.txt',
                )
                data = parse(path)
                getavg += data['GET']['psum'] / (cc * data['GET']['pcount'])
                updavg += data['UPDATE']['psum'] / (cc * data['UPDATE']['pcount'])
                tputavg += data['local tput']
            # opavg = ((getavg + updavg) / 2) if workload == "workload-A" else (getavg * 0.95 + updavg * 0.05)
            print(f'  - with {cc} clients -> GETs average latency: {round(getavg, 3)}μs, UPDATEs average latency: {round(updavg, 3)}μs, throuput: {round(tputavg / 1000, 2)}Mops')
