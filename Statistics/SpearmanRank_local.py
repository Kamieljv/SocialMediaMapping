"""
Modified on Tue 5 Jun 2018
@author: Kamieljv (GitHub)
SpearmanRank_local.py:
    compute the Spearman Rank Correlation of local samples on a grid
    write results to a csv file
"""

from scipy import stats as scst
import csv
import numpy as np
import math
import statistics
np.set_printoptions(threshold=np.nan)

#----------Reading the data file----------------
ids = np.array([])
twt_cnt = np.array([])
bd_cnt = np.array([])
rd_len = np.array([])
root_dir = '' #directory of data file
filename = ''
with open(root_dir+filename+'.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        if line[0]=='id': #skipping the header file
            print(line)
        else:
            #loading the data per cell. Note: line indexes depend on data file.
            ids = np.append(ids, [int(line[0])]) #load cell ids
            twt_cnt = np.append(twt_cnt, [int(line[6])]) #load tweet counts
            bd_cnt = np.append(bd_cnt, [int(line[11])]) #load building counts
            rd_len = np.append(rd_len, [float(line[8])]) #load road lengths

#--------Storing the data--------------------
data = dict() #store data in dict, with ids as keys
for i, id in enumerate(ids):
    data[id] = [twt_cnt[i], bd_cnt[i], rd_len[i]]
print('=> Loaded and stored the data.')

def sampler(cent, dim, width):
    #Function to get indices of a square of cells with dimension dim
    #   cent: center cell of the square sample
    #   dim: dimension of the square sample
    #   width: width of the full square grid (i.e. added index value when moving DOWN one cell)

    if not dim in [3, 5, 7, 9]: #dimensions 3, 5, 7 or 9 possible
        raise ValueError('Please give a dim value in [3, 5, 7, 9].')
    ed = (dim-1)/2 #define horizontal and vertical distance to edge (from center)
    iter_i = np.linspace(-ed, ed, dim) #define iterator from edge to edge
    indices = np.array([])
    for j in iter_i:
        for i in iter_i:
            index = cent + i + j*width
            indices = np.append(indices, [index])
    return indices

def check(sample, ids, cent, thresh=.8):
    #Function to check whether enough of the cell indices in the sample are actually on the grid
    #Returns those indices that actually exist on the grid (the array called 'inside').
    #   sample: the array of sample indices
    #   ids: the array of all grid cell ids
    #   thresh: the threshold value for a pass: default=.8

    inside = [s for s in sample if s in ids]
    n = len(sample)
    cnt = len(inside)
    if cnt/n >= thresh:
        return True, inside
    else:
        return False, inside

def SpearmanRank(sample, type):
    #Function to calculate the Spearman Rank Correlation for a single sample.
    #   sample: list of indices that form the (square) sample. All indices must exist on the actual grid
    #   type: data that tweets are correlated with (either 'rd' or 'bd' for roads and buildings respectively)

    twt_cnt_lst = []
    bd_cnt_lst = []
    rd_len_lst = []
    for s in sample: #listing the cell properties based on their index
        twt_cnt_lst.append(data[s][0])
        bd_cnt_lst.append(data[s][1])
        rd_len_lst.append(data[s][2])
    if type == 'bd': #tweets vs buildings
        return scst.spearmanr(bd_cnt_lst,twt_cnt_lst)
    elif type == 'rd': #tweets vs roads
        return scst.spearmanr(rd_len_lst,twt_cnt_lst)
    else:
        raise ValueError('Please provide valid data type.')


#Looping over dims, types and center cells
dims = [3, 5, 7, 9] #nr of cells along one dimension of the sample area (options: 3, 5, 7, 9)
width = 341 #CHANGE THIS TO YOUR CASE: width of the (rectangular!) grid
types = ['rd','bd']

for dim in dims:
    for typ in types:
        print('=> Starting calculations. Dimensions: {}, Width: {}, Type: {}, Nr.Cells: {}'.format(dim, width, typ, len(ids)))
        corr = []
        for i,cent in enumerate(ids):
            if i%500 ==0:
                print('Progress: {}%'.format(round(i/15101*100,1)))
            sample = sampler(cent, dim, width) #get a square sample of 'dim'x'dim'
            thresh_check, filtered_sample = check(sample, ids, cent) #filter out cells that are not on the actual grid and
                                                                   #check if the percentage of cells on the grid exceeds the the threshold (default = .80)
            if thresh_check:
                loc_corr, p = SpearmanRank(filtered_sample, typ)
                corr.append([loc_corr, p])
            else:
                corr.append([-3, -3]) #Add data label for cells that don't reach the existance threshold

        corr = [[c,p] if not math.isnan(c) else [-2,-2] for c,p in corr] #Add data label for cells that return an infinite correlation (not computable)
        corr_filtered = [[c,p] for c,p in corr if not c in [-3, -2]] #Filter out cells with data labels for statistics computation
        corr_filtered_no_p = [c for c,p in corr_filtered]
        p_val = [p for c,p in corr_filtered]

        print('Cells: ',len(ids))
        print('Cells after filter: ', len(corr_filtered_no_p), len(corr_filtered))

        av = sum(corr_filtered_no_p) / float(len(corr_filtered_no_p))
        print('Average correlation: ', av)

        stdv = statistics.stdev(corr_filtered_no_p)
        print('St.Dev correlation: ', stdv)

        bins = [-1, -.8, -.6, -.4, -.2, 0, .2, .4, .6, .8, 1] #classes: very weak, weak, moderate, strong, very strong (both pos. and neg.)
        hist, _ = np.histogram(corr_filtered_no_p, bins=bins)
        print('Distribution of classes', hist)

        av_p_val = sum(p_val) / float(len(p_val))
        print('Average p:', av_p_val)

        cnt_sig = sum(1 if p<=0.05 else 0 for p in p_val)
        print('Number of significant cells: ', cnt_sig)

        output = [[i,c,p] if p<=0.05 else [i,-4, -4] if (p>0.05 and p<=0.1) else [i,-5,-5] for (c,p),i in zip(corr, ids)]
        # Add data labels that tell whether the Spearman Rank is lightly insignificant or insignificant

        outfile = 'SpearmanRank_{}_dim{}'.format(typ, dim) #name of output file
        with open(outfile+'.csv', 'w', newline='') as file:
            csvwriter = csv.writer(file, delimiter=',')
            csvwriter.writerow(['id','c','p'])
            for line in output:
                csvwriter.writerow(line)

#Data labels:
        # -5 for insignificant (.10<p<=1.0)
        # -4 for lightly insignificant (0.05<p<=0.10)
        # -3 for edge,
        # -2 for nan,