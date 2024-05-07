import numpy as np
import matplotlib.pyplot as plt
from constants import *

## Parameters for Plotting
from matplotlib import rcParams as rcp
rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

npzf = np.load("data/riskpref.npz")
mean_returns = npzf['mean_returns']
mean_var = npzf['mean_var']
m_obj = npzf['m_obj']

fig, ax = plt.subplots(1,3, figsize=(10,5))

ax[0].plot(risk_pref_vec,m_obj,label="Obj. Value",marker="o") # objective function value
ax[0].set_xlabel("Risk Preference")
ax[0].set_ylabel("Obj. Value")
#
ax[1].plot(risk_pref_vec,mean_returns,label="Returns",marker="o")
ax[1].set_xlabel("Risk Preference")
ax[1].set_ylabel("Expected Portfolio Return")
ax[1].set_title("Risk Preference Effects with $k=5$")
#
ax[2].plot(risk_pref_vec, mean_var,label="Variance",marker="o")
ax[2].set_xlabel("Risk Preference")
ax[2].set_ylabel("Portfolio Variance")
#
plt.subplots_adjust(wspace=0.5, hspace=0.7)
fig.savefig('img/0026.pdf', bbox_inches='tight')