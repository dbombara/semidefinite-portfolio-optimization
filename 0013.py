import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from constants import *
from matplotlib import rcParams as rcp
from matplotlib.cm import ScalarMappable
from tqdm import tqdm
from matplotlib import cm
from matplotlib.ticker import LinearLocator

rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

str1 = "Number of Stocks"

try:
    nf = np.load("data/EfficientFrontierNumStocks.npz")
except:
    nf = np.load("data/0013.npz")
    
returns, variance = nf["returns"], nf["variance"]
obj_val = nf["obj_val"]
num_stocks = nf["num_stocks"]

### Get meshgrid
var1, var2 = np.meshgrid(risk_pref_vec,num_stocks)

### Plot Returns
fig, ax = plt.subplots(subplot_kw={"projection":"3d"})
surf = ax.plot_surface(var1, var2, returns,cmap=cm.coolwarm,linewidth=0, antialiased=False)
ax.set_title("Returns")
ax.set_xlabel("Risk")
ax.set_ylabel(str1)
fig.colorbar(surf, shrink=0.5,aspect=5)
fig.savefig("img/0013a.pdf", bbox_inches='tight')

### Plot Variance
fig, ax = plt.subplots(subplot_kw={"projection":"3d"})
surf = ax.plot_surface(var1, var2, variance,cmap=cm.coolwarm,linewidth=0, antialiased=False)
ax.set_title("Variance")
ax.set_xlabel("Risk")
ax.set_ylabel(str1)
fig.colorbar(surf, shrink=0.5,aspect=5)
fig.savefig("img/0013b.pdf", bbox_inches='tight')

### Plot Objective Function Value
fig, ax = plt.subplots(subplot_kw={"projection":"3d"})
surf = ax.plot_surface(var1, var2, variance,cmap=cm.coolwarm,linewidth=0, antialiased=False)
ax.set_title("Objective Value")
ax.set_xlabel("Risk")
ax.set_ylabel(str1)
fig.colorbar(surf, shrink=0.5,aspect=5)
fig.savefig("img/0013c.pdf", bbox_inches='tight')