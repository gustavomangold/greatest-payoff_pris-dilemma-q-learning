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
    # -1 hole, 0 compare, 1 move
    elif id == 1:
        cmap = lcm(['#15100f', '#15E42A', '#7900FF'])
        vmin = -1
        vmax = 1

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
        data[data == -1] =  42 #dummy value 
        data[data == 1] = -1
        data[data == 0] = 1
        data[data == 42] = 0
    if id == 0:
        data[data == -1] = -1 

    if step in correlation_dict.keys():
        return pearsonr(data, correlation_dict[step])[0]
    else:
        return data

def plot_one_corr(correlation_matrix_dict, main_plot):
    x_corr = []
    y_corr = []
    for key in correlation_matrix_dict.keys():
        x_corr.append(int(key))
        y_corr.append(float(correlation_matrix_dict[key]))
    y_corr = [y for _, y in sorted(zip(x_corr, y_corr))]
    x_corr = sorted(x_corr)

    return x_corr, y_corr

path = './data/stochastic-choosing-the-best/snapshots/'
L = 100
seed_to_plot = '1750884094_prof.dat'

def get_corr_dict_for_seed(seed):
    correlation_matrix_dict = {}
    for filename in glob.glob(path + '*' + seed):
        step = filename.split('Step')[1].split('_T')[0]
        if '(0)' in filename:
            data_states = genfromtxt(filename, delimiter=',')
            data_states = data_states.reshape(L, L)
            if int(step) in [32698, 0, 10000] and seed_to_plot == seed:
                plot_matrix(data_states, filename, 0)
            correlation_matrix_dict[step] = save_in_dict(data_states, correlation_matrix_dict, 0, step)
        elif '(1)' in filename:
            data_actions = genfromtxt(filename, delimiter=',')
            data_actions = data_actions.reshape(L, L)
            if int(step) in [32698, 0, 10000] and seed_to_plot == seed:
                plot_matrix(data_actions, filename, 1)
            correlation_matrix_dict[step] = save_in_dict(data_actions, correlation_matrix_dict, 1, step)
    return correlation_matrix_dict

label_size_standard = 15
plt.figure(figsize = (12, 2), dpi = 500)
plt.xlabel(r"$t$", fontsize = label_size_standard)
plt.ylabel(r"$C_{\mathbf{s}, \mathbf{a_G}}$", fontsize = label_size_standard)

seeds = []
for filename in glob.glob(path + '*dat'):
    seed  = filename.split('_CONF_1_')[1]
    if seed not in seeds:
        seeds.append(seed)

for seed in seeds:
    if seed == seed_to_plot: 
        main_plot = True
    else:
        main_plot = False

    corr_dict = get_corr_dict_for_seed(seed)
    x_corr, y_corr = plot_one_corr(corr_dict, main_plot)
    
    if main_plot:
        alpha = 1
        linewidth = 3 
    else:
        alpha = .3
        linewidth = 2
    plt.plot(x_corr, y_corr, linewidth = linewidth, color = '#4f759b', alpha = alpha)

plt.yticks([.0, .2, .4, .6])
plt.xticks([0, 10000, 30000])
plt.tick_params(axis = 'y', labelsize = label_size_standard)
plt.tick_params(axis = 'x', labelsize = label_size_standard)
plt.rc('axes', labelsize=17)
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.savefig('stochastic-choosing-the-best-correlation.png', dpi = 500, bbox_inches = 'tight')
