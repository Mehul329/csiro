#this porgram assumes that the path of the input filter bank is in the format 


#%% importing modules

import matplotlib.pyplot as plt
from sigpyproc.readers import FilReader as F
import numpy as np
import argparse

#%%defining inputs

a = argparse.ArgumentParser()
a.add_argument('-t', type = str, help = 'Give the tape name')
a.add_argument('-o', type = str, help = 'Give the observation ')

args = a.parse_args()
tape_no = args.t
observation = args.o

#%%defining functions

#this function flattens the curve. Because each channel has quadratic nature, and when
#summed up, the quadratic nature amplifies, so this will help faltten it
def flatten(time_series, interval):
    xx = np.arange(len(time_series))
    model = np.poly1d(np.polyfit(xx[::interval], time_series[::interval], 2 ))
    y = model[2] * xx**2 + model[1] * xx + model[0]
    return time_series - y

#this function will generate the data to plot how the candidate looks
def plotter(matrix, dm, imp_start, bins, blocks):
    #blocks helps us tell how many points do we want on the either side of the
    #candidate when plotting it
    
    matrix = F(matrix)
    nsamps = matrix.header.nsamples
    n_chans = matrix.header.nchans
    max_f = matrix.header.fch1
    min_f = max_f + matrix.header.foff * (n_chans-1)
    
    matrix = matrix.read_block(0, nsamps)

    #the function is in the format frequency = a/(sample_number - b)^2
    b = ((min_f/max_f)**2)*dm/(1-(min_f/max_f)**2) #constant in equation
    a = max_f*((b)**0.5) #constant in equation
    freq = np.linspace(max_f, min_f, n_chans)

    #following is the lenght of each channel and its being determined based
    #on the last channel
    c = nsamps - int((a/(freq[-1]))**2 - b)

    #creating an empty array of the size that the dispersed data set will be because
    #row stacking is not efficient
    final = np.empty([n_chans,c])
    
    #after the for loop finishes the pulse should be lined up
    for j in range(n_chans):

        temp_start = int((a/(freq[j]))**2 - b)
        temp_end = temp_start + c
        
        final[j] = matrix[j][temp_start:temp_end]
        
    #next job is to remove the extra bits from the start and end so that the 
    #channel lenght remains a multiple of bin size
    
    rem_start = imp_start % bins
    start_blocks_av = (imp_start - rem_start)//bins

    if start_blocks_av <= blocks:
        start = rem_start
    else:
        extra_block = start_blocks_av - blocks
        start = rem_start + extra_block * bins

    new_imp_start = imp_start - start
    
    rem_end = (c-(imp_start + bins))%bins
    end_blocks_av = (c-(imp_start + bins))//bins

    if end_blocks_av <= blocks:
        end = rem_end
    else:
        extra_block = end_blocks_av - blocks
        end = (c-(imp_start + bins)) - blocks * bins
        
    if end == 0:    
        final = final[:,start:]
    else:
        final = final[:,start:-end]
        
    #reshaping it to find the average in an efficient way
    final = final.reshape(n_chans, len(final[0])//bins, bins).mean(axis=-1)
    
    sum_ = np.average(final, axis = 0)
    sum_ = flatten(sum_, 5)
    
    #this is converting the dm to parsec/cm^3
    dm = ((dm * ((2**16)/100000000))*1000)/(4.15*((min_f/1000)**(-2) - (max_f/1000)**(-2)))
    
    #returning the final frequency time plot, sum plot, the location of where the candidates is,
    #maximum frequency, difference between different frequencies, dispersion measure in actual units
    return final, sum_, new_imp_start//bins, max_f, matrix.header.foff, dm

#%%calling the functions
candidates = f"/scratch2/aga017/output/{tape_no}/slotter_results/{tape_no}_{observation}_.txt"
candidates = np.loadtxt(candidates, dtype=str)
candidates = candidates[1:,:].astype(float)
    

for i in range(len(candidates)):
    imp_start = int(float(candidates[i,0]))    
    dm = int(float(candidates[i,2]))
    bins = int(float(candidates[i,1]))
    SNR = round(float(candidates[i,3]),2)
    beam = int(candidates[i,-1])
    beam = "{:03}".format(beam)

    filter_bank = f"/scratch2/aga017/utmost_data/{tape_no}/{observation}/FB/BEAM_{beam}/{observation}.fil"
    
    out, sum_, idx, max_f, f_off, dm = plotter(filter_bank, dm, imp_start, bins, 50)
    
    dm = '%.3g' % dm
    bins = '%.3g' % (bins * ((2**16)/100000000))
    
    fig = plt.figure(figsize=(18, 11))
    
    ax0 = plt.subplot2grid(shape = (6, 1), loc = (0, 0), rowspan = 5, colspan = 1, fig = fig)
    ax1 = plt.subplot2grid(shape = (6, 1), loc = (5, 0), rowspan = 1, colspan = 1, fig = fig, sharex = ax0)
    plt.subplots_adjust(hspace = 0)
    
    
    ax0.set_title(f"DM = {dm} pc.cm$^{3}$, Sample # = {imp_start} \n Pulse Width = {bins} sec, S/N = {SNR}", y = 1.05)
    
    ax0.imshow(out, aspect = 'auto', interpolation = 'None')

    ax0.axes.get_xaxis().set_visible(False)
    y_ticks = ax0.get_yticks()
    new_ticks = [round((f_off*y + max_f),2) for y in y_ticks]    
    ax0.set_yticklabels(new_ticks)
    ax0.set_ylabel("Frequency in MHz")
    ax2 = ax0.twinx()
    ax2.set_ylim(40, 0)
    ax2.set_yticks([0, 8, 16, 24, 32, 40])
    ax2.set_ylabel("Channel #")

    ax1.plot(sum_, 'r-')
    #ax1.plot(idx, sum_[idx], '*')
    ax1.set_yticks([])
    ax1.axes.get_xaxis().set_visible(False)
    name = f"/scratch2/aga017/output/{tape_no}/plotter_results/{tape_no}_{observation}_{beam}_{i}.png"   
    fig.savefig(name, format = 'png', dpi = 70)    
    print(f"Saved: {tape_no}_{observation}_{beam}_{i}.png")
    if i % 20 == 0:
        plt.close('all')

    
    
    
    
    
    
    
    
    
    
    