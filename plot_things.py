import numpy as np
import pandas as pd
import glob
import io
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools
import re
from matplotlib.ticker import ScalarFormatter

def plot_heatmap(x_list, y_list, cooperation_list):
    '''
    Plot the heatmap

    Returns:
    (void)
    '''
    x = np.array(x_list)
    y = np.array(y_list)
    z = np.array(cooperation_list)

    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(ScalarFormatter())

    ax.set_xlabel(r'$\rho$')
    ax.set_ylabel(r'$p_d$')
    #plt.gca().invert_yaxis()

    plt.tricontourf(x, y, z, levels = np.arange(0, .9001, .005), cmap = 'jet_r')
    cbar = plt.colorbar()
    ax.set_yticks([.01, .1, 1])
    ax.set_ylim(.01, 1.)
    ax.yaxis.set_ticks_position('both')# Ticks on all 4 sides
    ax.xaxis.set_ticks_position('both')
    cbar.ax.tick_params(labelsize=14)
    ax.tick_params(axis='y', labelsize=label_size_standard)
    ax.tick_params(axis='x', labelsize=label_size_standard)

    cbar.set_ticks([.0, .3, .5, .7, .9])

    plt.savefig('heatmap_coop-async-stochastic.png', dpi=400, bbox_inches='tight')
    plt.clf()

    return

def plot_separate_column(colnames, color):
    for column in colnames[1:]:
        if column[2] == 'b':
            plt.plot(data[['t']].to_numpy(), data[[column]].to_numpy(),
                color = next(color), label = r'$Q_{{{}}}$'.format(column[1:]))
    plt.legend(loc = 'best')
    plt.savefig(filename + 'q-table-for-d.png', dpi = 400, bbox_inches='tight')
    plt.close()

    for column in colnames[1:]:
        if column[2] == 'm':
            plt.plot(data[['t']].to_numpy(), data[[column]].to_numpy(),
                color = next(color), label = r'$Q_{{{}}}$'.format(column[1:]))
    plt.legend()
    plt.savefig(filename + 'q-table-for-c.png', dpi = 400, bbox_inches='tight')
    plt.close()

def plot_data_values(filename, data, colnames, color, identifier: str):
    #plt.title('Prob diffusion = ' + filename.split('P_DIFFUSION')[1][:3] + ' Occupation =' +
    #    filename.split('rho')[1][:4])
    if identifier == 'cooperation':
        data['mean_coop'] = data['f_c'] / (data['f_d'] + data['f_c'])
        plt.plot(data[['t']].to_numpy(), data[['mean_coop']].to_numpy(), color = next(color))
        plt.ylim(0., 1.)
        plt.savefig(filename + 'cooperation.png', dpi = 400)

    elif identifier == 'q-table':
        plot_separate_column(colnames, color)
    plt.clf()
    plt.cla()
    plt.close()
path = './data/stochastic-choosing-the-best/'

cooperation_dict = {}
variance_dict    = {}
colnames = ['t',  'f_c',  'f_d', 'r_m', 'Qdb',  'Qcb', 'Qdm', 'Qcm']

labels_to_plot = []
x_axis_to_plot = []
cooperation_plot = []

check_repeat_params = []
x_static = []
y_static = []

index = 0
for filename in glob.glob(path + 'T*.dat'):
    data = pd.read_csv(filename, comment = '#', delimiter = ' ', names = colnames, index_col = False)
    
    pattern = r"[a-zA-Z]"
    string  = filename.split('P_DIFFUSION')[1][0:6]
    string = ''.join(i for i in string if (i.isdigit() or i == '.'))
    key = float(string)
    data['mean_coop'] = data['f_c'] / (data['f_d'] + data['f_c'])

    """#plot_data_values(filename, data, colnames_dynamic, color, 'cooperation')
    #plot_data_values(filename, data, colnames_dynamic, color, 'q-table')

    if 0.8 > key > 0.5:
        plot_data_values(filename, data, colnames_dynamic, color, 'q-table')
        plot_data_values(filename, data, colnames_dynamic, color, 'cooperation')
"""

    """reward_series = data['r_m']
    plt.plot(np.array(data['t']), np.array(reward_series), label = key, color = next(color))
    plt.xlabel('t')
    plt.ylabel(r'$\bar{R}$')
    plt.savefig('reward-time_series' + str(key) + '.png', dpi = 400)"""
    """plot_data_values(filename, data, colnames_dynamic, color, 'q-table')
    plot_data_values(filename, data, colnames_dynamic, color, 'cooperation')"""
    try:
        if (float(filename.split('T')[1][:4]) == 1.4):
            x_variable  = float(filename.split('rho')[1][:6])
            mean_coop   = np.mean(data[['mean_coop']].to_numpy()[-100:])
            var_coop    = np.var(data[['mean_coop']].to_numpy()[-100:])

            """if key <= 0.01:
                plot_data_values(filename, data, colnames, color, 'q-table')"""

            if (not ([key, x_variable] in check_repeat_params)):
                if key == 0.:
                    x_static.append(x_variable)
                    y_static.append(mean_coop)

                if key in (cooperation_dict.keys()):
                    cooperation_dict[key].append([x_variable, float(mean_coop)])
                    variance_dict[key].append([x_variable, float(var_coop)])
                else:
                    cooperation_dict[key] = [[x_variable, float(mean_coop)]]
                    variance_dict[key] = [[x_variable, float(var_coop)]]

                #no duplicates
                if key != 0:
                    labels_to_plot.append(key)
                    x_axis_to_plot.append(x_variable)
                    cooperation_plot.append(mean_coop)

                check_repeat_params.append([key, x_variable])

            index += 1
    except Exception as E:
        print('Unavailable data for' + filename)
        print(E)

plt.rc('axes', labelsize=17)
label_size_standard = 14

plot_heatmap(x_axis_to_plot, labels_to_plot, cooperation_plot)

plt.style.use('seaborn-v0_8-ticks')

#codigo horrivel, mas funciona
# tem que dar sorted com relaçao a coordenada x
# senao o plot fica errado, fora de ordem as conexoes
color_plots_static = '#EB6E14'
x_plot, y_plot = zip(*sorted(zip(x_static, y_static),key=lambda x: x[0]))
plt.plot(x_plot, y_plot, label = r'$p_d = 0$', color = color_plots_static, alpha=0.75, linestyle='dotted')

marker = itertools.cycle((',', 'P', 'p', '*', '.', 'X', 'P', 'p', 'o'))
color  = itertools.cycle(("#0E56FD", "#6135ca", "#606b9b", "#4AA6B5", "#335430", "#d02f6a", "#e61976", "#ff1611"))

fig, ax1 = plt.subplots()

plt.tick_params(axis='y', labelsize=label_size_standard)
plt.tick_params(axis='x', labelsize=label_size_standard)

#codigo horrivel, mas funciona
# tem que dar sorted com relaçao a coordenada x
# senao o plot fica errado, fora de ordem as conexoes
color_plots_static = '#EB6E14'
x_plot, y_plot = zip(*sorted(zip(x_static, y_static),key=lambda x: x[0]))
ax1.plot(x_plot, y_plot, label = r'$p_d = 0$', color = color_plots_static, alpha=0.75, linestyle='dotted')

left, bottom, width, height = [0.2, 0.65, 0.2, 0.2]
ax2 = fig.add_axes([left, bottom, width, height])

ax2.plot(x_plot, y_plot, label = r'$p_d = 0$', color = color_plots_static, alpha=0.75, linestyle='dotted')

index = 0
for key in sorted(cooperation_dict.keys()):
    if key in [0.01, 0.05, 0.1, 0.5, 1.]:
        size = 20
        if key == 1.:
            size = 12
        if key == 0.1:
            size = 30
        color_both_plots = next(color)
        iteration_marker = next(marker)
        ax1.scatter(*zip(*cooperation_dict[key]),  marker = iteration_marker, linestyle='', label = r'$p_d = $' + str(key), color = color_both_plots, s = size)
        
        ax2.scatter(*zip(*cooperation_dict[key]),  marker = iteration_marker, linestyle='', label = r'$p_d = $' + str(key), color = color_both_plots, s = size)
        
        #plt.plot(*zip(*cooperation_dict[key]), linewidth = 0.5, alpha=0.4, color = color_both_plots)
        index += 1

plt.title('')
ax1.set_ylim(-0.02, 1.)
ax1.set_xlim(0.075, 1.01)
ax2.set_xlim(0.9745, 1.001)
ax2.set_ylim(.0, .4)
ax1.set_xlabel(r'$\rho$')
ax1.set_ylabel(r'$f_c$')
ax1.legend(loc='best', ncol = 2, edgecolor = 'black', framealpha=0.5, prop={'size': 12})
plt.savefig('cooperation_versus_b-per_occupation-async-stochastic.png', dpi=400, bbox_inches='tight')

plt.close()
plt.clf()
plt.cla()

marker = itertools.cycle((',', 'P', 'p', '*', '.', 'X', 'P', 'p', 'o'))
color  = itertools.cycle(("#0E56FD", "#6135ca", "#606b9b", "#4AA6B5", "#335430", "#d02f6a", "#e61976", "#ff1611"))

plt.plot(x_plot, y_plot, label = r'$p_d = 0$', color = color_plots_static, alpha=0.75, linestyle='dotted')

index = 0
for key in sorted(cooperation_dict.keys()):
    if key in [0.01, 0.03, 0.05, 0.5, 1.]:
        size = 20
        if key == 1.:
            size = 12
        if key == 0.1:
            size = 30
        color_both_plots = next(color)
        plt.scatter(*zip(*cooperation_dict[key]),  marker = next(marker), linestyle='',
            label = r'$p_d = $' + str(key), color = color_both_plots)
        #plt.plot(*zip(*cooperation_dict[key]), linewidth = 0.5, alpha=0.4, color = color_both_plots)
        index += 1

plt.title('')
plt.xlim(0.9745, 1.0005)
plt.xlabel(r'$\rho$')
plt.ylabel(r'$f_c$')
#plt.legend(loc='best', ncol = 2, edgecolor = 'black', framealpha=0.5, prop={'size': 12})
plt.savefig('cooperation_versus_b-per_occupation-async-zoom-stochastic.png', dpi=400, bbox_inches='tight')

plt.close()
plt.clf()
plt.cla()

color = itertools.cycle(("#0E56FD", "#6135ca", "#606b9b", "#ca23dc",  "#e61976", "#d02f6a", "#ff1611"))
marker = itertools.cycle((',', 'P', 'p', '*', 'X', 'P', 'p', 'o'))

index = 0
for key in sorted(variance_dict.keys()):
    if key in [0.01, 0.03, 0.05, 0.1, 0.5, 1.]:
        color_both_plots = next(color)
        plt.scatter(*zip(*variance_dict[key]),  marker = next(marker), linestyle='',
            label = r'$p_d = $' + str(key), color = color_both_plots)
        #plt.plot(*zip(*cooperation_dict[key]), linewidth = 0.5, alpha=0.4, color = color_both_plots)
        index += 1

plt.title('')
plt.xlabel(r'$\rho$')
plt.ylabel(r'$\sigma ^2$')
#plt.legend(loc='upper right', ncol = 2, edgecolor = 'black', framealpha=0.5)
plt.savefig('variance_versus_b-per_occupation-async-stochastic.png', dpi=400, bbox_inches='tight')

"""index = 0
for filename in glob.glob(path + 'T*.dat'):
    data = pd.read_csv(filename, comment = '#', delimiter = ' ', names = colnames_dynamic, index_col = False)
    plot_data_values(filename, data, colnames_dynamic, color, 'q-table')
    index += 1"""

'''
#print(temptation, mean_cooperation)
plt.plot(*zip(*cooperation_per_episode), label = str(temptation), color = color[index % len(color)])
index += 1

plt.savefig('cooperation-time_series.png', dpi = 400, bbox_inches='tight')
plt.clf()'''
