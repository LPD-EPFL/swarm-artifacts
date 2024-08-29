#!/usr/bin/env python3

import os
from logparser import parse

for workload in ["workload-A", "workload-B"]:
    print(f'{workload}:')

    for s in ['SWARM-KV','DM-ABD']:
        print(f'- {s}:')

        for p in range(1,9):
            getavg = 0
            updavg = 0
            tputavg = 0
            for c in range(1,5):
                path = os.path.join('logs',
                    f'fig6-tput-latency/{workload}/{s}/{p}parallelOps/client{c}.txt',
                )
                data = parse(path)
                getavg += data['GET']['psum'] / (4 * data['GET']['pcount'])
                updavg += data['UPDATE']['psum'] / (4 * data['UPDATE']['pcount'])
                tputavg += data['local tput'] / 4
            opavg = ((getavg + updavg) / 2) if workload == "workload-A" else (getavg * 0.95 + updavg * 0.05)
            print(f'  - with {p} parallel operations -> average latency: {round(opavg, 3)}μs throuput: {round(tputavg, 2)}kops')
