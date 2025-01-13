import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from   numpy import genfromtxt
from   matplotlib.colors import ListedColormap as lcm

path = './data/stochastic-choosing-the-best-and-mantain/snapshots/'
L = 100

for filename in glob.glob(path + '*.dat'):

    data = genfromtxt(filename, delimiter=',')

    data = data.reshape(L, L)

    plt.style.use('default')

    figure = plt.figure()
    axes = figure.add_subplot(111)

    #C or D colors
    #cmap = lcm(['#e42a15', '#15100f', '#0116a6'])
    # -1 hole, 0 compare, 1 stay, 2 move
    cmap = lcm(['#15100f', '#00FFB7', '#D41306', '#7900FF'])

    # using the matshow() function
    myplot = axes.matshow(data, cmap=cmap, rasterized=True, vmin=-1, vmax=2) 
    axes.set(xticklabels=[])
    axes.set(yticklabels=[])

    plt.colorbar(myplot)

    plt.savefig(path + filename.strip('.dat').strip(path) + '.png', dpi=400, bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
