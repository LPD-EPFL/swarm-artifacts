#!/usr/bin/env python3

import os
from prelude import plt
from matplotlib.ticker import *
from matplotlib.lines import Line2D
from logparser import parse

for workload in ["A"]:
  for clients in [16]:
    schemes = {
        # 'RAW': {
        #     'label': 'RAW',
        #     'color': '#893ab0',
        #     'lstyle': '-.',
        #     'lwidth': 1.2,
        # },
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
        # 'FUSEE': {
        #     'label': 'FUSEE',
        #     'color': '#f4860b',
        #     'lstyle': ':',
        #     'lwidth': 1.4,
        # },
    }

    ops = {
        'GET': 'o',
        'UPDATE': 'd',
    }

    ptiles = [0.1] + list(range(1,100)) + [99.9]


    legends = [
        Line2D([0], [0],
        color=schemes[s]['color'],
        # marker=marker.next(),
        linestyle=schemes[s]['lstyle'],
        linewidth=schemes[s]['lwidth'],
        label=schemes[s]['label'])
        for s in schemes
    ]

    # legends2 = [
    #     Line2D([], [],
    #     color='grey',
    #     marker=ops[op],
    #     linestyle='None',
    #     markersize=6,
    #     label=op)
    #     for op in ops
    # ]

    fig, subplots = plt.subplots(1, 2, figsize=(3.35, 1.3), tight_layout=True,
        # gridspec_kw={'width_ratios': [1, 1.3]}
    )

    # plt.tight_layout(pad=0, w_pad=0, h_pad=0, rect=(0,0,.9,1))
    # fig.subplots_adjust(wspace=0.22, hspace=.20, top=.80)

    for plot in subplots:
        plot.tick_params(axis='both', which='major', pad=0.5)
        plot.tick_params(axis='both', which='minor', pad=0.5)

    line_style = dict(
        markersize=4.5
    )

    for subplot, op in zip(subplots, ops):
            for i, s in enumerate(schemes):
                    path = os.path.join('logs',
                        f'fig11-single-key/workload-{workload}/{clients}clients/{s}/client1.txt',
                    )
                    data = parse(path)[op]
                    xs = []
                    for ptile in ptiles:
                        xs.append(data[ptile])
                    
                    subplot.plot(xs + [1000000000], ptiles + [100],
                        **line_style,
                        color=schemes[s]['color'],
                        # marker=ops[op],
                        linestyle=schemes[s]['lstyle'],
                        linewidth=schemes[s]['lwidth'],
                        # markevery=[True if c == 1 or c == 99 or (c % 25) == 0 else False for c in ptiles + [100]]
                        # zorder...
                    )

            subplot.grid(axis='y', which='major', linestyle='--', linewidth='0.5')
            subplot.grid(axis='y', which='minor', linestyle=':', linewidth='0.25')
            # subplot.set_xticks([])
            subplot.set_ylim(-5, 105)
            subplot.yaxis.set_major_locator(FixedLocator(list(range(0, 125, 50))))
            subplot.yaxis.set_minor_locator(FixedLocator(list(range(0, 100, 10))))
            # subplot.xaxis.set_major_formatter(FixedFormatter(['GET', 'UPDATE']))
            subplot.yaxis.set_minor_formatter(NullFormatter())
            
            #_, automax = subplot.get_ylim()
            #subplot.set_ylim(0, 20)
            subplot.grid(axis='x', which='major', linestyle='--', linewidth='0.5')
            subplot.grid(axis='x', which='minor', linestyle=':', linewidth='0.25')
            # subplot.set_yscale('log', base=20)
            subplot.set_xlim([0, 36 if op == 'GET' else 36])
            subplot.xaxis.set_major_locator(MultipleLocator(10))
            subplot.xaxis.set_major_formatter(ScalarFormatter())
            subplot.xaxis.set_minor_locator(MultipleLocator(2))
            subplot.xaxis.set_minor_formatter(NullFormatter())

            subplot.set_title(op + 's', pad=0)
            subplot.set_axisbelow(True)
            

    subplots[0].set_ylabel('Percentile (%)', labelpad=1)
    subplots[0].set_xlabel('Latency (µs)', labelpad=1)
    subplots[1].set_xlabel('Latency (µs)', labelpad=1)

    leg = fig.legend(handles=legends, bbox_to_anchor=(0.18,0.975,0.70,0.015),
        loc='center', edgecolor='black', borderaxespad=0, ncols=2,
        borderpad=.3, labelspacing=0.1, handletextpad=0.5
    )
    # leg = fig.legend(handles=legends2, bbox_to_anchor=(0.65,1.001,0.30,0.015),
    #     loc='center', edgecolor='black', borderaxespad=0, ncols=2,
    #     borderpad=.3, labelspacing=0.1, mode='expand', handlelength=0.6, handletextpad=0.5
    # )

    # print(leg.get_bbox_to_anchor())

    plt.savefig(f'output-plots/fig11-single-key.pdf', format='pdf', bbox_inches = 'tight', pad_inches=0.01)
