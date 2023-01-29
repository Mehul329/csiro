import matplotlib.pyplot as plt
from sigpyproc.readers import FilReader as F
import numpy as np
import argparse

a = argparse.ArgumentParser()
a.add_argument('-t', type = str, help = 'Give the tape name')
a.add_argument('-o', type = str, help = 'Give the observation ')

args = a.parse_args()
tape_no = args.t
observation = args.o

def flatten(time_series, interval):
    xx = np.arange(len(time_series))
    model = np.poly1d(np.polyfit(xx[::interval], time_series[::interval], 2 ))
    y = model[2] * xx**2 + model[1] * xx + model[0]
    return time_series - y

def plotter(matrix, dm, imp_start, bins, blocks):
    
    matrix = F(matrix)
    nsamps = matrix.header.nsamples
    n_chans = matrix.header.nchans
    max_f = matrix.header.fch1
    min_f = max_f + matrix.header.foff * (n_chans-1)
    
    matrix = matrix.read_block(0, nsamps)

    b = ((min_f/max_f)**2)*dm/(1-(min_f/max_f)**2) #constant in equation
    a = max_f*((b)**0.5) #constant in equation
    freq = np.linspace(max_f, min_f, n_chans)

    c = nsamps - int((a/(freq[-1]))**2 - b) #length of each channel
    
    imp = int((a/(freq[0]))**2 - b) + imp_start

    final = np.empty([n_chans,c])
    for j in range(n_chans):

        temp_start = int((a/(freq[j]))**2 - b)
        temp_end = temp_start + c
        
        final[j] = matrix[j][temp_start:temp_end]

    rem_start = imp % bins
    start_blocks_av = (imp - rem_start)//bins

    if start_blocks_av <= blocks:
        start = rem_start
    else:
        extra_block = start_blocks_av - blocks
        start = rem_start + extra_block * bins

    new_imp_start = imp - start
    
    rem_end = (c-(imp + bins))%bins
    end_blocks_av = (c-(imp + bins))//bins

    if end_blocks_av <= blocks:
        end = rem_end
    else:
        extra_block = end_blocks_av - blocks
        end = (c-(imp + bins)) - blocks * bins
        
    if end == 0:    
        final = final[:,start:]
    else:
        final = final[:,start:-end]
        
        

    final = final.reshape(n_chans, len(final[0])//bins, bins).mean(axis=-1)
    #plt.imshow(final, aspect = 'auto')

    
    sum_ = np.average(final, axis = 0)
    sum_ = flatten(sum_, 5)
    
    dm = ((dm * ((2**16)/100000000))*1000)/(4.15*((min_f/1000)**(-2) - (max_f/1000)**(-2)))
    
    return final, sum_, new_imp_start//bins, max_f, matrix.header.foff, dm

candidates = f"/scratch2/aga017/output/{tape_no}/slotter_results/{tape_no}_{observation}_.txt"
candidates = np.loadtxt(candidates, dtype=str)
candidates = candidates[1:,:].astype(float)
candidates = candidates[(candidates[:,-1] > 120) & (candidates[:,-1] < 160)]
    

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
    ax1.plot(idx, sum_[idx], '*')
    ax1.set_yticks([])
    ax1.axes.get_xaxis().set_visible(False)
    name = f"/scratch2/aga017/output/{tape_no}/plotter_results/{tape_no}_{observation}_{beam}_{i}.png"   
    fig.savefig(name, format = 'png', dpi = 70)    
    print(f"Saved: {tape_no}_{observation}_{beam}_{i}.png")
    if i % 20 == 0:
        plt.close('all')

    
    
    
    
    
    
    
    
    
    
    