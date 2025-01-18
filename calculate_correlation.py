import glob
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from   numpy import genfromtxt

def plot_corr(key_list, corr_list):
    plt.scatter(key, corr_list)
    plt.save('correlation-specific-example.png', dpi = 400)

path = './data/stochastic-choosing-the-best-and-mantain/snapshots/snapshots-for-corr/'
L = 100

states  = {}
actions = {}

for filename in glob.glob(path + '*.dat'):

    key = int(filename.split('Step')[1].split('_')[0])
    if '(0)' in filename:
        data_states = genfromtxt(filename, delimiter=',')
        data_states = data_states.reshape(L, L)
        states[key] = data_states

    elif '(1)' in filename:
        data_actions = genfromtxt(filename, delimiter=',')
        data_actions = data_actions.reshape(L, L)
        #in this way, holes are 0 in both representations
        data_actions = data_actions + 1
        #ad hoc, assume all compare and stay are cooperators
        data_actions[data_actions == 2] = 1
        data_actions[data_actions == 1] = 1
        #changing variable dummy label
        data_actions[data_actions == 3] = -1
        actions[key] = data_actions

states  = collections.OrderedDict(sorted(states.items()))
actions = collections.OrderedDict(sorted(actions.items()))


correlation_list = []
key_list         = []

for key in states.keys():
    corr = np.corrcoef(states[key].flatten(), actions[key].flatten())
    correlation_list.append(float(corr[1,0]))
    key_list.append(key)

plt.plot(key_list, correlation_list)
plt.savefig('correlation_example.png', dpi = 400)
