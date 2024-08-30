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
for wid in [0]:
    workload = ['A', 'B'][wid]
    deathpoint = [6500000000,5000000000][wid]

    schemes = {
        'SWARM': {
            'label': 'SWARM-KV',
            'color': '#3b8df8',
            'lstyle': '-',
            'lwidth': 0.8,
        },
        # 'ABD': {
        #     'label': 'DM-ABD',
        #     'color': '#d11414',
        #     'lstyle': '--',
        #     'lwidth': 1,
        # },
    }

    ops = {
        'GET': {
            'label': 'GETs',
            'color': '#0f6010',
        },
        'UPDATE': {
            'label': 'UPDATEs',
            'color': '#e9811e',
        },
    }
    both = {
        'label': 'Both',
        'color': '#3b8df8',
    }

    leg = {**ops, **{'Both': both}}

    legends = [
        Line2D([], [],
        color=leg[op]['color'],
        label=leg[op]['label'])
        for op in leg
    ]

    fig, subplots = plt.subplots(2, 2, figsize=(3.35, 1.3), tight_layout=True,
        # gridspec_kw={'width_ratios': [1,1.2]}
    )

    for row in subplots:
        for plot in row:
            plot.tick_params(axis='both', which='major', pad=0.5)
            plot.tick_params(axis='both', which='minor', pad=0.5)
            plot.plot([0,0], [-1e9,1e9],
                    color='red',
                    linewidth=0.5,
                    linestyle='-'
                )
    for plot in subplots[0]:
        plot.tick_params(axis='x', which='both', bottom=False, labelbottom=False)


    plt.tight_layout(pad=0, w_pad=0, h_pad=0, rect=(0,0,.877,1))
    fig.subplots_adjust(wspace=0.19, hspace=.045)

    # line_style = dict(
    #     markersize=3.5
    # )

    # subplots[0][i].set_title(f'{a} parallel operations' if a!=1 else 'sequential', pad=3)

    for s in schemes:
        path = os.path.join("logs",
            f'fig10-failure/workload-{workload}/crash/client1.txt',
        )
        data = parse(path)
        for col in [0,1]:
            grain = [20,1][col]
            timescale = [1e9,1e6][col]
            for op in ops:
                opgrain = grain*4 if op == 'UPDATE' and workload == 'B' else grain
                l = len(data['b-midpoints']) - (opgrain - 1)
                xs = [
                    (
                        sum(
                            data['b-midpoints'][i:i+opgrain]
                        ) / opgrain - deathpoint
                    ) / timescale
                    for i in range(l)
                ]
                for i in range(l):
                    if sum(data[f'b-{op}-counts'][i:i+opgrain]) == 0:
                        # print(i, i+opgrain)
                        # print(f'b-GET-sums', data[f'b-GET-sums'][i:i+opgrain])
                        # print(f'b-GET-counts', data[f'b-GET-counts'][i:i+opgrain])
                        # print(f'b-UPDATE-sums', data[f'b-UPDATE-sums'][i:i+opgrain])
                        # print(f'b-UPDATE-counts', data[f'b-UPDATE-counts'][i:i+opgrain])
                        # print(f'b-midpoints', data[f'b-midpoints'][i:i+opgrain])
                        raise "oops ?"
                ys = [
                    sum(
                        data[f'b-{op}-sums'][i:i+opgrain]
                    ) / (1000 * sum(
                        data[f'b-{op}-counts'][i:i+opgrain]
                    ))
                    for i in range(l)
                ]
                subplots[0][col].plot(xs, ys,
                    color=ops[op]['color'],
                    linewidth=[0.5,.8][col]
                )
            
            l = len(data['b-midpoints']) - (grain - 1)
            xs = [
                (
                    sum(
                        data['b-midpoints'][i:i+grain]
                    ) / grain - deathpoint
                ) / timescale
                for i in range(l)
            ]
            ys = [
                    1000000 * sum(
                        data[f'b-interval-counts'][i:i+grain]
                    ) / sum(
                        data[f'b-interval-sums'][i:i+grain]
                    )
                    for i in range(l)
                ]
            subplots[1][col].plot(xs, ys,
                color=both['color'],
                linewidth=[0.5,.8][col]
            )
    for j in [0,1]:
        subplot = subplots[j][0]
        subplot.grid(axis='both', which='major', linestyle='--', linewidth='0.5')
        subplot.grid(axis='both', which='minor', linestyle=':', linewidth='0.25')
        subplot.set_xlim(-1, 11)
        subplot.xaxis.set_major_locator(MultipleLocator(2))
        subplot.xaxis.set_minor_locator(MultipleLocator(1))

        subplot = subplots[j][1]
        subplot.grid(axis='both', which='major', linestyle='--', linewidth='0.5')
        subplot.grid(axis='both', which='minor', linestyle=':', linewidth='0.25')
        subplot.set_xlim(-7.5, 22.5)
        subplot.xaxis.set_major_locator(MultipleLocator(5))
        subplot.xaxis.set_minor_locator(MultipleLocator(2.5))

    subplots[0][0].set_ylim(0, 5)
    subplots[0][0].yaxis.set_major_locator(MultipleLocator(2))
    subplots[0][0].yaxis.set_minor_locator(MultipleLocator(1))

    subplots[1][0].set_ylim(0, [275,350][wid])
    subplots[1][0].yaxis.set_major_locator(MultipleLocator(100))
    subplots[1][0].yaxis.set_minor_locator(MultipleLocator(50))


    subplots[0][1].set_ylim(2, [5,5.5][wid])
    subplots[0][1].yaxis.set_major_locator(MultipleLocator(1))
    subplots[0][1].yaxis.set_minor_locator(MultipleLocator(0.5))
    if workload == 'A':
        subplots[1][1].set_ylim(180, 270)
    else:
        subplots[1][1].set_ylim(250, 350)
    subplots[1][1].yaxis.set_major_locator(MultipleLocator(40))
    subplots[1][1].yaxis.set_minor_locator(MultipleLocator(10))



    #     subplot.set_axisbelow(True)
            
    subplots[0][0].set_ylabel('    Latency (μs)', labelpad=4)
    subplots[1][0].set_ylabel('Tput (kops)    ', labelpad=1)
    subplots[1][0].set_xlabel('Time (s)', labelpad=0.2)
    subplots[1][1].set_xlabel('Time (ms)', labelpad=0.2)
    subplots[0][0].set_title('Zoomed-out', pad=0.2)
    subplots[0][1].set_title('Zoomed-in', pad=0.2)

    leg = fig.legend(handles=legends, bbox_to_anchor=(0.05,1.10,0.80,0.015),
        loc='center', edgecolor='black', borderaxespad=0, ncols=3,
        borderpad=.3, labelspacing=0.1, handletextpad=0.5
    )

    # print(leg.get_bbox_to_anchor())

    plt.savefig(f'output-plots/fig10-failure.pdf', format='pdf', bbox_inches = 'tight', pad_inches=0.01)
