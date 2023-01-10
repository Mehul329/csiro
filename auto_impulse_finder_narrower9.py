import numpy as np
from sigpyproc.readers import FilReader as F
import argparse
import matplotlib.pyplot as plt
from sklearn import cluster

#%% Input
a = argparse.ArgumentParser()
a.add_argument('-f', type = str, help = 'Type the filename', default = '2018-06-27-04:14:17.fil')
a.add_argument('-k', type = int, nargs = 3, help = 'Bins list: Start, End, Steps', default = [1,10,1])
a.add_argument('-dm', type = int, nargs = 3, help = 'DM list: Start, End, Steps', default = [40,50,1])
a.add_argument('-fl_j', '--flattening_jump', type=int, help="Jump size to use when flattening the time series (def = 100", default=100)
a.add_argument("-t", '--threshold', type=float, help='S/N threshold for selecting candidates (def = 8)', default=8)

args = a.parse_args()
filename = args.f #takes the filename
k_start, k_end, k_space = args.k
dm_start, dm_end, dm_space = args.dm
kernel_lst = np.linspace(k_start, k_end, int(1+(k_end-k_start)/k_space)).astype(int) #take the list of bin sizes
dm = np.linspace(dm_start, dm_end, int(1+(dm_end-dm_start)/dm_space)).astype(int) #take the list of possible dm's

#%%
data = F(filename)
nsamps = data.header.nsamples
data = data.read_block(0, nsamps)


n_chans = data.header.nchans
max_f = data.header.fch1
min_f = max_f + data.header.foff * (n_chans-1)
possible_freq = np.linspace(max_f, min_f, n_chans) #different frequency channels


possible_b = ((min_f/max_f)**2)*dm/(1-(min_f/max_f)**2) #possible b's
possible_a = max_f*((possible_b)**0.5) #possible a's


#all the channels of the data has been flattened
time_x = np.linspace(0,nsamps-1, nsamps)

def flatten(time_series, interval):
    xx = np.arange(len(time_series))
    model = np.poly1d(np.polyfit(xx[::interval], time_series[::interval], 2 ))
    y = model[2] * xx**2 + model[1] * xx + model[0]
    return time_series - y


#cands = np.array(['Initial Time', 'S/R', 'Bins', 'DM'])
SNRs = []
Bins = []
DMs = []
Times = []

new_data = np.empty([n_chans,nsamps])
threshold = args.threshold
    
for i in range(len(possible_a)):
    print("DM is : ", dm[i])
    new_data[0] = data[0]
    for j in range(1, n_chans):
        freq = possible_freq[j]
        new_start = int((possible_a[i]/(freq))**2 - possible_b[i])
        new_data[j] = np.roll(data[j], -new_start)
        #if (840 <= freq <= 844.5) or (835.5 <= freq <= 840) or (830 <= freq <= 835) or 
        #(825.25 <= freq <= 829.75): 
        #    new_data[j] = np.zeros_like(new_data[j])
        #new data is  now transformed data based on the curve

    #following calculates the sum of each column
    sum_ = np.average(new_data, axis = 0)

    flattened_sum = flatten(sum_, args.flattening_jump)

    rms = flattened_sum.std()

    for kernel in kernel_lst:
        print("Kernel is: ", kernel)

        mvaverage_arr = np.convolve(flattened_sum, np.ones(kernel), mode='valid')
        mvaverage_arr /= (rms * np.sqrt(kernel))
        #plt.plot(mvaverage_arr)
        #plt.show()
        peak_locs = mvaverage_arr > threshold
        snr = mvaverage_arr[peak_locs]
        
        SNRs.extend(list(snr))
        Bins.extend(list(kernel * np.ones_like(snr)))
        DMs.extend(list(dm[i] * np.ones_like(snr)))
        Times.extend( list(np.arange(len(mvaverage_arr))[peak_locs]))

fig = plt.figure()
ax = plt.axes(projection ='3d')
ax.plot3D(Bins, DMs, Times, '.')
plt.show()

#%%
cls_obj = cluster.AgglomerativeClustering(n_clusters=None, compute_full_tree=True, distance_threshold=10)
clusters = cls_obj.fit(np.column_stack([Times, Bins, DMs])).labels_


#%%
#this function will group the neighbouring points (used on first_seen_time)
'''
def groupBlocks(samp_list, bin_list):
    res = [[0]]
  
    for i in range(1, len(samp_list)):
        if samp_list[i] in range(int(samp_list[i-1]),int(samp_list[i-1]+bin_list[i-1])):
            res[-1].append(i)
        else:
            res.append([i])
    return res

a = groupBlocks(Times, Bins) 

#this loop will extract the point that has the maximum S/R among the neighbouring points
for i in range(len(a)):
    if len(a[i]) == 1:
        a[i] = a[i][0]
    else:
        max_value = 0
        max_ind = 0
        for j in range(len(a[i])):
            if SNRs[a[i][j]] > max_value:
                max_value = SNRs[a[i][j]]
                max_ind = j
        a[i] = a[i][max_ind]

Times = list(np.array(Times)[a])
SNRs = list(np.array(Times)[a])
Bins = list(np.array(Times)[a])
DMs = list(np.array(Times)[a])
cands = cands[a]
cands = cands[cands[:,3].argsort()] #sorting it with respect to DMs
#%%
#this function will group the neighbouring duplicates (used on DMs)
def groupDuplicates(lst):
    res = [[0]]
  
    for i in range(1, len(lst)):
        if lst[i-1] == lst[i]:
            res[-1].append(i)
  
        else:
            res.append([i])
    return res

a = groupDuplicates(DM)

#this loop will sort the in_times in each DMs
for i in range(len(a)):
    if len(a[i]) > 1:
        start = a[i][0]
        end = a[i][-1]
        temp = cands[start:end+1, :]
        temp = temp[temp[:,0].argsort()]
        cands[start:end+1,:] = temp

#%%
name = np.array(['Initial Time', 'S/R', 'Bins', 'DM'])
cands = np.row_stack((name, cands))
np.save(filename, cands)
'''
