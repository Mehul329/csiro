#this porgram assumes that the path of the input filter bank is in the format 
#/scratch2/aga017/utmost_data/tape_no/obs_no/FB/beam_no/filterbank.fil

#%% importing modules

import numpy as np
from sigpyproc.readers import FilReader as F
import argparse
from numba import jit

#%% Input

a = argparse.ArgumentParser()
a.add_argument('-f', type = str, help = 'Give the full location of the filename in .fil format', default = '/u/aga017/Desktop/2018-03-01-14:17:51/BEAM_063/2018-03-01-14:17:51.fil')
a.add_argument('-t_x', type = int, help = 'Give the value for scrunching', default = 20)
a.add_argument('-k', type = int, nargs = 3, help = 'Bins list: Start, Factor, End', default = [1,1.25,800])
a.add_argument('-dm', type = int, nargs = 3, help = 'DM list: Start, End, Steps', default = [1,90,2])
a.add_argument('-fl_j', '--flattening_jump', type=int, help="Jump size to use when flattening the time series (def = 100", default=100)
a.add_argument("-t", '--threshold', type=float, help='S/N threshold for selecting candidates (def = 8)', default=8)

args = a.parse_args()
filename = args.f #takes the filename

k_start, k_factor, k_end = args.k
k_n = int(np.ceil((np.log(k_end/k_start)/np.log(k_factor))+1))
k_end = k_start*k_factor**(k_n-1)
kernel_lst = np.geomspace(k_start, k_end, k_n).astype(int) 
kernel_lst = np.unique(kernel_lst) #take the list of bin sizes

dm_start, dm_end, dm_space = args.dm
dm = np.linspace(dm_start, dm_end, int(1+(dm_end-dm_start)/dm_space)).astype(int) #take the list of possible dm's

t_x = args.t_x

threshold = args.threshold

jump = args.flattening_jump

#%% Functions are defined in this block

#this function finds the average of the time series based on the average width provided to it
#if anything is left at the end, it just ignores it
def t_scrunch(data, t_x):
    n_chans = data.header.nchans     
    nsamps = data.header.nsamples
    rem = nsamps % t_x
    if rem != 0:
        nsamps = nsamps - rem
    data = data.read_block(0, nsamps)
    nsamps = int(nsamps/t_x)
    data = data.reshape([nsamps*n_chans,t_x])
    data = np.average(data,axis = 1)
    data = data.reshape(n_chans,nsamps)
    return data, nsamps, n_chans

#this function flattens the curve. Because each channel has quadratic nature, and when
#summed up, the quadratic nature amplifies, so this will help faltten it
def flatten(time_series, interval):
    xx = np.arange(len(time_series))
    model = np.poly1d(np.polyfit(xx[::interval], time_series[::interval], 2 ))
    y = model[2] * xx**2 + model[1] * xx + model[0]
    return time_series - y

#this function helps in choosing the best average width if the time and dm is same for
#a candidate
@jit(nopython=True)
def box_remover(array):
    final_cands = np.zeros_like(array)
    times = np.unique(array[:,0])
    count = 0
    for time_ in times:
        array_2 = array[array[:,0] == time_]
        final_cand = array_2[array_2[:,-1] == np.max(array_2[:,-1])]
        final_cands[count] = final_cand
        count += 1
    return final_cands[:count]


#this function is the main function which finds the potential candidates in the filer
#bank and stores the sample number, its dispersion meaure in terms of change in sample,
#its average width, its Signal to Noise Ratio and 
def find_cands(filterbank, t_x, threshold, dm, kernel_lst):
    data = F(filename) #reads the data from filter bank
    data, nsamps, n_chans= t_scrunch(data, t_x) #averages the data by t_x because no need of full data
    max_f = data.header.fch1 #maximum observing frequency
    min_f = max_f + data.header.foff * (n_chans-1) #minimum observing frequency
    possible_freq = np.linspace(max_f, min_f, n_chans) #different frequency channels

    #the function is in the format frequency = a/(sample_number - b)^2
    possible_b = ((min_f/max_f)**2)*dm/(1-(min_f/max_f)**2) #possible b's
    possible_a = max_f*((possible_b)**0.5) #possible a's

    SNRs = []
    Bins = []
    Times = []
    DMs = []
    
    #creating an empty array of the size that the dispersed data set will be because
    #row stacking is not efficient
    new_data = np.empty([n_chans,nsamps]) 
    
    #checking mutiple dispersion measures now
    for i in range(len(possible_a)):
        #print("DM is : ", dm[i])
        new_data[0] = data[0]
        for j in range(1, n_chans):
            freq = possible_freq[j]
            new_start = int((possible_a[i]/(freq))**2 - possible_b[i])
            new_data[j] = np.roll(data[j], -new_start) #rolling or dispersing the channel
            
            #this will be used for zapping the channels
            #if (840 <= freq <= 844.5) or (835.5 <= freq <= 840) or (830 <= freq <= 835) or 
            #(825.25 <= freq <= 829.75):
            if (840 <= freq <= 844.5): 
                new_data[j] = np.zeros_like(new_data[j])

        #following calculates the sum of each column
        sum_ = np.average(new_data, axis = 0)

        #uses the flattening function to flatten the sum
        flattened_sum = flatten(sum_, jump)
        
        #calcultes the rms of sum
        rms = flattened_sum.std()
        
        SNRs_temp = []
        Bins_temp = []
        Times_temp = []
        DMs_temp = []
        
        for kernel in kernel_lst:
            #print("Kernel is: ", kernel)
            
            #finds the moving average of the the sum and removes the extra cands
            mvaverage_arr = np.convolve(flattened_sum, np.ones(kernel), mode='valid') 
            #divides it by rms and sqrt(kernel) to show the highest SNR as highest and to correc the data
            mvaverage_arr /= (rms * np.sqrt(kernel))
            #stores the data of the peaks greater than threhold
            peak_locs = mvaverage_arr > threshold
            
            snrs = mvaverage_arr[peak_locs]
            times = np.arange(len(mvaverage_arr))[peak_locs] * t_x
            bins = kernel * t_x * np.ones_like(snrs)
            dms = [dm[i] * t_x] * len(bins)

            SNRs_temp.extend(list(snrs))
            Bins_temp.extend(list(bins))
            Times_temp.extend(list(times))
            DMs_temp.extend(list(dms))
            
        cands = np.column_stack([Times_temp, Bins_temp, DMs_temp, SNRs_temp])
        
        #removes the extra candnidates which doesnt have good average widhts give 
        #high SNR
        cands = box_remover(cands)
        Times.extend(list(cands[:,0]))
        Bins.extend(list(cands[:,1]))
        DMs.extend(list(cands[:,2]))
        SNRs.extend(list(cands[:,3]))
        
    
    final_cands = np.column_stack([Times, Bins, DMs, SNRs])
    titles = np.array(['Times', 'Bins', 'DMs', 'SNRs'])
    final_cands = np.row_stack([titles, final_cands]).astype(str)
    return final_cands

#%% File name is being created

outdir = "/scratch2/aga017/output/"
infile = filename.split('/')[-5:]
outname = outdir+infile[0]+'_'+infile[1]+'_'+infile[3]+'.txt'
sentence = f"#The data is being sruched by a factor of {t_x}. DM search is linear from {dm_start} to {dm_end} with a spacing of {dm_space}. Boxcarring is geometric from {k_start} to {int(k_end)} with a factor of {k_factor}. The threshold is {threshold} and the curve of best fit is being derived by jumping to every {args.flattening_jump} point in the scrunched data"

#%% Defined function is being called and written on a text file and stored in the directory above

with open(outname, "w") as file:
    file.write(sentence + "\n")
    np.savetxt(file, find_cands(filename, t_x, threshold, dm, kernel_lst), fmt = '%s')
