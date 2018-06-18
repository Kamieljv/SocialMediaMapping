"""
Modified on Mon 18 Jun 2018
@author: Kamieljv (GitHub)
regression_road.py:
    regression analysis of data on a spatial grid
    fits a line through the data
    makes estimate based on fit
    write results to a csv
"""

from scipy import optimize as opt
import csv
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.nan)

#Reading the data file
twt_dens = np.array([])
bd_cnt = np.array([])
rd_len = np.array([])
sat_binary = np.array([])
ids = np.array([])
folder = '' #data folder
filename = '' #data file name
with open(folder+filename+'.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        if line[0]=='id':
            print(line)
        else: #read the right columns to extract the data
            twt_dens = np.append(twt_dens, [float(line[19])])
            bd_cnt = np.append(bd_cnt, [int(line[8])])
            rd_len = np.append(rd_len, [float(line[6])])
            sat_binary = np.append(sat_binary, [int(line[9])])
            ids = np.append(ids, [int(line[0])])

#reading local Spearman Rank Correlation (SRC) data
corr = np.array([])
p_val = np.array([])
SRC_folder = '' #folder with SRC data file
SRC_filename = '' #name of file with SRC data
with open(SRC_folder+SRC_filename+'.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        if line[0]=='id':
            print(line)
        else:
            corr = np.append(corr, [float(line[1])])
            p_val = np.append(p_val, [float(line[2])])
print('=> Loaded the data.')

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=False)))

def f(x, a, b):
    return a*x**(1/3) + b

def sampler(cent, dim, width): #dimensions 3, 5, 7 or 9 possible
    if not dim in [3, 5, 7, 9]:
        raise ValueError('Please give a dim value in [3, 5, 7, 9].')
    ed = (dim-1)/2 #define horizontal and vertical distance to edge (from center)
    iter_i = np.linspace(-ed, ed, dim) #define iterator from edge to edge
    indices = np.array([])
    for j in iter_i:
        for i in iter_i:
            index = cent + i + j*width
            indices = np.append(indices, [index])
    return indices

def fit_and_predict(pairs_or, plot):
    pairs = np.append(pairs_or, [[0, 0, 0]], axis=0) #add a zero point
    sigma = np.ones(len(pairs))
    sigma[-1] = 0.000001 # make sure the fit goes through the zero point by making the sigma value (change factor) small.
    popt, pcov = opt.curve_fit(f, pairs[:,2], pairs[:,1], sigma=sigma)
    a, b = popt
    mx = max(pairs_or[:,2])
    x = np.linspace(0,mx,100)
    if plot:
        plt.plot(x, f(x, a, b))
        plt.scatter(pairs_or[:,2], pairs_or[:,1], c='r', marker='.')
        plt.show()

    model_pred = f(twt_dens, a, b)
    return model_pred, x, a, b

#converting deg to km
rd_len = rd_len*111.325
twt_dens = twt_dens/7.706

#creating paired list
spear = np.array([[id, c, p] for id, c, p in zip(ids, corr, p_val)])
pairs = np.array([[id, rd, twt] for id, rd, twt in zip(ids, rd_len, twt_dens)])
pairs_nozero = np.array([[id, rd, twt] for id, rd, twt in zip(ids, rd_len, twt_dens) if twt > 0.001])

ids_cent_m = np.array([pair[0] for pair, sp in zip(pairs, spear) if (not sp[1] in [-5, -4, -3, -2] and sp[1]>=.4)])
ids_spear_m = np.ndarray.flatten(np.array([sampler(id, 9, 341) for id in ids_cent_m]))
ids_spear_m = sort_and_deduplicate(ids_spear_m)
pairs_spear_m = np.array([pair for pair in pairs if pair[0] in ids_spear_m])

ids_cent_h = np.array([pair[0] for pair, sp in zip(pairs, spear) if (not sp[1] in [-5, -4, -3, -2] and sp[1]>=.6)])
ids_spear_h = np.ndarray.flatten(np.array([sampler(id, 9, 341) for id in ids_cent_h]))
ids_spear_h = sort_and_deduplicate(ids_spear_h)
pairs_spear_h = np.array([pair for pair in pairs if pair[0] in ids_spear_h])
print('=> Processed the data.')

pred_raw, x, a, b = fit_and_predict(pairs, False)
pred_nozero, x0, a0, b0 = fit_and_predict(pairs_nozero, False)
pred_spear_m, x1, a1, b1 = fit_and_predict(pairs_spear_m, False)
pred_spear_h, x2, a2, b2 = fit_and_predict(pairs_spear_h, False)

#plot the fits
fig, ax = plt.subplots()
ax.plot(x, f(x, a, b), 'b-', label='Raw fit')
ax.plot(x0, f(x0, a0, b0), 'r-', label='Tweet dens. < 0.001')
ax.plot(x1, f(x1, a1, b1), 'g-', label='Only >moderate Spearman')
ax.plot(x2, f(x2, a2, b2), 'c-', label='Only >high Spearman')
ax.scatter(pairs[:,2], pairs[:,1], c='gray', marker='.', label='All cell data')
legend = ax.legend(loc='lower right', shadow=False)
plt.xlabel('Tweet density ($twt/km^2$)')
plt.ylabel('Road Length ($km$)')
plt.title('Different fits for Road Length vs. Tweet density')
plt.show()


#write results to a csv
root_dir = '' #folder to write file into
outfile = '' #name of output file
with open(root_dir+outfile+'.csv', 'w', newline='') as file:
    csvwriter = csv.writer(file, delimiter=',')
    csvwriter.writerow(['id','pred_raw', 'pred_nozero', 'pred_spear_m', 'pred_spear_h', 'diff_raw', 'diff_nonzero', 'diff_spear_m', 'diff_spear_h'])
    for i, id in enumerate(ids):
        csvwriter.writerow([id, round(pred_raw[i],4), round(pred_nozero[i],4), round(pred_spear_m[i],4), round(pred_spear_h[i],4),
                            round(pred_raw[i]-rd_len[i],4), round(pred_nozero[i]-rd_len[i],4), round(pred_spear_m[i]-rd_len[i],4), round(pred_spear_h[i]-rd_len[i],4)])
print('=> File written.')
