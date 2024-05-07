import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams as rcp
from constants import *

rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

npzf = np.load("data/returnsMV.npz")
weights_ = npzf["weights_"]
weights = npzf["weights"]

fig, ax1 = plt.subplots(2,1,figsize=(10,5))
color = 'tab:red'
ax1[0].set_xlabel("Asset Index")
ax1[0].set_ylabel("Weight")
#ax1.tick_params(axis='y', labelcolor=color)
ax1[0].stem(weights,label="$\hat{k} > k$")
ax1[0].set_title("Without Enforcing Cardinality")
ax1[0].legend()

ax1[1].stem(weights_,label="$\hat{k} = k$")
ax1[1].set_title("Enforcing Cardinality")
ax1[1].set_xlabel("Asset Index")
ax1[1].set_ylabel("Weight")
ax1[1].legend()

plt.subplots_adjust(wspace=0.3, hspace=0.8)
fig.savefig('img/0025.pdf', bbox_inches='tight')