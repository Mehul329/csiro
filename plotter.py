import matplotlib.pyplot as plt
from sigpyproc.readers import FilReader as F
import numpy as np


def flatten(time_series, interval):
    xx = np.arange(len(time_series))
    model = np.poly1d(np.polyfit(xx[::interval], time_series[::interval], 2 ))
    y = model[2] * xx**2 + model[1] * xx + model[0]
    return time_series - y

def plotter(matrix, dm, imp_start, bins, blocks):
    fig = plt.figure()
    ax0 = plt.subplot2grid(shape = (3, 1), loc = (0, 0), rowspan = 2, colspan = 1, fig = fig)
    ax0.set_title(f"DM = {dm}, First seen = {imp_start}, bins = {bins}, S/R = {SNR}")
    ax1 = plt.subplot2grid(shape = (3, 1), loc = (2, 0), rowspan = 1, colspan = 1, fig = fig, sharex = ax0)
    
    matrix = F(matrix)
    nsamps = matrix.header.nsamples
    n_chans = matrix.header.nchans
    max_f = matrix.header.fch1
    min_f = max_f + matrix.header.foff * (n_chans-1)
    
    matrix = matrix.read_block(0, nsamps)

    b = ((min_f/max_f)**2)*dm/(1-(min_f/max_f)**2)
    a = max_f*((b)**0.5)
    freq = np.linspace(max_f, min_f, n_chans)

    c = nsamps - int((a/(freq[-1]))**2 - b)

    final = []
    for j in range(n_chans):
        #imp = int((a/(freq[j]))**2 - b) + imp_start
        
        temp_start = int((a/(freq[j]))**2 - b)
        temp_end = temp_start + c
        
        channel = matrix[j][temp_start:temp_end]
        
        rem_start = imp_start%bins
        start_blocks_av = (imp_start - rem_start)//bins

        if start_blocks_av <= blocks:
            start = rem_start
        else:
            extra_block = start_blocks_av - blocks
            start = rem_start + extra_block * bins

        rem_end = (len(a)-(imp_start + bins))%bins
        end_blocks_av = (len(a)-(imp_start + bins))//bins

        if end_blocks_av <= blocks:
            end = rem_end
        else:
            extra_block = end_blocks_av - blocks
            end = (len(a)-(imp_start + bins)) - extra_block * bins
            
        print(start, -end)
        if rem_end == 0:    
            print(a[start:])
        else:
            print(a[start:-end])
            
        
        channel, idx_2 = average(channel,imp_start,bins)
        final.append(channel)

    sum_ = np.average(final, axis = 0)
    sum_ =  flatten(sum_, 1)
    sum_, start, end, max_ = middle(np.array(sum_), idx_2, 25)
    final = np.array(final)
    if end == -1:
        final = final[:, start:]
    else:
        final = final[:, start:end]
    plt.subplots_adjust(hspace = 0)
    ax0.imshow(final, aspect = 'auto', interpolation = 'None')
    ax0.axes.get_xaxis().set_visible(False)
    ax1.plot(sum_, 'r-')
    #ax1.plot(max_, sum_[max_], 'b*')
    plt.show()
    return final, sum_


candidates = np.loadtxt('/u/aga017/Desktop/Output/SM0006L6_2018-03-01-14:17:51_BEAM_352.txt', dtype=str)
candidates = candidates[1:,:].astype(float)
    

for i in range(1, len(candidates)):
    dm = int(float(candidates[i,2])) * 20
    imp_start = int(float(candidates[i,0])) * 20
    SNR = round(float(candidates[i,3]),2)
    bins = int(float(candidates[i,1])) * 20
    beam = int(candidates[i,-1])
    beam_file = str(np.core.defchararray.zfill(str(beam), 3))
    filter_bank = '/u/aga017/Desktop/2018-03-01-14:17:51/BEAM_'+beam_file+'/2018-03-01-14:17:51.fil'
    out, sum_ = plotter(filter_bank, dm, imp_start, bins)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        