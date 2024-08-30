#!/usr/bin/env python3

import os
from prelude import plt
from matplotlib.ticker import *
from matplotlib.lines import Line2D
from logparser import parse

apps = {
        'YCSB A - Zipfian' : 'A',
        'YCSB B - Zipfian' : 'B',
}
# workload = 'A'

schemes = {
    'In-n-Out': {
        'label': "In-n-Out",
        'color': '#3b8df8',
        'lstyle': '-',
        'lwidth': 0.8,
    },
    'Out-P': {
        'label': 'Out-P.',
        'color': '#300093',
        'lstyle': ':',
        'lwidth': 1.3,
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


plt.tight_layout(pad=0, w_pad=0, h_pad=0, rect=(0,0,.8815,1))
fig.subplots_adjust(wspace=0.16, hspace=.045)

# line_style = dict(
#     markersize=3.5
# )

sizes = [2**i for i in range(4,14)]
indexes = [i for i, _ in enumerate(sizes)]
a = 1 # outstandings
for i, app in enumerate(apps):
    subplots[0][i].set_title(app, pad=3)
    workload = apps[app]
    assert(workload in ['A', 'B'])
    for s in schemes:
            lats = []
            getlats = []
            updlats = []
            tputs = []
            for sz in sizes:
                getavg = 0
                updavg = 0
                tputavg = 0
                for c in range(1,5):
                    path = os.path.join("logs",
                        f'fig8-value-sizes/workload-{workload}/SWARM-KV/{s}/values-of-{sz}B/client{c}.txt',
                    )
                    # print(path)
                    data = parse(path)
                    getavg += data['GET']['psum'] / (4 * data['GET']['pcount'])
                    updavg += data['UPDATE']['psum'] / (4 * data['UPDATE']['pcount'])
                    # getavg += data['GET']['avg'] / 4
                    # updavg += data['UPDATE']['avg'] / 4
                    tputavg += data['local tput']

                opavg = ((getavg + updavg) / 2) if workload == 'A' else (getavg * 0.95 + updavg * 0.05)
                # print(opavg, 4 * 1000 / opavg, tputavg)
                lats.append(opavg)
                getlats.append(getavg)
                updlats.append(updavg)
                tputs.append(tputavg / 1000)


            for ys, op in zip([getlats, updlats], ops):
                subplots[0][i].plot(indexes, ys,
                    color=schemes[s]['color'],
                    linestyle=schemes[s]['lstyle'],
                    linewidth=schemes[s]['lwidth'],
                    marker=ops[op],
                    markevery=[(x % 3 == 0) for x in indexes],
                    markersize=3.5,
                )
            subplots[1][i].plot(indexes, tputs,
                color=schemes[s]['color'],
                linestyle=schemes[s]['lstyle'],
                linewidth=schemes[s]['lwidth'],
            )
    for j in [0,1]:
        subplot = subplots[j][i]
        subplot.grid(axis='both', which='major', linestyle='--', linewidth='0.5')
        subplot.grid(axis='both', which='minor', linestyle=':', linewidth='0.25')
        subplot.xaxis.set_major_locator(FixedLocator([0,3,6,9]))
        subplot.xaxis.set_major_formatter(FixedFormatter(["16$\,$B","128$\,$B","1$\,$KiB","8$\,$KiB"]))
        subplot.xaxis.set_minor_locator(MultipleLocator(1))
        subplot.set_xlim(-.5, 9.5)

subplots[0][0].set_ylim(1.5, 8.5)
subplots[0][0].yaxis.set_major_locator(MultipleLocator(2))
subplots[0][0].yaxis.set_minor_locator(MultipleLocator(1))
subplots[0][1].set_ylim(1.5, 8.5)
subplots[0][1].yaxis.set_major_locator(MultipleLocator(2))
subplots[0][1].yaxis.set_minor_locator(MultipleLocator(1))

subplots[1][0].set_ylim(0, 1.75)
subplots[1][0].yaxis.set_major_locator(FixedLocator([0,0.5,1,1.5]))
subplots[1][0].yaxis.set_minor_locator(MultipleLocator(.25))
subplots[1][1].set_ylim(0, 1.75)
subplots[1][1].yaxis.set_major_locator(FixedLocator([0,0.5,1,1.5]))
subplots[1][1].yaxis.set_minor_locator(MultipleLocator(.25))



#     subplot.set_axisbelow(True)
        
subplots[0][0].set_ylabel('    Latency (μs)', labelpad=1)
subplots[1][0].set_ylabel('Tput (Mops)    ', labelpad=1)
subplots[1][0].set_xlabel('Value size (Bytes, log)', labelpad=0.2)
subplots[1][1].set_xlabel('Value size (Bytes, log)', labelpad=0.2)

leg = fig.legend(handles=legends, bbox_to_anchor=(0.02,1.15,0.50,0.015),
    loc='center', edgecolor='black', borderaxespad=0, ncols=2,
    borderpad=.3, labelspacing=0.1, handletextpad=0.5
    )
leg = fig.legend(handles=legends2, bbox_to_anchor=(0.56,1.15,0.30,0.015),
    loc='center', edgecolor='black', borderaxespad=0, ncols=2,
    borderpad=.3, labelspacing=0.1, mode='expand', handlelength=0.6, handletextpad=0.5
    )

# print(leg.get_bbox_to_anchor())

plt.savefig("output-plots/fig8-value-sizes.pdf", format='pdf', bbox_inches = 'tight', pad_inches=0.01)
