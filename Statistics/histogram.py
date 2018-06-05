import csv
import numpy as np
import matplotlib.pyplot as plt

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
print('=> Loaded the data.')

# ---- Plot building histogram -----
max_twt = twt_cnt.max()
nrbins_twt = int(max_twt+1) #define number of bins
hist = np.histogram(twt_cnt, bins=nrbins_twt)
freq_twt = hist[0]
bins_twt = hist[1]
end_twt = 1000 #maximum number of tweets per cell (higher will not be plotted)

x = np.linspace(0,end_twt-1,end_twt) #create x-axis
y = freq_twt[:end_twt]
plt.bar(x,y,log=1)
plt.title("Number of Tweets")
plt.xlabel('number of tweets')
plt.ylabel('frequency')
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
plt.bar(x,y,log=1)
plt.title("Number of Buildings")
plt.xlabel('number of buildings')
plt.ylabel('frequency')
plt.show()