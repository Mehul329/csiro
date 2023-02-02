#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 08:23:07 2023

@author: mehulagarwal
"""
import numpy as np
import matplotlib.pyplot as plt

samps = 100
chans = np.linspace(800,840,10)
x = np.linspace(0,samps,samps)
'''
data = np.random.normal(0,0.5,[len(chans),samps])


#plotting the original data from a telescope
for i in range(len(chans)):
    data[i] = data[i] + chans[i]
    plt.plot(x, data[i], '-')
plt.show()

np.save('data', data)
'''
def coeffs(chans, imp_start, imp_end):
    b = (((min(chans)/max(chans))**0.5)*imp_end - imp_start)/(((min(chans)/max(chans))**0.5)-1)
    a = max(chans) * (imp_start - b)**2
    return a, b
    
#%%
imp_start = 20
imp_end = 20
sigma = 0.5
'''
#now plotting the data with high sigma at a single time stamp
y = np.load('data.npy')
a, b = coeffs(chans, imp_start, imp_end)
for i in range(len(chans)):
    idx_imp = int((a/chans[i])**0.5 + b)
    y[i][idx_imp]+=sigma
    plt.plot(x, y[i], '-')
plt.savefig('1.png', format = 'png', dpi = 300) #disable this on your machine or change accordingly
plt.show()
'''

'''
y = np.load('data.npy')
a, b = coeffs(chans, imp_start, imp_end)
#now start plotting the data with lower sigmas at a single time stamp
sigma = np.linspace(4,1,10)
for i in range(len(sigma)):
    y = np.load('data.npy')
    for j in range(len(chans)):
        idx_imp = int((a/chans[j])**0.5 + b)
        y[j, idx_imp]=y[j, idx_imp]+sigma[i]
        plt.plot(x, y[j], '-')
    
    plt.savefig(str(sigma[i])+'.png', format = 'png', dpi = 300) #disable this on your machine or change accordingly
    plt.show()
'''

'''
a, b = coeffs(chans, imp_start, imp_end)
#now start plotting the above data with sum along the axis
sigma = np.linspace(4,1,10)
for i in range(len(sigma)):
    fig = plt.figure()
    ax0 = plt.subplot2grid(shape = (3, 1), loc = (0, 0), rowspan = 2, colspan = 1, fig = fig)
    ax0.set_title('something')
    ax1 = plt.subplot2grid(shape = (3, 1), loc = (2, 0), rowspan = 1, colspan = 1, fig = fig, sharex = ax0)
    plt.subplots_adjust(hspace = 0)
    y = np.load('data.npy')
    for j in range(len(chans)):
        idx_imp = int((a/chans[j])**0.5 + b)
        y[j][idx_imp]+=sigma[i]
        ax0.plot(x, y[j], '-')
    sum_ = np.average(y,axis = 0)
    ax0.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)
    ax1.plot(sum_, 'r-')
    plt.savefig(str(sigma[i])+'.png', format = 'png', dpi = 300) #disable this on your machine or change accordingly
    plt.show()
'''

'''
#now start a mediocere sigma but disperesed
for i in range(10,60):
    fig = plt.figure()
    ax0 = plt.subplot2grid(shape = (3, 1), loc = (0, 0), rowspan = 2, colspan = 1, fig = fig)
    ax0.set_title(f'Dispersing it by {60-i} samples')
    ax1 = plt.subplot2grid(shape = (3, 1), loc = (2, 0), rowspan = 1, colspan = 1, fig = fig, sharex = ax0)
    plt.subplots_adjust(hspace = 0)
    imp_end = i
    b = (((min(chans)/max(chans))**0.5)*imp_end - imp_start)/(((min(chans)/max(chans))**0.5)-1)
    a = max(chans) * (imp_start - b)**2
    y = np.load('data.npy')
    for j in range(len(chans)):
        idx_imp = int((a/chans[j])**0.5 + b)
        if imp_end < imp_start:  
            idx_imp = int(-(a/chans[j])**0.5 + b)
        y[j][idx_imp]+=3
        ax0.plot(x, y[j], '-')
    sum_ = np.average(y,axis = 0)
    ax0.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.plot(sum_, 'r-')
    plt.savefig(str(i)+'.png', format = 'png', dpi = 300) #disable this on your machine or change accordingly
    plt.show()
'''
'''
def averge_in_time(time_series, binssize_samp, tstart_samp, tsamp=1):
    
    rms = time_series[:tstart_samp].std()
    
    area_under_the_boxcar = time_series[tstart_samp:tstart_samp + binssize_samp].sum()
    snr_for_boxcar = area_under_the_boxcar / np.sqrt(binssize_samp) / rms

    return snr_for_boxcar

x = np.linspace(0,10000,10000)
y = np.random.normal(0,0.2,[10000,1])
idx_imp = 5000
y[idx_imp:idx_imp+1000]+=3
bins = np.linspace(600,1300,8).astype(int)
for bin_ in bins:
    print(bin_, averge_in_time(y, bin_, idx_imp, tsamp=1))
'''    

'''
#now add sigma to a breadth
fig = plt.figure(figsize=(10, 2))
idx_imp = 5000
x = np.linspace(0,10000,10000)
y = np.random.normal(0,0.2,[10000,1])
y[idx_imp:idx_imp+1000]+=3
plt.plot(x, y, '-')
plt.savefig(str(60)+'.png', format = 'png', dpi = 900) #disable this on your machine or change accordingly
plt.show()

rms = np.std(y)
bins = np.linspace(600,1300,8).astype(int)

for k in bins:
    rem_start = idx_imp % k
    start_blocks_av = (imp_start - rem_start)//k
        
    start = rem_start
    
    rem_end = (len(y)-(idx_imp + k))%k
    end_blocks_av = (len(y)-(idx_imp + k))//k
        
    if rem_end == 0:
        avg = y[rem_start:]
    else:
        avg = y[rem_start:-rem_end]
        
    avg /= ((rms * np.sqrt(k))/k)
    print(k)
    avg = avg.reshape(len(avg)//k, k).mean(axis = 1)
    print(avg)
    plt.plot(avg)
    plt.title(f"{k} {max(avg)}")
    plt.show()
'''

import numpy as np

def gaussian(x, mean, std):
    return 8*np.exp(-((x - mean)**2)/(2 * std**2))

x = np.linspace(0,1000,1000)
y1 = gaussian(x, 500, 60)
y2 = np.random.normal(0,0.2,[1000,1])
for i in range(len(y1)):
    y2[i] = y2[i] + y1[i]
fig = plt.figure(figsize=(10, 2))
plt.plot(x, y2, '.')
plt.xlim([0,1000])
plt.savefig(str(60)+'.png', format = 'png', dpi = 900) #disable this on your machine or change accordingly
plt.show()
