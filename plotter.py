import matplotlib.pyplot as plt
from sigpyproc.readers import FilReader as F
import numpy as np


def flatten(time_series, interval):
    xx = np.arange(len(time_series))
    model = np.poly1d(np.polyfit(xx[::interval], time_series[::interval], 2 ))
    y = model[2] * xx**2 + model[1] * xx + model[0]
    return time_series - y


def average(array, idx, bins):
    if idx%bins == 0:
        out = array
        idx_2 = idx
    else:
        out = np.pad(array, (bins - idx%bins, 0), 'constant')
        idx_2 = idx + bins - idx%bins
    
    if (len(array) - (idx+bins)) % bins == 0:
        out = out
    else:
        end = bins - (len(array) - (idx+bins)) % bins
        out = np.pad(out, (0, end), 'constant')
    
    out_1 = np.reshape(out, [int(len(out)/bins),bins]) #reshapes
    idx_2 = idx_2//bins
    out_2 = np.sum(out_1, axis=1)
    non_zero_count = np.count_nonzero(out_1, axis=1)
    out_2 = out_2 / non_zero_count
    return out_2, idx_2

def middle(a, idx, points):

    left_out_end = len(a) - (idx+1)
    if (left_out_end < points) and (left_out_end < idx):
        start = idx-left_out_end
        end = -1
        a = a[idx-left_out_end:]
        idx = left_out_end
    elif (idx < left_out_end) and (idx < points):
        start = 0
        end = idx+idx+1
        a = a[:idx+idx+1]
    else:
        start = idx-points
        end = idx+points+1
        a = a[idx-points:idx+points+1]
        idx = points
    return a, start, end, idx

    

def plotter(matrix, dm, imp_start, bins):
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
        
        start = int((a/(freq[j]))**2 - b)
        end = start + c
 

        channel = matrix[j][start:end]
        channel, idx_2 = average(channel,imp_start,bins)
        final.append(channel)

    sum_ = np.average(final, axis = 0)
    sum_ =  flatten(sum_, 1)
    sum_, start, end, max_ = middle(np.array(sum_), idx_2, 50)
    final = np.array(final)
    if end == -1:
        final = final[:, start:]
    else:
        final = final[:, start:end]
    plt.subplots_adjust(hspace = 0)
    ax0.imshow(final, aspect = 'auto', interpolation = 'None')
    ax0.axes.get_xaxis().set_visible(False)
    ax1.plot(sum_, 'r-')
    ax1.plot(max_, sum_[max_], 'b*')
    plt.show()
    return final, sum_


try:
    candidates = np.loadtxt('/u/aga017/Desktop/time_dm.txt', dtype = str)
except:
    candidates = np.loadtxt('/Users/mehulagarwal/Downloads/time_dm.txt', dtype = str)
candidates = candidates[1:]

for i in range(1, len(candidates)):
    dm = int(float(candidates[i,2]))
    imp_start = int(float(candidates[i,0]))
    SNR = round(float(candidates[i,3]),2)
    bins = int(float(candidates[i,1]))
    out, sum_ = plotter('/Users/mehulagarwal/Downloads/2018-07-08-02 58 17.fil', dm, imp_start, bins)