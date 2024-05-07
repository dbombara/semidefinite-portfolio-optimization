import numpy as np
import matplotlib.pyplot as plt
from constants import *
from matplotlib import rcParams as rcp
rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

outfile = "data/computationtime.npz"
npzfile = np.load(outfile)

num_stocks = npzfile['num_stocks']
mean_time = npzfile['mean_time']
std_time = npzfile['std_time']
m_obj = npzfile['m_obj']

fig, ax = plt.subplots(2,1, figsize=(10,5))
ax[0].plot(num_stocks,mean_time,label="Time")
ax[0].fill_between(num_stocks, mean_time - std_time, mean_time + std_time, facecolor='blue', alpha=0.5)
ax[0].set_xlabel("Number of Stocks")
ax[0].set_ylabel("Time")
ax[0].set_title("Mean-Variance Opt., $k=5$")
#
ax[1].plot(num_stocks,m_obj,label="Obj. Value") # objective function value
ax[1].set_xlabel("Number of Stocks")
ax[1].set_ylabel("Obj. Value")

plt.subplots_adjust(wspace=0.3, hspace=0.4)
fig.savefig('img/0022p.pdf', bbox_inches='tight')