from scipy import stats as scst
from scipy import optimize as opt
import csv
import numpy as np
import matplotlib.pyplot as plt
import math
np.set_printoptions(threshold=np.nan)

#Reading the data file
twt_cnt = np.array([])
bd_cnt = np.array([])
rd_len = np.array([])
sat_binary = np.array([])
ids = np.array([])
with open('C:/Users/Kamiel/Documents/UT/Semester 6/Thesis/QGIS/Kenya_vecGrid_0025deg_case_ided_rdLen_build_twtCnt_20180526_labeled.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        if line[0]=='id':
            print(line)
        else:
            twt_cnt = np.append(twt_cnt, [int(line[6])]) #Structure: ['id', 'xmin', 'xmax', 'ymin', 'ymax', 'loc_id', 'twt_cnt', 'twt_cnt_n', 'rd_len', 'rd_cnt', 'rd_len_n', 'bd_cnt', 'bd_cnt_n', 'lbls']
            bd_cnt = np.append(bd_cnt, [int(line[11])])
            rd_len = np.append(rd_len, [float(line[8])])
            sat_binary = np.append(sat_binary, [int(line[13])])
            ids = np.append(ids, [int(line[0])])
print('=> Loaded the data.')

def f(x, a, b):
    return a*x**2 + b

#creating paired list
i=0
length = len(twt_cnt)
pairs = np.zeros((length,3))
for id, rd, twt in zip(ids, rd_len, twt_cnt):
    pairs[i] = [id, rd, twt]
    i+=1

#printing percentiles
steps = np.linspace(80,100,21)
for p in steps:
    percentile = np.percentile(pairs, p, axis=0)
    print('%s-th percentile Tweets:    ' %p + str(percentile[2]))

#cut of percentiles
# pairs = pairs[pairs[:,2].argsort()]
# cut_p = 0.99 #cut off last percentile
# cut = int(cut_p * length)
# pairs = pairs[:cut]

sigma = np.ones(len(pairs))
sigma[0] = 0.000001
popt, pcov = opt.curve_fit(f, pairs[:,1], pairs[:,2], sigma=sigma)
a, b = popt
max = max(pairs[:,1])
x = np.linspace(0,max,100)
plt.plot(x, f(x, a, b))
plt.scatter(pairs[:,1], pairs[:,2], c='r', marker='.')
plt.show()

model_pred = f(rd_len, a, b)
model_pred = [0 if pred<0 else pred for pred in model_pred]

#write results to a csv
# root_dir = 'C:/Users/Kamiel/Documents/UT/Semester 6/Thesis/QGIS/'
# with open(root_dir+'fit_secondorder_perc1-99_roadLen_Tweets_20180529.csv', 'w', newline='') as file:
#     csvwriter = csv.writer(file, delimiter=',')
#     for i, id in enumerate(ids):
#         csvwriter.writerow([id, round(model_pred[i],4)])
# print('=> File written.')
