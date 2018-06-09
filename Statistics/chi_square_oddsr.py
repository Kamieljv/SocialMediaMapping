"""
Modified on Tue 8 Jun 2018
@author: Kamieljv (GitHub)
chi_square_oddsr.py:
    compute the chi-square values and odds ratio of a set of values on a spatial grid.
"""

from scipy import stats as scst
import csv
import numpy as np
import matplotlib.pyplot as plt
import math

#Reading the data file
twt_cnt = np.array([])
bd_cnt = np.array([])
rd_len = np.array([])
sat_binary = np.array([])
root_dir = '' #directory of data file
filename = ''
with open(root_dir+filename+'.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        if line[0]=='id':
            print(line)
        else:
            twt_cnt = np.append(twt_cnt, [int(line[6])]) #load tweet counts
            bd_cnt = np.append(bd_cnt, [int(line[11])]) #load building counts
            rd_len = np.append(rd_len, [float(line[8])]) #load road lengths
            sat_binary = np.append(sat_binary, [int(line[13])]) #load binary satellite classification
print('=> Loaded the data.')

len = len(twt_cnt)
twt_binary = [1 if cnt!=0 else 0 for cnt in twt_cnt] #create binary list of tweets (contains tweet = 1)
bd_binary = [1 if cnt!=0 else 0 for cnt in bd_cnt] #create binary list of buildings (contains building = 1)
rd_binary = [1 if len!=0 else 0 for len in rd_len] #create binary list of roads (contains road = 1)
osm_binary = [1 if (bd_cnt[i]!=0 or rd_len[i]!=0) else 0 for i,item in enumerate(bd_cnt)] #create binary list of OSM (contains feature (road/building) = 1)

def contingency(binary1, binary2):
    #Function that creates a contingency table (actually the values a, b, c, d)
    #Table:
    #  a  |  b
    #  -------
    #  c  |  d
    #   binary1: variable on rows
    #   binary2: variable on cols

    a = np.count_nonzero([1 if (binary1[i]==0 and binary2[i]==0) else 0 for i in range(len)])
    b = np.count_nonzero([1 if (binary1[i]==0 and binary2[i]==1) else 0 for i in range(len)])
    c = np.count_nonzero([1 if (binary1[i]==1 and binary2[i]==0) else 0 for i in range(len)])
    d = np.count_nonzero([1 if (binary1[i]==1 and binary2[i]==1) else 0 for i in range(len)])

    return a, b, c, d

def chi2(binary1, binary2):
    #Function that computes chi2 based on the contingency table
    #   binary1: variable on rows
    #   binary2: variable on cols

    a, b, c, d = contingency(binary1, binary2)
    cont = np.array([[a, b],
                    [c, d]])
    print(cont)
    chi2 = scst.chi2_contingency(cont)
    print('chi2: '+str(round(chi2[0], 2))+'\n'+'p-value:   ' +str(chi2[1])+'\n')
    return chi2[0], chi2[1] #chi2 value and p-value, respectively

def oddsratio(binary1, binary2):
    #Function that computes the odds ratio based on the contingency table
    #   binary1: variable on rows
    #   binary2: variable on cols

    a, b, c, d = contingency(binary1, binary2)
    cont = np.array([[a, b],
                      [c, d]])
    print(cont)
    oddsr = (a/b)/(c/d)
    print('oddsr: '+str(round(oddsr, 2))+'\n')

    conf_l = round(math.exp(math.log(oddsr) - 1.96*math.sqrt(1/a+1/b+1/c+1/d)),1)
    conf_u = round(math.exp(math.log(oddsr) + 1.96*math.sqrt(1/a+1/b+1/c+1/d)),1)

    conf95 = [conf_l, conf_u]
    print('95% Confidence Interval: ',conf95)

    return oddsr, conf95

print('---------------------------------\n',
      'SAT CLASS VS ROADS:')
chi2_sat_rd, p_sat_rd = chi2(sat_binary, rd_binary)
oddsr_sat_rd = oddsratio(sat_binary, rd_binary)

print('---------------------------------\n',
      'SAT CLASS VS BUILDINGS:')
chi2_sat_bd, p_sat_bd = chi2(sat_binary, bd_binary)
oddsr_sat_bd = oddsratio(sat_binary, bd_binary)

print('---------------------------------\n',
      'SAT CLASS VS TWEET:')
chi2_sat_twt, p_sat_twt = chi2(sat_binary, twt_binary)
oddsr_sat_twt = oddsratio(sat_binary, twt_binary)

print('---------------------------------\n',
      'TWEET VS ROADS:')
chi2_twt_rd, p_twt_rd = chi2(twt_binary, rd_binary)
oddsr_twt_rd = oddsratio(twt_binary, rd_binary)

print('---------------------------------\n',
      'TWEET VS BUILDINGS:')
chi2_twt_bd, p_twt_bd = chi2(twt_binary, bd_binary)
oddsr_twt_bd = oddsratio(twt_binary, bd_binary)

print('---------------------------------\n',
      'ROADS VS BUILDINGS:')
chi2_rd_bd, p_rd_bd = chi2(rd_binary, bd_binary)
oddsr_rd_bd = oddsratio(rd_binary, bd_binary)