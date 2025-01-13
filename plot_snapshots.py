import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from   numpy import genfromtxt
from   matplotlib.colors import ListedColormap as lcm

def plot_matrix(data, filename, id):
    plt.style.use('default')

    figure = plt.figure()
    axes = figure.add_subplot(111)

    #C or D colors
    if id == 0:
        cmap = lcm(['#e42a15', '#15100f', '#0116a6'])
        vmin = -1
        vmax = 1
    # -1 hole, 0 compare, 1 stay, 2 move
    elif id == 1:
        cmap = lcm(['#15100f', '#00FFB7', '#7900FF', '#e42a15'])
        vmin = -1
        vmax = 2

    # using the matshow() function
    myplot = axes.matshow(data, cmap=cmap, rasterized=True, vmin=vmin, vmax=vmax) 
    axes.set(xticklabels=[])
    axes.set(yticklabels=[])

    #plt.colorbar(myplot)

    plt.savefig(path + filename.strip('.dat').strip(path) + '.png', dpi=400, bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

path = './data/stochastic-choosing-the-best-and-mantain/snapshots/'
L = 100

for filename in glob.glob(path + '*.dat'):

    if '(0)' in filename:
        data_states = genfromtxt(filename, delimiter=',')
        data_states = data_states.reshape(L, L)
        plot_matrix(data_states, filename, 0)
    elif '(1)' in filename:
        data_actions = genfromtxt(filename, delimiter=',')
        data_actions = data_actions.reshape(L, L)
        plot_matrix(data_actions, filename, 1)
    
