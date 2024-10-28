import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from   numpy import genfromtxt
from   matplotlib.colors import ListedColormap as lcm

path = './data/move_as_c_or_d-async/snapshots/'
L = 100

for filename in glob.glob(path + '*.dat'):

    data = genfromtxt(filename, delimiter=',')

    data = data.reshape(L, L)

    plt.style.use('default')

    figure = plt.figure()
    axes = figure.add_subplot(111)

    # saturated red, red, black, blue, saturated blue
    cmap = lcm(['#D42B3D', '#e42a15', '#15100f', '#0116a6', '#34C5CB'])

    # using the matshow() function
    cax = axes.matshow(data, cmap=cmap, rasterized=True, vmin=-2, vmax=2)
    cbar = plt.colorbar(cax)

    plt.savefig(path + filename.strip('.dat').strip(path) + '.png', dpi=400, bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
