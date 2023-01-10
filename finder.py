import numpy as np
from sigpyproc.readers import FilReader as F
import argparse
#import matplotlib.pyplot as plt


#%% Input
a = argparse.ArgumentParser()
a.add_argument('-f', type = str, help = 'Type the filename', default = '2018-06-27-04_14_17.fil')
a.add_argument('-k', type = int, nargs = 3, help = 'Bins list: Start, End, Steps', default = [1,10,1])
a.add_argument('-dm', type = int, nargs = 3, help = 'DM list: Start, End, Steps', default = [10,100,10])
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


SNRs = []
Bins = []
DMs = []
Times = []

new_data = np.empty([n_chans,nsamps])
threshold = args.threshold
    
for i in range(len(possible_a)):
    #print("DM is : ", dm[i])
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
        #print("Kernel is: ", kernel)

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
        
cands = np.column_stack([Times, Bins, DMs, SNRs])
titles = np.array(['Times', 'Bins', 'DMs', 'SNRs'])
cands = np.row_stack([titles, cands]).astype(str)

np.savetxt(filename[:-3]+'txt', cands, fmt='%s')
