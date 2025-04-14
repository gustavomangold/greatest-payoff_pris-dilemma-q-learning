import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from   numpy import genfromtxt
from   matplotlib.colors import ListedColormap as lcm
from   scipy.stats import pearsonr

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

def save_in_dict(data, correlation_dict, id, step):
    data = data.flatten()
    if id == 1:
        data[data == -1] = 0 
        data[data == 2] = -1 
    if id == 0:
        data[data == -1] = -1 

    if step in correlation_dict.keys():
        correlation_dict[step] = pearsonr(data, correlation_dict[step])[0]
    else:
        correlation_dict[step] = data


path = './data/stochastic-choosing-the-best-and-mantain/snapshots/'

L = 100

correlation_matrix_dict = {}

for filename in glob.glob(path + '*.dat'):
    step = filename.split('Step')[1].split('_T')[0]
    if '(0)' in filename:
        data_states = genfromtxt(filename, delimiter=',')
        data_states = data_states.reshape(L, L)
        if int(step) in [100000, 0, 50000]:
            plot_matrix(data_states, filename, 0)
        save_in_dict(data_states, correlation_matrix_dict, 0, step)
    elif '(1)' in filename:
        data_actions = genfromtxt(filename, delimiter=',')
        data_actions = data_actions.reshape(L, L)
        if int(step) in [100000, 0, 50000]:
            plot_matrix(data_actions, filename, 1)
        save_in_dict(data_actions, correlation_matrix_dict, 1, step)

x_corr = []
y_corr = []
for key in correlation_matrix_dict.keys():
    x_corr.append(int(key))
    y_corr.append(float(correlation_matrix_dict[key]))

y_corr = [y for _, y in sorted(zip(x_corr, y_corr))]
x_corr = sorted(x_corr)
plt.figure(figsize = (12, 2), dpi = 500)
plt.yticks([.1, .3, .5])
plt.xlabel(r"$t$")
plt.ylabel(r"$C_{\mathbf{s}, \mathbf{a_{PB}}}$")
plt.plot(x_corr, y_corr, linewidth = 2., color = '#4f759b')
plt.savefig('stochastic-choosing-the-best-and-maintain-correlation.png', dpi = 500, bbox_inches = 'tight')  
