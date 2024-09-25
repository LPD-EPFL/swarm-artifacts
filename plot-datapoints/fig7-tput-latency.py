#!/usr/bin/env python3

import os
from prelude import plt
from matplotlib.ticker import *
from matplotlib.lines import Line2D
from logparser import parse

apps = [
    {
        'YCSB A - Zipfian' : 'A',
        'YCSB B - Zipfian' : 'B',
    },
    # {
    #     # 'YCSB A - Uniform' : 'A-uniform',
    #     'YCSB B - Uniform' : 'B-uniform',
    # },
][0]

schemes = {
    'SWARM-KV': {
        'label': 'SWARM-KV',
        'color': '#3b8df8',
        'lstyle': '-',
        'lwidth': 0.8,
        'markersize': 3.5,
        'marker': 'x',
        'mew': 0.8,
    },
    'DM-ABD': {
        'label': 'DM-ABD',
        'color': '#d11414',
        'lstyle': '--',
        'lwidth': 1,
        'markersize': 3.1,
        'marker': 's',
        'mew': .0,
    },
}

legends = [
    Line2D([0], [0],
    color=schemes[s]['color'],
    linestyle=schemes[s]['lstyle'],
    linewidth=schemes[s]['lwidth'],
    marker=schemes[s]['marker'],
    markersize=schemes[s]['markersize'],
    mew=schemes[s]['mew'],
    label=schemes[s]['label'])
    for s in schemes
]

fig, subplots = plt.subplots(1, 2, figsize=(3.35, 1.10), tight_layout=True,
    # gridspec_kw={'width_ratios': [1,1.2]}
)

plt.tight_layout(pad=0, w_pad=0, h_pad=0, rect=(0,0,.9415,1))
fig.subplots_adjust(wspace=0.2, hspace=.20, top=.80)

for plot in subplots:
    # for plot in row:
        plot.tick_params(axis='both', which='major', pad=0.5)
        plot.tick_params(axis='both', which='minor', pad=0.5)

# line_style = dict(
#     markersize=3.5
# )

outstandings = list(range(1,9))

# for row, rapps in zip(subplots, apps):
#     for subplot, app in zip(row, rapps):
for subplot, app in zip(subplots, apps):
        workload = apps[app][0]
        assert(workload in ['A', 'B'])
        for i, s in enumerate(schemes):
            lats = []
            tputs = []
            for a in outstandings:
                getavg = 0
                updavg = 0
                tputavg = 0
                # print(f'fig7-tput-latency/workload-{apps[app]}/{s}/{a}parallelOps/client*.txt')
                for c in range(1,5):
                    path = os.path.join("logs",
                        f'fig7-tput-latency/workload-{apps[app]}/{s}/{a}parallelOps/client{c}.txt',
                    )
                    data = parse(path)
                    getavg += data['GET']['psum'] / (4 * data['GET']['pcount'])
                    updavg += data['UPDATE']['psum'] / (4 * data['UPDATE']['pcount'])
                    # getavg += data['GET']['avg'] / 2
                    # updavg += data['UPDATE']['avg'] / 2
                    tputavg += data['local tput'] / 4

                opavg = ((getavg + updavg) / 2) if apps[app][0] == 'A' else (getavg * 0.95 + updavg * 0.05)
                # print(f'latency-avg:{opavg} tput:{tputavg}')
                lats.append(opavg)
                tputs.append(tputavg)
            
            subplot.plot(tputs, lats,
                color=schemes[s]['color'],
                linestyle=schemes[s]['lstyle'],
                linewidth=schemes[s]['lwidth'],
                marker=schemes[s]['marker'],
                markersize=schemes[s]['markersize'],
                mew=schemes[s]['mew'],
                # markevery=[True if c == 1 or (c % 4) == 0 else False for c in client_counts]
                # zorder...
            )

        # subplot.set_xticks([])
        subplot.set_xlim(0, 800 if workload == 'A' else 1200)
        subplot.xaxis.set_major_locator(MultipleLocator(250 if workload == 'A' else 500))
        subplot.xaxis.set_major_formatter(ScalarFormatter())
        subplot.xaxis.set_minor_locator(MultipleLocator(50 if workload == 'A' else 100))
        subplot.xaxis.set_minor_formatter(NullFormatter())
        # subplot.xaxis.set_major_formatter(FixedFormatter(['GET', 'UPDATE']))
        # _, automax = subplot.get_ylim()

        subplot.set_ylim(0, 11)
        subplot.grid(axis='both', which='major', linestyle='--', linewidth='0.5')
        subplot.grid(axis='both', which='minor', linestyle=':', linewidth='0.25')
        # subplot.set_yscale('log', base=20)
        # subplot.set_ylim([1.75, 20])
        subplot.yaxis.set_major_locator(MultipleLocator(2))
        subplot.yaxis.set_major_formatter(ScalarFormatter())
        subplot.yaxis.set_minor_locator(MultipleLocator(1))
        subplot.yaxis.set_minor_formatter(NullFormatter())

        subplot.set_title(app, pad=3)
        subplot.set_axisbelow(True)
        

# subplots[0][0].set_ylabel('Throughput (Mops)', labelpad=1)
# subplots[1][0].set_ylabel('Throughput (Mops)', labelpad=1)
# subplots[1][0].set_xlabel('Clients')
# subplots[1][1].set_xlabel('Clients')
subplots[0].set_ylabel('Latency (μs)', labelpad=1)
subplots[0].set_xlabel('Throughput (kops)', labelpad=1)
subplots[1].set_xlabel('Throughput (kops)', labelpad=1)

leg = fig.legend(handles=legends, bbox_to_anchor=(0.20,1.005,0.60,0.015),
    loc="center", edgecolor='black', borderaxespad=0, ncols=3,
    borderpad=.3, labelspacing=0.1, mode="expand", handletextpad=0.5
    )

# print(leg.get_bbox_to_anchor())

plt.savefig("output-plots/fig7-tput-latency.pdf", format='pdf', bbox_inches = 'tight', pad_inches=0.01)
