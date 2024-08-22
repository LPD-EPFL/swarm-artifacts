#!/usr/bin/env python3

import os
from logparser import parse

client_counts = list(range(1,9)) + [10, 12, 14] + list(range(16, 68, 4))
vsizes = [2**i for i in range(4,14)]

workload = "workload-B"
for s in ['SWARM-KV','DM-ABD']:
    print(f'{s}:')

    for replicas in [3,5,7]:
        getavg = 0
        get99 = 0
        get1 = 0
        updavg = 0
        upd99 = 0
        upd1 = 0
        tputavg = 0

        
        for c in range(1,5):
            path = os.path.join("logs",
                f'fig9-replication-factor/{workload}/{s}/{replicas}replicas/client{c}.txt',
            )
            data = parse(path)
            getavg += data['GET']['psum'] / (4 * data['GET']['pcount'])
            get99 += data['GET'][99] / 4
            get1 += data['GET'][1] / 4
            updavg += data['UPDATE']['psum'] / (4 * data['UPDATE']['pcount'])
            upd99 += data['UPDATE'][99] / 4
            upd1 += data['UPDATE'][1] / 4
            tputavg += data['local tput'] / 4
        
        # opavg = ((getavg + updavg) / 2) if workload == "workload-A" else (getavg * 0.95 + updavg * 0.05)
        print(f'  - {replicas} replicas:')
        print(f'    - GETs average latency: {round(getavg, 3)}μs')
        print(f'    - GETs 1%-tile latency: {round(get1, 3)}μs')
        print(f'    - GETs 99%-tile latency: {round(get99, 3)}μs')
        print(f'    - UPDATEs average latency: {round(updavg, 3)}μs')
        print(f'    - UPDATEs 1%-tile latency: {round(upd1, 3)}μs')
        print(f'    - UPDATEs 99%-tile latency: {round(upd99, 3)}μs')
        print(f'    - throughput: {round(tputavg / 1000, 2)}Mops')

