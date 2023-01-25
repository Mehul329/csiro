#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 11:09:57 2023

@author: aga017
"""

import time
import numpy as np
from numba import jit
import os
#%%
#this porgram should go into each observation (327) and cluster data for all beams at once
#it take the location of observations number


file1 = '/u/aga017/Desktop/output'
beams = os.listdir(file1) 


cands = np.loadtxt(file1+'/'+beams[174], dtype='str')
cands = cands[1:,:].astype(float)

@jit(nopython=True)
def box_remover(array):
    final_cands = np.zeros_like(cands)
    DMs = np.unique(cands[:,2])
    count = 0
    for DM in DMs:
        cands_2 = cands[cands[:,2] == DM]
        times = np.unique(cands_2[:,0])
        for time_ in times:
            cands_3 = cands_2[cands_2[:,0] == time_]
            final_cand = cands_3[cands_3[:,-1] == np.max(cands_3[:,-1])]
            final_cands[count] = final_cand
            count += 1
    return final_cands[:count]

start = time.time()
cands = np.loadtxt(file1+'/'+beams[174], dtype='str')
cands = cands[1:,:].astype(float)
lst = box_remover(cands)
cands = np.loadtxt(file1+'/'+beams[175], dtype='str')
cands = cands[1:,:].astype(float)
lst = box_remover(cands)
cands = np.loadtxt(file1+'/'+beams[176], dtype='str')
cands = cands[1:,:].astype(float)
lst = box_remover(cands)
print(time.time()-start)