
import numpy as np
import matplotlib.pyplot as plt
from sigpyproc.readers import FilReader as F
import pathlib
import argparse

#%% Input
#a = argparse.ArgumentParser()
#a.add_argument('-f', type = str, help = 'Type the filename', default = '/u/aga017/Desktop/SM0005L6_2018-02-23-17:56:51_BEAM_004.txt')
#args = a.parse_args()
#filename = args.f

#%%
#candidates = np.loadtxt(filename+'.txt',dtype=str)
candidates = np.loadtxt('/u/aga017/Desktop/SM0005L6_2018-02-23-17:56:51_BEAM_004.txt')
candidates = candidates[1:]

def plotter(matrix, dm, imp_start, bins, area):
  
    matrix = F(matrix)
    nsamps = matrix.header.nsamples
    n_chans = matrix.header.nchans
    max_f = matrix.header.fch1
    min_f = max_f + matrix.header.foff * n_chans
    
    matrix = matrix.read_block(0, nsamps)
    
    area = area + (bins - (area % bins)) 
    
    b = ((min_f/max_f)**2)*dm/(1-(min_f/max_f)**2)
    a = max_f*((b)**0.5)
    freq = np.linspace(max_f, min_f, n_chans)
    
    out = np.empty([n_chans, int((2 * area + bins)/bins)])
    for j in range(n_chans):
        imp = int((a/(freq[j]))**2 - b) + imp_start
        
        area_start = imp - area
        start_range = matrix[j][np.linspace(area_start, imp + bins - 1, imp + bins - area_start).astype(int)]
       
        
        area_end = imp + bins + area
        end_range = matrix[j][(np.linspace(imp + bins, area_end - 1, area_end - (imp + bins)) % nsamps).astype(int)]

       
        channel = np.concatenate((start_range, end_range))
        channel = np.reshape(channel, [int(len(channel)/bins), bins])
        new_channel = np.average(channel, axis = 1)
        out[j] = new_channel
    
    sum_ = np.sum(out, axis = 0)
        
    return out, sum_

#new_dir = pathlib.Path('/u/aga017/Desktop/', filename) #disable this on your machine or change accordingly
#new_dir.mkdir(parents=True, exist_ok=True) #disable this on your machine or change accordingly
for i in range(1, len(candidates)):
    dm = int(float(candidates[i,2]))
    imp_start = int(float(candidates[i,0]))
    SNR = round(float(candidates[i,3]),2)
    bins = int(float(candidates[i,1]))
    out, sum_ = plotter('/u/aga017/Desktop/2018-02-23-17:56:51.fil', dm, imp_start, bins, 500)
    temp = np.where(sum_ > (7*np.std(sum_) + np.mean(sum_)))
    #check = len(temp[0]) #enable this if you want to look at sharp spikes only
    check = 1
    if check == 1:
        fig = plt.figure()
        ax0 = plt.subplot2grid(shape = (3, 1), loc = (0, 0), rowspan = 2, colspan = 1, fig = fig)
        ax0.set_title(f"DM = {dm}, First seen = {imp_start}, bins = {bins}, S/R = {SNR}")
        ax1 = plt.subplot2grid(shape = (3, 1), loc = (2, 0), rowspan = 1, colspan = 1, fig = fig, sharex = ax0)
        plt.subplots_adjust(hspace = 0)
        ax0.imshow(out, aspect = 'auto', interpolation = 'None')
        ax0.axes.get_xaxis().set_visible(False)
        ax1.plot(sum_, 'r-')
        plt.show()
        #fig.savefig(new_dir / str(i), format = 'png', dpi = 300) #disable this on your machine or change accordingly
        plt.show()
    
            
