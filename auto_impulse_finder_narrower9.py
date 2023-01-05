import numpy as np
from sigpyproc.readers import FilReader as F

#%% Input
filename = '2018-07-02-03:55:09' #takes the filename
kernel_lst = np.linspace(4,16,16-4+1).astype(int) #take the list of bin sizes
dm = np.linspace(110,120,120-110+1).astype(int) #take the list of possible dm's

#%%
data = F(filename+'.fil')
nsamps = data.header.nsamples
data = data.read_block(0, nsamps)


n_chans = data.header.nchans
max_f = data.header.fch1
min_f = max_f + data.header.foff * n_chans
possible_freq = np.linspace(max_f, min_f, n_chans) #different frequency channels


possible_b = ((min_f/max_f)**2)*dm/(1-(min_f/max_f)**2) #possible b's
possible_a = max_f*((possible_b)**0.5) #possible a's


#all the channels of the data has been flattened
time_x = np.linspace(0,nsamps-1, nsamps)

for k in range(len(data)):
    model = np.poly1d(np.polyfit(time_x, data[k], 2))
    c_ = model[0]
    b_ = model[1]
    a_ = model[2]
    y = a_*time_x**2 + b_*time_x + c_
    data[k] = data[k] - y

cands = np.array(['Initial Time', 'S/R', 'Bins', 'DM'])

for i in range(len(possible_a)):
    print(dm[i])
    new_data = np.empty([n_chans,nsamps]) 
    new_data[0] = data[0]
    spectral_std = []
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

    threshold = 8
    
    for kernel in kernel_lst:
        print(kernel)
        mvaverage = []
        
        for l in range(len(sum_)-(kernel-1)):
            mvaverage.append(np.average(sum_[l:l+kernel]))
        
        mvaverage_arr = np.array(mvaverage)
        mvaverage_arr /= np.std(mvaverage_arr)
        in_time = np.transpose(np.where(mvaverage_arr > threshold)) 
        snr = np.reshape(mvaverage_arr[mvaverage_arr > threshold], np.shape(in_time))
        bins = kernel * np.ones_like(snr)
        dm_ = dm[i] * np.ones_like(snr)
        stack = np.column_stack((in_time, snr, bins, dm_))
        cands = np.row_stack((cands, stack))

#%%
cands = cands[1:,:].astype(float)
cands = cands[cands[:,0].argsort()] #sorting it with respect to in_time
in_time = list(cands[:,0])
SNR = list(cands[:,1]) 
bins = list(cands[:,2]) 
DM = list(cands[:,3])

#%%
#this function will group the neighbouring points (used on first_seen_time)
def groupBlocks(samp_list, bin_list):
    res = [[0]]
  
    for i in range(1, len(samp_list)):
        if samp_list[i] in range(int(samp_list[i-1]),int(samp_list[i-1]+bin_list[i-1])):
            res[-1].append(i)
        else:
            res.append([i])
    return res

a = groupBlocks(in_time, bins) 

#this loop will extract the point that has the maximum S/R among the neighbouring points
for i in range(len(a)):
    if len(a[i]) == 1:
        a[i] = a[i][0]
    else:
        max_value = 0
        max_ind = 0
        for j in range(len(a[i])):
            if SNR[a[i][j]] > max_value:
                max_value = SNR[a[i][j]]
                max_ind = j
        a[i] = a[i][max_ind]

cands = cands[a]
cands = cands[cands[:,3].argsort()] #sorting it with respect to DMs
in_time = list(cands[:,0])
SNR = list(cands[:,1]) 
bins = list(cands[:,2]) 
DM = list(cands[:,3])

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

