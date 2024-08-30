#!/usr/bin/env python3

import os
from logparser import parse

client_counts = list(range(1,9)) + [10, 12, 14] + list(range(16, 68, 4))
vsizes = [2**i for i in range(4,14)]

workload = "workload-A"
deathpoint = 6500000000 if workload == "workload-A" else 5000000000

path = os.path.join('logs',
    f'fig10-failure/{workload}/crash/client1.txt',
)
data = parse(path)
grain = 20
start_ms = -1000
end_ms = -11000

for op in ['GET','UPDATE']:
    print(f'{op}s latency:')
    opgrain = grain*4 if op == 'UPDATE' and workload == 'workload-B' and grain < 4 else grain
    l = len(data['b-midpoints']) - (opgrain - 1)
    xs = [
        (
            sum(
                data['b-midpoints'][i:i+opgrain]
            ) / opgrain - deathpoint
        ) / 1e6
        for i in range(0,l,grain)
    ]
    ys = [
        sum(
            data[f'b-{op}-sums'][i:i+opgrain]
        ) / (1000 * sum(
            data[f'b-{op}-counts'][i:i+opgrain]
        ))
        for i in range(0,l,grain)
    ]
    for x,y in zip(xs, ys):
        if x < -1000:
            continue
        if x > 11000:
            break
        print(f' at {int(round(x))}ms -> {op}s latency: {round(y,2)}μs')


print(f'throughput:')

l = len(data['b-midpoints']) - (grain - 1)
xs = [
    (
        sum(
            data['b-midpoints'][i:i+grain]
        ) / grain - deathpoint
    ) / 1e6
    for i in range(0,l,grain)
]
ys = [
    1000000 * sum(
        data[f'b-interval-counts'][i:i+grain]
    ) / sum(
        data[f'b-interval-sums'][i:i+grain]
    )
    for i in range(0,l,grain)
]
for x,y in zip(xs, ys):
    if x < -1000:
        continue
    if x > 11000:
        break
    print(f' at {int(round(x))}ms -> throughput: {round(y,1)}kops')
print('This script only prints one in every 20 points. For all points, check the print-datapoints/extra directory')
