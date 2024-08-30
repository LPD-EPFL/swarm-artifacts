#!/usr/bin/env python3

import os
from prelude import plt
from matplotlib.ticker import *
from matplotlib.patches import Patch
from logparser import parse

workload = 'B'
a = 1

replication_factors = [3,5,7]

schemes = {
    'SWARM-KV': {
        'label': 'SWARM-KV',
        'color': '#3b8df8',
        # 'lstyle': '-',
        # 'lwidth': 0.8,
        # 'markersize': 3.5,
        # 'marker': 'x',
        # 'mew': 0.8,
        'hatch': '',
    },
    'DM-ABD': {
        'label': 'DM-ABD',
        'color': '#d11414',
        # 'lstyle': '--',
        # 'lwidth': 1,
        # 'markersize': 3.1,
        # 'marker': 's',
        # 'mew': .0,
        'hatch': '///',
    },
}


legends2 = [
    Patch(
        facecolor=schemes[s]['color'],
        hatch=schemes[s]['hatch'],
        linestyle='None',
        edgecolor='white',
        label=schemes[s]['label'],
    ) for s in schemes
]


fig, subplots = plt.subplots(1, 2, figsize=(3.35, 1.3), tight_layout=True,
    gridspec_kw={'width_ratios': [2,1]}
)

# plt.tight_layout(pad=0, w_pad=0, h_pad=0, rect=(0,0,.941,1))
# fig.subplots_adjust(wspace=0.2, hspace=.20, top=.80)

for plot in subplots:
    # for plot in row:
        plot.tick_params(axis='both', which='major', pad=0.5)
        plot.tick_params(axis='both', which='minor', pad=0.5)

# line_style = dict(
#     markersize=3.5
# )


errobar_style = dict(
    # elinewidth=0.5,     # width of error bar line
    ecolor='black',   # color of error bar
    capsize=2.0,        # cap length for error bar
    # capthick=0.5        # cap thickness for error bar
)

# for row, rapps in zip(subplots, apps):
#     for subplot, app in zip(row, rapps):
xpos = 0.5
upd_offset = (len(schemes)+1)*len(replication_factors)+2
for j, rep_factor in enumerate(replication_factors):
        for i, s in enumerate(schemes):
            getavg = 0
            get99 = 0
            get1 = 0
            updavg = 0
            upd99 = 0
            upd1 = 0
            tputavg = 0
            # print(f'{workload}/a{a}/{s}-m{rep_factor}: ', end="")
            for c in range(1,5):
                path = os.path.join("logs",
                    f'fig9-replication-factor/workload-{workload}/{s}/{rep_factor}replicas/client{c}.txt',
                )
                # print(path)
                data = parse(path)
                getavg += data['GET']['psum'] / (4 * data['GET']['pcount'])
                get99 += data['GET'][99] / 4
                get1 += data['GET'][1] / 4
                updavg += data['UPDATE']['psum'] / (4 * data['UPDATE']['pcount'])
                upd99 += data['UPDATE'][99] / 4
                upd1 += data['UPDATE'][1] / 4
                # getavg += data['GET']['avg'] / 2
                # updavg += data['UPDATE']['avg'] / 2
                tputavg += data['local tput'] / 4

            opavg = ((getavg + updavg) / 2) if workload == 'A' else (getavg * 0.95 + updavg * 0.05)
            # print(f'lat-avg:{round(opavg,2)}, GETs:{round(getavg,2)}, UPDs:{round(updavg,2)}, tput:{round(tputavg,2)}')
            
            for cap in subplots[0].bar(xpos, getavg, 1,
                yerr=[[getavg - get1], [get99 - getavg]],
                **errobar_style,
                color=schemes[s]['color'],
                hatch=schemes[s]['hatch'],
                edgecolor='white',
                linewidth=0
            ).errorbar.lines[1]:
                cap.set_marker("_")
                cap.set_markeredgewidth(0.25)
                cap.set_linewidth(1)

            for cap in subplots[0].bar(xpos + upd_offset, updavg, 1,
                yerr=[[updavg - upd1], [upd99 - updavg]],
                **errobar_style,
                color=schemes[s]['color'],
                hatch=schemes[s]['hatch'],
                edgecolor='white',
                linewidth=0
            ).errorbar.lines[1]:
                cap.set_marker("_")
                cap.set_markeredgewidth(0.25)
                cap.set_linewidth(1)

            subplots[1].bar(xpos, tputavg, 1,
                color=schemes[s]['color'],
                hatch=schemes[s]['hatch'],
                edgecolor='white',
                linewidth=0
            )
            xpos += 1
        xpos += 1

subplots[0].set_xlim(-.5, xpos+upd_offset-1)
subplots[1].set_xlim(-.5, xpos-1)

subplots[0].set_ylim(0, 7)
subplots[1].set_ylim(0, 500)

for subplot in subplots:
        subplot.grid(axis='y', which='major', linestyle='--', linewidth='0.5')
        subplot.grid(axis='y', which='minor', linestyle=':', linewidth='0.25')
        subplot.set_axisbelow(True)

        # # subplot.set_xticks([])
        # subplot.set_xlim(0, 800 if workload == 'A' else 1200)
        # subplot.xaxis.set_major_locator(MultipleLocator(250 if workload == 'A' else 500))
        # subplot.xaxis.set_major_formatter(ScalarFormatter())
        # subplot.xaxis.set_minor_locator(MultipleLocator(50 if workload == 'A' else 100))
        # subplot.xaxis.set_minor_formatter(NullFormatter())
        # # subplot.xaxis.set_major_formatter(FixedFormatter(['GET', 'UPDATE']))
        # # _, automax = subplot.get_ylim()

        # subplot.set_ylim(0, 11)
        # # subplot.set_yscale('log', base=20)
        # # subplot.set_ylim([1.75, 20])
        # subplot.yaxis.set_major_locator(MultipleLocator(2))
        # subplot.yaxis.set_major_formatter(ScalarFormatter())
        # subplot.yaxis.set_minor_locator(MultipleLocator(1))
        # subplot.yaxis.set_minor_formatter(NullFormatter())

        # subplot.set_title(app, pad=3)
        
locs = [(len(schemes)+1)*i + len(schemes)/2 for i in range(len(replication_factors))]
subplots[0].xaxis.set_major_locator(FixedLocator(locs + [l + upd_offset for l in locs]))
subplots[0].xaxis.set_major_formatter(FixedFormatter(replication_factors + replication_factors))
subplots[1].xaxis.set_major_locator(FixedLocator(locs))
subplots[1].xaxis.set_major_formatter(FixedFormatter(replication_factors))

subplots[0].yaxis.set_major_locator(MultipleLocator(2))
subplots[0].yaxis.set_minor_locator(MultipleLocator(1))
# subplots[1].yaxis.set_major_locator(MultipleLocator(2))
# subplots[1].yaxis.set_minor_locator(MultipleLocator(1))
subplots[1].yaxis.set_major_locator(MultipleLocator(200))
subplots[1].yaxis.set_minor_locator(MultipleLocator(50))
        
subplots[0].set_title('   GETs              UPDATEs', pad=1)
# subplots[1].set_title('UPDATEs')
# subplots[1].set_title('', pad=1)

subplots[0].set_ylabel('Latency (μs)', labelpad=1)
# subplots[1].set_ylabel('Latency (μs)', labelpad=1)
subplots[1].set_ylabel('Tput (kops)', labelpad=1)
subplots[0].set_xlabel('Replicas', labelpad=1)
subplots[1].set_xlabel('Replicas', labelpad=1)

leg = fig.legend(handles=legends2, bbox_to_anchor=(0.20,.98,0.60,0.015),
    loc="center", edgecolor='black', borderaxespad=0, ncols=3,
    borderpad=.3, labelspacing=0.1, mode="expand", handletextpad=0.5
)

# print(leg.get_bbox_to_anchor())

plt.savefig("output-plots/fig9-replication-factor.pdf", format='pdf', bbox_inches = 'tight', pad_inches=0.01)
