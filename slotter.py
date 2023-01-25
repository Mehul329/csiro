import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
import os
#%%
#this porgram should go into each observation (327) and cluster data for all beams at once
#it take the location of observations number
import time
file1 = '/u/aga017/Desktop/output'
beams = os.listdir(file1) 
beams = beams[:4]
cand_list = []

def cluster_each_beam(beam_cands, time_scale, dm_scale, box_scale, radius, beam_no):
    #dm_scale = within what range of DM would you consider it one cluster = 40
    #time_scale = within what range of time would you consider it one cluster = 200
    #box_scale = within what range of boxcar would you consider it one cluster = 100
    #radius = radius under whihc you will mkae one cluster = 1.1    
    
    cls_obj = DBSCAN(eps=radius, min_samples=1)
    times = beam_cands[:,0] / time_scale
    dms = beam_cands[:,2] / dm_scale
    boxcars = beam_cands[:,1] / box_scale   
    
    start = time.time()
    clusters = cls_obj.fit(np.column_stack([times, dms, boxcars])).labels_
    
    final_cands = []
    
    n_clusters = max(clusters)+1
    print(time.time()-start)
    plt.figure()
    for icluster in range(n_clusters):
        cand = beam_cands[icluster == clusters]
        final_cand = cand[np.where(cand[:,3]==np.max(cand[:,3]))[0]][0]
        plt.plot(final_cand[0], final_cand[1], '.')
        final_cand = np.append(final_cand, beam_no)
        final_cands.append(final_cand)
    plt.show()
    final_cands = np.array(final_cands)
    return final_cands
    
beam_cands = np.loadtxt(file1+'/BEAM_176.txt', dtype='str')
beam_cands = beam_cands[1:,:].astype(float)
cluster_each_beam(beam_cands, 200, 40, 100, 1.1, 176)

'''
cls_obj = DBSCAN(eps=1.1, min_samples=1)
for i in range(len(beams)):
    beam_no = int(beams[i].split('_')[1].split('.')[0])
    
    print(beams[i])
    cands = np.loadtxt(file1+'/'+beams[i], dtype='str')
    cands = cands[1:,:].astype(float)
    time = cands[:,0]
    DM = cands[:,2]
    clusters = cls_obj.fit(np.column_stack([time, DM])).labels_
    final_cands = []
    n_clusters = max(clusters)+1
    plt.figure()
    plt.plot(time, DM, '.')
    plt.show()
    
    for icluster in range(n_clusters):
        cand = cands[icluster == clusters]
        final_cand = cand[np.where(cand[:,3]==np.max(cand[:,3]))[0]]
        final_cand = np.append(final_cand, beam_no)
        final_cands.append(final_cand)
    print(n_clusters)
    final_cands = np.array(final_cands)
    final_cands[:, 3] *= 20
    cand_list.extend(final_cands)
    plt.plot(final_cands[:,0]*20, final_cands[:,2]*20, '.')
    plt.xlim([0,600000])
    plt.show()
    
    break
cand_list = np.array(cand_list)
#np.save('/u/aga017/Desktop/beams_clustered', cand_list)
'''
