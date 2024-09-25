#!/usr/bin/env python3

import os
from prelude import plt
from matplotlib.ticker import *
from matplotlib.lines import Line2D
from logparser import parse

for workload in ["B"]:
    schemes = {
        'SWARM-KV': {
            'label': 'SWARM-KV',
            'color': '#3b8df8',
            'lstyle': '-',
            'lwidth': .8,
        },
        'DM-ABD': {
            'label': 'DM-ABD',
            'color': '#d11414',
            'lstyle': '--',
            'lwidth': 1,
        },
        'FUSEE': {
            'label': 'FUSEE',
            'color': '#f4860b',
            'lstyle': ':',
            'lwidth': 1.4,
        },
    }

    ops = {
        'GET': 'o',
        'UPDATE': 'd',
    }

    ptiles = [0.1] + list(range(1,100)) + [99.9]


    legends = [
        Line2D([0], [0],
        color=schemes[s]['color'],
        linestyle=schemes[s]['lstyle'],
        linewidth=schemes[s]['lwidth'],
        label=schemes[s]['label'])
        for s in schemes
    ]

    fig, subplots = plt.subplots(1, 2, figsize=(3.35, 1.3), tight_layout=True)

    for plot in subplots:
        plot.tick_params(axis='both', which='major', pad=0.5)
        plot.tick_params(axis='both', which='minor', pad=0.5)

    line_style = dict(
        markersize=4.5
    )

    for subplot, op in zip(subplots, ops):
            for i, s in enumerate(schemes):
                    path = os.path.join('logs',
                        f'fig6-limited-cache/5MiB/workload-{workload}/{s}/client1.txt',
                    )
                    data = parse(path)[op]
                    xs = []
                    for ptile in ptiles:
                        xs.append(data[ptile])
                    
                    subplot.plot(xs + [1000000000], ptiles + [100],
                        **line_style,
                        color=schemes[s]['color'],
                        linestyle=schemes[s]['lstyle'],
                        linewidth=schemes[s]['lwidth'],
                    )

            subplot.grid(axis='y', which='major', linestyle='--', linewidth='0.5')
            subplot.grid(axis='y', which='minor', linestyle=':', linewidth='0.25')
            subplot.set_ylim(-5, 105)
            subplot.yaxis.set_major_locator(FixedLocator(list(range(0, 125, 50))))
            subplot.yaxis.set_minor_locator(FixedLocator(list(range(0, 100, 10))))
            subplot.yaxis.set_minor_formatter(NullFormatter())
            
            subplot.grid(axis='x', which='major', linestyle='--', linewidth='0.5')
            subplot.grid(axis='x', which='minor', linestyle=':', linewidth='0.25')
            subplot.set_xlim([0, 8.5 if op == 'GET' else 13])
            subplot.xaxis.set_major_locator(MultipleLocator(1 if op == 'GET' else 2))
            subplot.xaxis.set_major_formatter(ScalarFormatter())
            subplot.xaxis.set_minor_locator(MultipleLocator(0.5 if op == 'GET' else 1))
            subplot.xaxis.set_minor_formatter(NullFormatter())

            subplot.set_title(op + 's', pad=0)
            subplot.set_axisbelow(True)
            

    subplots[0].set_ylabel('Percentile (%)', labelpad=1)
    subplots[0].set_xlabel('Latency (µs)', labelpad=1)
    subplots[1].set_xlabel('Latency (µs)', labelpad=1)

    # Legend not included because it is the same as fig5. Uncomment to add the legend back.
    # leg = fig.legend(handles=legends, bbox_to_anchor=(0.05,0.975,0.90,0.015),
    #     loc='center', edgecolor='black', borderaxespad=0, ncols=4,
    #     borderpad=.3, labelspacing=0.1, mode='expand', handletextpad=0.5
    #     )

    plt.savefig(f'output-plots/fig6-limited-cache.pdf', format='pdf', bbox_inches = 'tight', pad_inches=0.01)
