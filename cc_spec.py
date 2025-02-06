# A python script to evaluate the Pearson's correlation spectrum between /
# eta and surface air temperature.

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import pandas as pd
from datetime import datetime,timedelta
import math,os
from tqdm import tqdm


def dateRange(beginDate,endDate):
    dates=[]
    dt = datetime.strptime(beginDate,'%Y-%m-%d')
    date = beginDate[:]
    while date<=endDate:
        dates.append(dt)
        dt = dt + timedelta(1)
        date = dt.strftime('%Y-%m-%d')
    return dates

def normalization(data):
    data -= np.mean(data)
    return data/np.max(data)

def moving_average(data, windowsize):
    window = np.ones(int(windowsize))/float(windowsize)
    re = np.convolve(data, window, 'same')
    return re


# Read surface air temperature
with open('ERA5/ERA5.txt') as f:
    cat = f.readlines()
f.close()
dates2,tem,sps,sds = [],[],[],[]
for i in range(len(cat)):
    line = cat[i].split()
    dates2.append(datetime.strptime(line[0],'%Y-%m-%d'))
    tem.append(float(line[1]))
    sps.append(float(line[2]))
    sds.append(float(line[3]))
dates2,tem = np.array(dates2),np.array(tem)

# Creat an output folder 'etas'
output_path = 'etas'
if not os.path.exists(output_path):
    os.makedirs(output_path)


# Read eta from "output" folder of eta.py
stack = '10'    # select NCFs with 10-day-stacking
ref_sts = ['MA1','MA2','MA3','MA4','MA6','MA7','MEI05']   # reference station list
sr = 200   # sampling rate of NCFs
data_len = 1201
mov_size = 30

matrix = np.zeros((len(ref_sts),600))
matrix2 = np.zeros((len(ref_sts),600))
for i in tqdm(range(len(ref_sts))):
    etas = np.load('output/%sd_%s.npy'%(stack,ref_sts[i]))
    rs = []
    for f in range(etas.shape[1]):
        eta = etas[:,f]
        eta1 = pd.DataFrame(eta)
        eta1 = np.array(eta1.interpolate(method='nearest'))[:,0]        
        tem1 = tem[239:239+len(eta1)]

        eta1 = moving_average(eta1,mov_size)[mov_size:-mov_size]
        tem1 = moving_average(tem1,mov_size)[mov_size:-mov_size]
        eta1 = normalization(eta1)
        tem1 = normalization(tem1)
        r,p = pearsonr(eta1,tem1)
        rs.append(r)
    matrix[i,:] = np.array(rs)





plt.figure(figsize=[9,4])
plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'
freqs = np.linspace(0,sr/2,int(data_len/2))
plt.pcolormesh(freqs,[ ]+ref_sts,matrix,cmap='seismic',
               shading='auto',vmin=-1,vmax=1)
cb = plt.colorbar(pad=0.03,ticks=np.arange(-1,1.1,0.5))
cb.set_label("Pearson CC value",size=16)
cb.ax.tick_params(labelsize=14)
plt.xlabel('Frequency (Hz)',fontsize=16)
plt.ylabel('Reference station',fontsize=16)
plt.title('Correlation between $\Delta \eta$ and $T$',weight='bold',fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.savefig(os.path.join(output_path,'cc.jpg'),bbox_inches='tight',dpi=400)
plt.close()




