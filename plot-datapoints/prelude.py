#!/usr/bin/env python3
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Linux Libertine O'
mpl.rcParams['text.usetex'] = False
mpl.rcParams['hatch.linewidth'] = 0.6

from matplotlib import pyplot as plt

plt.style.use('seaborn-paper')

EXTRA_SMALL_SIZE = 6
SMALL_SIZE = 8
MEDIUM_SIZE = 9
NORMAL_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes

plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize

plt.rc('figure', titlesize=MEDIUM_SIZE)  # Figure title (used when having multiple subplots)
plt.rc('axes', titlesize=MEDIUM_SIZE)     # Subplot title

plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels

plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels

line_style = dict(linewidth='0.75', markersize=2.5)
errobar_style = dict(
    uplims=True,
    lolims=True,
    elinewidth=0.5, # width of error bar line
    ecolor='black',     # color of error bar
    capsize=1.0,    # cap length for error bar
    capthick=0.5    # cap thickness for error bar
)
#https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html
