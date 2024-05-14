import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams as rcp
from matplotlib.cm import ScalarMappable
from tqdm import tqdm
from matplotlib import cm
from matplotlib.ticker import LinearLocator

rcp['font.family'],rcp['font.serif'] = 'serif', ['Computer Modern Roman']
rcp['text.usetex'] = True
rcp['font.size'], rcp['axes.labelsize'],rcp['axes.titlesize'] = 16, 16,18
rcp['xtick.labelsize'],rcp['ytick.labelsize'] = 14, 14

nf = np.load("data/005.npz")

trades = nf["trades"]

num_up = np.sum(trades > 0)
num_down = np.sum(trades < 0)
updownratio = num_up/num_down
print("Up/Down Ratio: ",updownratio)
print("Profit: ",sum(trades)/1_000_000*100)

fig, ax = plt.subplots(1,1,figsize=(5,2))
ax.hist(trades,bins=50,density=True)
ax.set_xlabel("Profit/Loss per Trade")
ax.set_ylabel("Density")
ax.set_xlim(left=-4e5,right=4e5)

plt.subplots_adjust(wspace=0.3, hspace=0.4)
fig.savefig('img/005.pdf', bbox_inches='tight')
plt.show()


print("Up/Down Ratio", updownratio)
print("Total Return: ",np.sum(trades))
print(len(trades))
