import numpy as np
import pandas as pd
import glob
import io
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools

def plot_heatmap(x_list, y_list, cooperation_list):
    '''
    Plot the heatmap

    Returns:
    (void)
    '''
    x = np.array(x_list)
    y = np.array(y_list)
    z = np.array(cooperation_list)

    plt.xlabel(r'$\rho$')
    plt.ylabel(r'$p_d$')

    #plt.gca().invert_yaxis()

    plt.ylim(0.01, 1.)
    plt.xlim(0.07, 1.)
    plt.yticks([.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.])

    plt.tricontourf(x, y, z, levels = 80, cmap = 'jet_r')
    cbar = plt.colorbar()
    cbar.set_ticks(np.arange(0, 1.01, 0.1))

    plt.savefig('heatmap_coop_versus_prob-diff-fermi.png', dpi=400, bbox_inches='tight')
    plt.clf()

    return

def plot_separate_column(colnames, color):
    for column in colnames:
        if column[2] == 'b':
            plt.plot(data[['t']].to_numpy(), data[[column]].to_numpy(),
                color = next(color), label = r'$Q_{{{}}}$'.format(column[1:]))
    plt.legend(loc = 'best')
    plt.savefig(filename + 'q-table-for-d.png', dpi = 400, bbox_inches='tight')
    plt.close()

    for column in colnames:
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

path = './data/fermi/'

cooperation_dict = {}
variance_dict    = {}
colnames = ['t',  'f_c',  'f_d', 'r_m', 'Qdb',  'Qcb', 'Qdm', 'Qcm']

labels_to_plot = []
x_axis_to_plot = []
cooperation_plot = []

x_static = []
y_static = []

check_repeat_params = []

index = 0
for filename in glob.glob(path + 'T*.dat'):
    data = pd.read_csv(filename, comment = '#', delimiter = ' ', names = colnames, index_col = False)

    key = float(filename.split('P_DIFFUSION')[1][0:4])

    data['mean_coop'] = data['f_c'] / (data['f_d'] + data['f_c'])

    try:
        x_variable  = float(filename.split('rho')[1][:6])
        mean_coop   = np.mean(data[['mean_coop']].to_numpy()[-100:])
        var_coop    = np.var(data[['mean_coop']].to_numpy()[-100:])

        '''if np.random.rand() < 0.1:
            plot_data_values(filename, data, colnames, color, 'q-table')
            plot_data_values(filename, data, colnames, color, 'cooperation')'''

        if key == 0.:
            x_static.append(x_variable)
            y_static.append(mean_coop)

        if x_variable > 0.001 and (not ([key, x_variable] in check_repeat_params)):
            labels_to_plot.append(key)
            x_axis_to_plot.append(x_variable)
            cooperation_plot.append(mean_coop)

            if key in (cooperation_dict.keys()):
                cooperation_dict[key].append([x_variable, float(mean_coop)])
                variance_dict[key].append([x_variable, float(var_coop)])
            else:
                cooperation_dict[key] = [[x_variable, float(mean_coop)]]
                variance_dict[key] = [[x_variable, float(var_coop)]]

            check_repeat_params.append([key, x_variable])

        index += 1
    except:
        print('Unavailable data for' + filename)

plt.rc('axes', labelsize=16)

#plot_heatmap(x_axis_to_plot, labels_to_plot, cooperation_plot)

plt.style.use('seaborn-v0_8-ticks')

###################
### normal plot ###
###################

#codigo horrivel, mas funciona
# tem que dar sorted com relaçao a coordenada x
# senao o plot fica errado, fora de ordem as conexoes
color_plots_static = '#EB6E14'
x_plot, y_plot = zip(*sorted(zip(x_static, y_static),key=lambda x: x[0]))
plt.plot(x_plot, y_plot, label = r'$p_d = 0$', color = color_plots_static, alpha=0.75, linestyle='dotted')

marker = itertools.cycle((',', 'P', 'p', '*', '.', 'X', 'P', 'p', 'o'))
color  = itertools.cycle(("#0E56FD", "#6135ca", "#606b9b", "#4AA6B5", "#335430", "#d02f6a", "#e61976", "#ff1611"))

index = 0
for key in sorted(cooperation_dict.keys()):
    if key in [0.01, 0.05, 0.1, 0.5, 1.]:
        size = 20
        if key == 1.:
            size = 10
        if key == 0.1:
            size = 30
        color_both_plots = next(color)
        plt.scatter(*zip(*cooperation_dict[key]),  marker = next(marker), linestyle='',
            label = r'$p_d = $' + str(key), color = color_both_plots, s = size)
        #plt.plot(*zip(*cooperation_dict[key]), linewidth = 0.5, alpha=0.4, color = color_both_plots)
        index += 1

plt.title('')
plt.ylim(-0.01, 1.01)
plt.xticks(np.arange(0.1, 1.001, 0.1))
plt.xlim(0.07, 1.05)
plt.xlabel(r'$\rho$')
plt.ylabel(r'$f_c$')
plt.legend(loc='upper right', ncol = 1, edgecolor = 'black', framealpha=0.5)
plt.savefig('cooperation_versus_b-per_occupation-fermi.png', dpi=400, bbox_inches='tight')

plt.close()
plt.clf()
plt.cla()

marker = itertools.cycle((',', 'P', 'p', '.', '*', 'X', 'P', 'p', 'o'))
color = itertools.cycle(("#0E56FD", "#6135ca", "#606b9b", "#ca23dc",  "#e61976", "#d02f6a", "#ff1611"))

###################
### zoom plot   ###
###################
plt.plot(x_plot, y_plot, label = r'$p_d = 0$', color = color_plots_static, alpha=0.75, linestyle='dotted')

index = 0
for key in sorted(cooperation_dict.keys()):
    if key in [0.05]:
        color_both_plots = next(color)
        plt.scatter(*zip(*cooperation_dict[key]),  marker = 'P', linestyle='',
            label = r'$p_d = $' + str(key), color = "#6135ca")
        #plt.plot(*zip(*cooperation_dict[key]), linewidth = 0.5, alpha=0.4, color = color_both_plots)
        index += 1

plt.title('')
plt.ylim(-0.01, 1.01)
plt.xlim(0.07, .16)
plt.xlabel(r'$\rho$')
plt.ylabel(r'$f_c$')
#plt.legend(loc='upper right', ncol = 1, edgecolor = 'black', framealpha=0.5)
plt.savefig('cooperation_versus_b-per_occupation-fermi-zoom.png', dpi=400, bbox_inches='tight')

plt.close()
plt.clf()
plt.cla()

###################
### var plot    ###
###################

marker = itertools.cycle((',', 'P', 'p', '.', '*', 'X', 'P', 'p', 'o'))
color = itertools.cycle(("#0E56FD", "#6135ca", "#606b9b", "#ca23dc",  "#e61976", "#d02f6a", "#ff1611"))

index = 0
for key in sorted(variance_dict.keys()):
    color_both_plots = next(color)
    plt.scatter(*zip(*variance_dict[key]),  marker = next(marker), linestyle='',
        label = r'$p_d = $' + str(key), color = color_both_plots)
    #plt.plot(*zip(*cooperation_dict[key]), linewidth = 0.5, alpha=0.4, color = color_both_plots)
    index += 1

plt.title('')
plt.xlabel(r'$\rho$')
plt.ylabel(r'$\sigma ^2$')
#plt.legend(loc='upper right', ncol = 2, edgecolor = 'black', framealpha=0.5)
plt.savefig('variance_versus_b-per_occupation-fermi.png', dpi=400, bbox_inches='tight')
