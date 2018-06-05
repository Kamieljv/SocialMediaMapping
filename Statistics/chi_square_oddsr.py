from scipy import stats as scst
import csv
import numpy as np
import matplotlib.pyplot as plt

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
    return oddsr

#SAT CLASS VS OSM FEATURE
print('SAT CLASS VS OSM FEATURE:')
chi2_sat_osm, p_sat_osm = chi2(sat_binary, osm_binary)
oddsr_sat_osm = oddsratio(sat_binary, osm_binary)

#SAT CLASS VS TWEET
print('SAT CLASS VS TWEET:')
chi2_sat_twt, p_sat_twt = chi2(sat_binary, twt_binary)
oddsr_sat_twt = oddsratio(sat_binary, twt_binary)

#TWEET VS OSM FEATURE
print('TWEET VS OSM FEATURE:')
chi2_twt_osm, p_twt_osm = chi2(twt_binary, osm_binary)
oddsr_twt_osm = oddsratio(twt_binary, osm_binary)