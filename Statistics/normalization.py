"""
Modified on Mon 18 Jun 2018
@author: Kamieljv (GitHub)
normalization.py:
    normalizing skewed data, for tweets, roads and buildings
    plotting the normalized data
    exporting the data as csv
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.nan)

twt_cnt = np.array([])
bd_cnt = np.array([])
rd_len = np.array([])
twt_kd = np.array([])
ids = np.array([])
root_dir = '' #folder to containing data file
filename = '' #name of data file
with open(root_dir+filename+'.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        if line[0]=='id':
            print(line)
        else:
            ids = np.append(ids, [int(line[0])])
            twt_cnt = np.append(twt_cnt, [int(line[17])])
            twt_kd = np.append(twt_kd, [float(line[19])])
            bd_cnt = np.append(bd_cnt, [int(line[8])])
            rd_len = np.append(rd_len, [float(line[6])])

print('=> Loaded the data.')

#couple data with ids
twt_kd = np.array([[id, val] for (id, val) in zip(ids, twt_kd)])
rd_len = np.array([[id, val] for (id, val) in zip(ids, rd_len)])
bd_cnt = np.array([[id, val] for (id, val) in zip(ids, bd_cnt)])

def lin_normalize(array):
    min = np.min(array)
    max = np.max(array)
    return np.divide(array - min, max - min)

# ---- Normalize Tweet Kernel Density -----
twt_sorted = np.array(sorted(twt_kd, key=lambda l:l[1],reverse=False)) #sort on tweet density
twt_sorted_cutoff = np.array([val if val[1]>0.001 else [val[0],0.001] for val in twt_sorted]) #implement a twt_dens cutoff at 0.001
twt_log2 = np.array([np.log(val)/np.log(2) for val in twt_sorted_cutoff]) #log2 transformation

twt_sorted[:,1] = lin_normalize(twt_sorted[:,1]) #normalize to [0, 1] range
lin_norm_twt = twt_sorted

twt_log2[:,1] = lin_normalize(twt_log2[:,1]) #normalize to [0, 1] range
log2_norm_twt = twt_log2


# ---- Normalize Road length -----
rd_sorted = np.array(sorted(rd_len, key=lambda l:l[1],reverse=False))
rd_sorted_cutoff = np.array([val if val[1]>0.001 else [val[0],0.001] for val in rd_sorted])
rd_log2 = np.array([np.log(val)/np.log(2) for val in rd_sorted_cutoff])

rd_sorted[:,1] = lin_normalize(rd_sorted[:,1])
lin_norm_rd = rd_sorted

rd_log2[:,1] = lin_normalize(rd_log2[:,1])
log2_norm_rd = rd_log2

# ---- Normalize Building count
bd_sorted = np.array(sorted(bd_cnt, key=lambda l:l[1],reverse=False))
bd_sorted_cutoff = np.array([val if val[1]>1 else [val[0],1] for val in bd_sorted])
bd_log2 = np.array([np.log(val)/np.log(2) for val in bd_sorted_cutoff])

bd_sorted[:,1] = lin_normalize(bd_sorted[:,1])
lin_norm_bd = bd_sorted

bd_log2[:,1] = lin_normalize(bd_log2[:,1])
log2_norm_bd = bd_log2

# -----Plotting ---------
x = np.linspace(1,len(rd_len), len(rd_len))
fig, ax = plt.subplots()
ax.plot(x, lin_norm_twt[:,1], 'b-', label='Lin.Norm. Tweets')
ax.plot(x, log2_norm_twt[:,1], 'b--', label='Log2-Norm. Tweets')
ax.plot([x[8219],x[-1]],[0,1], linestyle='--', color='gray', label='Ideal line')
# ax.plot(x, lin_norm_rd[:,1], 'r-', label='Lin.Norm. Roads')
# ax.plot(x, log2_norm_rd[:,1], 'r--', label='Log2-Norm. Roads')
# ax.plot(x, lin_norm_bd[:,1], 'g-', label='Lin.Norm. Buildings')
# ax.plot(x, log2_norm_bd[:,1], 'g--', label='Log2-Norm. Buildings')
legend = ax.legend(loc='upper left', shadow=False)
plt.title('Linear and Log$_2$ normalization for tweet counts')
plt.xlabel('Inversed rank')
plt.ylabel('Normalized tweet count')
plt.show()

# ---- Write results to a csv -----
#sorting the lists on ids
lin_norm_twt = np.array(sorted(lin_norm_twt, key=lambda l:l[0],reverse=False))
log2_norm_twt = np.array(sorted(log2_norm_twt, key=lambda l:l[0],reverse=False))
lin_norm_rd = np.array(sorted(lin_norm_rd, key=lambda l:l[0],reverse=False))
log2_norm_rd = np.array(sorted(log2_norm_rd, key=lambda l:l[0],reverse=False))
lin_norm_bd = np.array(sorted(lin_norm_bd, key=lambda l:l[0],reverse=False))
log2_norm_bd = np.array(sorted(log2_norm_bd, key=lambda l:l[0],reverse=False))

root_dir = '' #folder to write outfile to
outfile = '' #name of output file
with open(root_dir+outfile+'.csv', 'w', newline='') as file:
    csvwriter = csv.writer(file, delimiter=',')
    csvwriter.writerow(['id', 'lin_twt', 'log2_twt', 'lin_rd', 'log2_rd', 'lin_bd', 'log2_bd'])
    for i, id in enumerate(ids):
        csvwriter.writerow([id, lin_norm_twt[i,1], log2_norm_twt[i,1], lin_norm_rd[i,1], log2_norm_rd[i,1], lin_norm_bd[i,1], log2_norm_bd[i,1]])
print('=> File written.')


