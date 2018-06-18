"""
Modified on Mon 18 Jun 2018
@author: Kamieljv (GitHub)
histogram.py:
    plot histograms of values on a spatial grid.
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

twt_cnt = np.array([])
bd_cnt = np.array([])
root_dir = '' # root directory of file
filename = ''
with open(root_dir+filename+'.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        if line[0]=='id':
            print(line)
        else:
            #loading the data per cell. Note: line indexes depend on data file.
            twt_cnt = np.append(twt_cnt, [int(line[6])]) #load tweet counts
            bd_cnt = np.append(bd_cnt, [int(float(line[11]))]) #load building counts
            rd_len = np.append(rd_len, [float(line[8])]) #load road lengths
print('=> Loaded the data.')

# -------- Computing basic stats ----------------

def basic_stats(array):
    mode = stats.mode(array)[0][0]
    median = np.median(array)
    avg = np.average(array)
    min = np.min(array)
    max = np.max(array)
    skew = stats.skew(array)
    nonz = np.count_nonzero(array)
    print('Mode: {}\nMedian: {}\nAverage: {}\nMin: {}\nMax: {}\nSkew: {}\nNonzero: {}'.format(mode, median, avg, min, max, skew, nonz))
    return mode, median, avg, min, max, skew

print('-----------------------------------\nBasic stats for Tweet Count:')
basic_stats(twt_cnt)
print('-----------------------------------\nBasic stats for Road Length:')
basic_stats(rd_len)
print('-----------------------------------\nBasic stats for Building Count:')
basic_stats(bd_cnt)


# ---- Plot tweets histogram -----
max_twt = twt_cnt.max()
nrbins_twt = int(max_twt+1)
hist = np.histogram(twt_cnt, bins=nrbins_twt)
freq_twt = hist[0]
bins_twt = hist[1]
end_twt = 500

x = np.linspace(0,end_twt-1,end_twt)
y = freq_twt[:end_twt]
plt.bar(x,y,log=1)
plt.title("Distribution of Tweets per Cell")
plt.xlabel('Nr. of Tweets')
plt.ylabel('Frequency')
axes = plt.gca()
axes.set_ylim([0.5,2000])
plt.show()

# ---- Plot building histogram -----

max_bd = bd_cnt.max()
nrbins_bd = int(max_bd+1) #define number of bins
hist = np.histogram(bd_cnt, bins=nrbins_bd)
freq_bd = hist[0]
bins_bd = hist[1]
end_bd = 300 #maximum number of buildings per cell (higher will not be plotted)

x = np.linspace(0,end_bd-1,end_bd)
y = freq_bd[:end_bd]
plt.bar(x,y,log=1, color='red')
plt.title("Number of Buildings")
plt.xlabel('number of buildings')
plt.ylabel('frequency')
plt.show()