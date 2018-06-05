"""
Modified on Tue 5 Jun 2018
@author: Kamieljv (GitHub)
SpearmanRank_global.py:
    compute the Spearman Rank Correlation globally, for values on a spatial grid
"""

from scipy import stats as scst
import csv
import numpy as np
import matplotlib.pyplot as plt

twt_cnt = np.array([])
bd_cnt = np.array([])
rd_len = np.array([])
root_dir = '' #file directory
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

print("Tweet count: ",twt_cnt)
print("Building count: ",bd_cnt)
print("Road length: ",rd_len)

print('Spearman Rank tweet vs buildings: ',scst.spearmanr(bd_cnt,twt_cnt))
print('Spearman Rank tweet vs roads: ',scst.spearmanr(rd_len,twt_cnt))