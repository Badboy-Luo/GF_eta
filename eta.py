# This python script shows how to calculate changes in geometric phase (eta) /
# after obtaining seismic noise correlation functions. 
# The output includes a time-frequency plot of eta by setting a reference /
# station and several eta time series at different frequencies.

from obspy import read
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.ndimage import gaussian_filter
from datetime import datetime,timedelta
import math,os
from tqdm import tqdm
from fnmatch import fnmatch


def dateRange(beginDate,endDate):
    dates=[]
    dt = datetime.strptime(beginDate,'%Y-%m-%d')
    date = beginDate[:]
    while date<=endDate:
        dates.append(dt)
        dt = dt + timedelta(1)
        date = dt.strftime('%Y-%m-%d')
    return dates




# Read surface air temperature data
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
tem = gaussian_filter(tem,2)



ref_st = 'MA1'    # set the reference station: MA1, MA2, MA4, MA6, MA7, MEI05
sr = 200    # sampling rate of NCFs
path = 'CCFs'    # directory of all daily NCFs
pairs = [file for file in os.listdir(path) if fnmatch(file,'*%s*'%ref_st)]


# Build the reference vector
ref_allday = []
for ref_d in dateRange('2020-01-01','2020-01-31'):
    ref_mag = 0
    ref_daily_vectors = []
    num = 0
    for i in range(len(pairs)):
        try:
            st = read(os.path.join(path,pairs[i],str(ref_d).split()[0]+'.MSEED'))
        except FileNotFoundError:
            num = 0
            break
        num += 1
        data = st[0].data
        f = fft(data)[:int(len(data)/2)]
        ref_daily_vectors.append(f)
        ref_mag += abs(f)**2
    if num == 0:
        continue
    else:
        ref_allday.append(np.array(ref_daily_vectors)/np.sqrt(ref_mag))
ref_vectors = np.mean(np.array(ref_allday),axis=0)


# Calculate daily eta with respect to reference vector
dates = dateRange('2019-08-28','2021-07-18')  # create a date range
etas = []
for d in tqdm(range(len(dates))):
    sum_mag = 0
    vectors = []
    for i in range(len(pairs)):
        num = len(pairs)
        try:
            st = read(os.path.join(path,pairs[i],str(dates[d]).split()[0]+'.MSEED'))
            data = st[0].data
            f = fft(data)[:int(len(data)/2)]
            vectors.append(f)
            sum_mag += abs(f)**2
        except FileNotFoundError:
            num = 0
            break
    if num == len(pairs):
        vectors = np.array(vectors)/np.sqrt(sum_mag)
        eta = []
        for f in range(vectors.shape[1]):
            cdot = np.dot( np.conj([ref_vectors[:,f]]), vectors[:,f] )
            try:
                eta.append(math.acos(cdot.real))
            except ValueError:
                eta.append(math.acos(1))
        etas.append(np.array(eta))
    else:
        etas.append(np.zeros_like(eta) * np.nan)
etas = np.array(etas)


# Save eta as .npy files
# if not os.path.exists('output'):
#     os.makedirs('output')
# np.save(os.path.join('output','10d_%s.npy'%ref_st), etas)
# with open(os.path.join('output','10d_%s.txt'%ref_st), 'a+') as f:
#     for d in dates:
#         f.write(str(d).split()[0] + '\n')
# f.close()



xloc = [datetime(2020,1,1),
        datetime(2020,7,1),datetime(2021,1,1),datetime(2021,7,1)]
xlabel = ['2020-01','2020-07','2021-01','2021-07']

# Plot eta at certain frequencies
output_path = 'etas'
if not os.path.exists(output_path):
    os.makedirs(output_path)
freqs = [25,30,35,40]   
plt.figure(figsize=[5,8])
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
for f in range(len(freqs)):
    ind = int('%s1%s'%(len(freqs),f+1))
    ax = plt.subplot(ind)
    ax2 = ax.twinx()
    ax2.plot(dates2,tem,c='r',lw=1.5,alpha=0.8)    
    freq_len = etas.shape[1]
    eta = np.mean(etas[:,int(freqs[f]*(freq_len/(sr/2))):
                int((freqs[f]+5)*(freq_len/(sr/2)))], axis=-1)

    ax.plot(dates,eta,lw=1.5,c='k',label='%s Hz'%freqs[f])
    ax.axvspan(datetime(2020,1,1),datetime(2020,1,31),
            color='gray',alpha=0.3,label='reference period')
    if f == len(freqs)-1:
        ax.set_xticks(xloc)
        ax.set_xticklabels(xlabel,fontsize=12)
    else:
        ax.set_xticks(xloc)
        ax.set_xticklabels(len(xloc)*[])
    ax2.set_yticks([-10,-5,0,5,10])
    ax2.set_yticklabels([-10,-5,0,5,10],color='r')
    ax2.set_ylim(-10,15)
    ax2.set_ylabel('Surface T ($\circ C$)',color='red',fontsize=12)
    ax.set_ylabel('$\Delta \eta$ ($rad$)',fontsize=13)
    ax.grid(linestyle=':')
    plt.xlim(datetime(2019,9,1),dates[-1])
    plt.title('ref_sta=%s, %s-%s Hz'%(ref_st,freqs[f],freqs[f]+5),fontsize=12,weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_path,'eta_10d_%s.png'%ref_st)
            ,bbox_inches='tight',dpi=200)




# Display time-frequency plot of eta
plt.figure(figsize=[9,4])
plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'
data_len = etas.shape[1]*2
freqs_axis = np.linspace(0,sr/2,int(data_len/2))
plt.pcolormesh(freqs_axis,dates,etas,vmin=1.4,vmax=1.8, shading='auto')
plt.ylim(dates[0],dates[-1])
plt.yticks(xloc,xlabel,fontsize=14)
plt.xlim(0,100)
plt.xticks(fontsize=14)
plt.xlabel('Frequency (Hz)',fontsize=16)
cb = plt.colorbar(extend='both')
cb.set_label('$\Delta \eta$ ($rad$)',size=16)
cb.ax.tick_params(labelsize=14)
plt.title('Function of $\Delta \eta (\omega, t)$, ref_sta=%s'%ref_st,weight='bold',fontsize=18)
plt.grid(linestyle='dotted')
plt.savefig(os.path.join(output_path,'tf_10d_%s.jpg'%ref_st)
            ,bbox_inches='tight',dpi=400)





