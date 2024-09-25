#!/usr/bin/env python3

import os
from prelude import plt
from matplotlib.ticker import *
from matplotlib.lines import Line2D
from logparser import parse

# apps = [
#     {
#         'YCSB A - Zipfian' : 'A',
#         'YCSB B - Zipfian' : 'B',
#     },
#     # {
#     #     # 'YCSB A - Uniform' : 'A-uniform',
#     #     'YCSB B - Uniform' : 'B-uniform',
#     # },
# ][0]
workload = 'B'

schemes = {
    'SWARM-KV': {
        'label': 'SWARM-KV',
        'color': '#3b8df8',
        'lstyle': '-',
        'lwidth': 0.8,
    },
    'DM-ABD': {
        'label': 'DM-ABD',
        'color': '#d11414',
        'lstyle': '--',
        'lwidth': 1,
    },
}

legends = [
    Line2D([0], [0],
    color=schemes[s]['color'],
    linestyle=schemes[s]['lstyle'],
    linewidth=schemes[s]['lwidth'],
    label=schemes[s]['label'])
    for s in schemes
]

ops = {
    'GET': 'o',
    'UPDATE': 'd',
}

legends2 = [
    Line2D([], [],
    color='grey',
    marker=ops[op],
    linestyle='None',
    markersize=6,
    label=op)
    for op in ops
]

fig, subplots = plt.subplots(2, 2, figsize=(3.35, 1.3), tight_layout=True,
    # gridspec_kw={'width_ratios': [1,1.2]}
)

for row in subplots:
    for plot in row:
        plot.tick_params(axis='both', which='major', pad=0.5)
        plot.tick_params(axis='both', which='minor', pad=0.5)
for plot in subplots[0]:
    plot.tick_params(axis='x', which='both', bottom=False, labelbottom=False)


plt.tight_layout(pad=0, w_pad=0, h_pad=0, rect=(0,0,.902,1))
fig.subplots_adjust(wspace=0.16, hspace=.045)

# line_style = dict(
#     markersize=3.5
# )

client_counts = list(range(1,9)) + [10, 12, 14] + list(range(16, 68, 4))
outstandings = [1,4]
outstandingsMakers = {
    1: 'x',
    4: '+'
}

for i, a in enumerate(outstandings):
    subplots[0][i].set_title(f'{a} parallel operations' if a!=1 else 'sequential', pad=3)
    # workload = apps[app][0]
    # assert(workload in ['A', 'B'])
    for s in schemes:
            lats = []
            getlats = []
            updlats = []
            tputs = []
            for cc in client_counts:
                getavg = 0
                updavg = 0
                tputavg = 0
                # print(f'{workload}/a{a}/{s}-c{cc}: ', end="")
                for c in range(1, cc + 1):
                    path = os.path.join("logs",
                        f'fig8-scaling-clients/workload-{workload}/{a}parallelOps/{s}/{cc}clients/client{c}.txt',
                    )
                    # print(path)
                    data = parse(path)
                    getavg += data['GET']['psum'] / (cc * data['GET']['pcount'])
                    updavg += data['UPDATE']['psum'] / (cc * data['UPDATE']['pcount'])
                    # getavg += data['GET']['avg'] / cc
                    # updavg += data['UPDATE']['avg'] / cc
                    tputavg += data['local tput']

                opavg = ((getavg + updavg) / 2) if workload == 'A' else (getavg * 0.95 + updavg * 0.05)
                # print(f'latency-avg:{round(opavg,2)}, GETs:{round(getavg,2)}, UPDs:{round(updavg,2)}, tput:{round(tputavg / 1000,2)}')
                lats.append(opavg)
                getlats.append(getavg)
                updlats.append(updavg)
                tputs.append(tputavg / 1000)

            for ys, op in zip([getlats, updlats], ops):
                subplots[0][i].plot(client_counts, ys,
                    color=schemes[s]['color'],
                    linestyle=schemes[s]['lstyle'],
                    linewidth=schemes[s]['lwidth'],
                    marker=ops[op],
                    markevery=[(cc % 8 == 0) for cc in client_counts],
                    markersize=3.5
                )
            subplots[1][i].plot(client_counts, tputs,
                color=schemes[s]['color'],
                linestyle=schemes[s]['lstyle'],
                linewidth=schemes[s]['lwidth'],
                # marker=outstandingsMakers[a],
            )
    for j in [0,1]:
        subplot = subplots[j][i]
        subplot.grid(axis='both', which='major', linestyle='--', linewidth='0.5')
        subplot.grid(axis='both', which='minor', linestyle=':', linewidth='0.25')
        subplot.xaxis.set_major_locator(MultipleLocator(8))
        subplot.xaxis.set_minor_locator(MultipleLocator(4))
        subplot.set_xlim(0, 66)

subplots[0][0].set_ylim(1.5, 7)
subplots[0][0].yaxis.set_major_locator(FixedLocator([2,4,6]))
subplots[0][0].yaxis.set_minor_locator(MultipleLocator(1))
subplots[0][1].set_ylim(3, 14)
subplots[0][1].yaxis.set_major_locator(MultipleLocator(4))
subplots[0][1].yaxis.set_minor_locator(MultipleLocator(2))

subplots[1][0].set_ylim(0, 17)
subplots[1][0].yaxis.set_major_locator(FixedLocator([0,5,10,15]))
subplots[1][0].yaxis.set_minor_locator(MultipleLocator(2.5))
subplots[1][1].set_ylim(0, 32)
subplots[1][1].yaxis.set_major_locator(FixedLocator([0,10,20,30]))
subplots[1][1].yaxis.set_minor_locator(MultipleLocator(5))



#     subplot.set_axisbelow(True)
        
subplots[0][0].set_ylabel('    Latency (μs)', labelpad=1)
subplots[1][0].set_ylabel('Tput (Mops)    ', labelpad=1)
subplots[1][0].set_xlabel('Client threads', labelpad=0.2)
subplots[1][1].set_xlabel('Client threads', labelpad=0.2)

leg = fig.legend(handles=legends, bbox_to_anchor=(0.03,1.15,0.50,0.015),
    loc='center', edgecolor='black', borderaxespad=0, ncols=2,
    borderpad=.3, labelspacing=0.1, handletextpad=0.5
    )
leg = fig.legend(handles=legends2, bbox_to_anchor=(0.57,1.15,0.30,0.015),
    loc='center', edgecolor='black', borderaxespad=0, ncols=2,
    borderpad=.3, labelspacing=0.1, mode='expand', handlelength=0.6, handletextpad=0.5
    )

# print(leg.get_bbox_to_anchor())

plt.savefig("output-plots/fig8-scaling-clients.pdf", format='pdf', bbox_inches = 'tight', pad_inches=0.01)
