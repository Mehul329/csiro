#import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
import os
import time
import argparse


#%%

a = argparse.ArgumentParser()
a.add_argument('-t', type = str, help = 'Type the tape without /')
a.add_argument('-o', type = str, help = 'Type the observation without /')
a.add_argument('-t_s', type = float, help = 'Give the value for time scaling', default = 100)
a.add_argument('-d_s', type = float, help = 'Give the value for DM scaling', default = 40)
a.add_argument('-bx_s', type = float, help = 'Give the value for boxcar scaling', default = 20)
a.add_argument('-b_s', type = float, help = 'Give the value for beam scaling', default = 5)
a.add_argument('-r', type = float, help = 'Give the radius for clustering', default = 1.1)

args = a.parse_args()
tape = args.t
observation = args.o
time_scale = args.t_s
dm_scale = args.d_s
box_scale = args.bx_s
beam_scale = args.b_s
radius = args.r

#%%
#this porgram should go into each observation (327) and cluster data for all beams at once
#it take the location of observations number

def cluster_each_beam(beam_cands, time_scale, dm_scale, box_scale, radius, beam_no):
    #dm_scale = within what range of DM would you consider it one cluster = 40
    #time_scale = within what range of time would you consider it one cluster = 50
    #box_scale = within what range of boxcar would you consider it one cluster = 20
    #radius = radius under whihc you will mkae one cluster = 1.1    
    
    cls_obj = DBSCAN(eps=radius, min_samples=1)
    times = beam_cands[:,0] / time_scale
    dms = beam_cands[:,2] / dm_scale
    boxcars = beam_cands[:,1] / box_scale   
    
    start = time.time()
    clusters = cls_obj.fit(np.column_stack([times, dms, boxcars])).labels_
    
    cand_lst = []
    
    n_clusters = max(clusters)+1
    print(f'{beam_no} reduced from {len(beam_cands)} to {n_clusters} in {time.time()-start}')
    #plt.figure()
    for icluster in range(n_clusters):
        cand = beam_cands[icluster == clusters]
        final_cand = cand[np.where(cand[:,3]==np.max(cand[:,3]))[0]][0]
        #plt.plot(final_cand[0], final_cand[2], '.')
        final_cand = np.append(final_cand, beam_no)
        cand_lst.append(final_cand)
    #plt.show()
    cand_lst = np.array(cand_lst)
    return cand_lst


def cluster_all_beams(filtered_beams, time_scale, dm_scale, beam_scale, radius):
    #dm_scale = within what range of DM would you consider it one cluster = 40
    #time_scale = within what range of time would you consider it one cluster = 50
    #beam_scale = within what range of beams would you consider it one cluster = 4
    #radius = radius under whihc you will mkae one cluster = 1.1  
    cls_obj = DBSCAN(eps=radius, min_samples=1)
    times = filtered_beams[:,0] / time_scale
    dms = filtered_beams[:,2] / dm_scale
    beams = filtered_beams[:,-1] / beam_scale 

    start = time.time()
    clusters = cls_obj.fit(np.column_stack([times, dms, beams])).labels_   
    
    final_cands = []
    
    n_clusters = max(clusters)+1
    count = 0
    #plt.figure()
    for icluster in range(n_clusters):
        cand = filtered_beams[icluster == clusters]
        min_beam = np.min(cand[:,-1])
        max_beam = np.max(cand[:,-1]) 
        #plt.plot(cand[:,-1], cand[:,0], '-')
        if max_beam - min_beam < 2:
            candidate = cand[cand[:,-2] == np.max(cand[:,-2])][0]
            final_cands.append(candidate)
            count+=1
            #plt.plot(candidate[0], candidate[2], '-')
    #plt.ylim([0,250])
    #plt.show()
    print(f'Reduced from {len(filtered_beams)} to {n_clusters} to {count} in {time.time()-start}')
    
    return final_cands

start = time.time()
filtered_beams = []
beams = np.linspace(2,352,352-2+1).astype(int)
beams = np.core.defchararray.zfill(beams.astype(str), 3)
for beam in beams:
    path = '/scratch2/aga017/output/'+tape+'/'+tape+'_'+observation+'_BEAM_'+beam+'.txt' 
    print(path)
    if os.path.exists(path):
        beam_cand = np.loadtxt(path, dtype='str')
        beam_cand = beam_cand[1:,:].astype(float)     
        filtered_beams.extend(cluster_each_beam(beam_cand, time_scale, dm_scale, box_scale, radius, int(beam)))
    else:
        print(f"{path} does not exist")
    
filtered_beams = np.array(filtered_beams)
final_cands = np.array(cluster_all_beams(filtered_beams, time_scale, dm_scale, beam_scale, radius))
header = np.array(['Time', 'Boxcar', 'DM', 'SNR', 'BEAM'])
final_cands = np.row_stack([header, final_cands])
outname = '/scratch2/aga017/output/'+tape+'/'+tape+'_'+observation+'_.txt'
np.savetxt(outname, final_cands, fmt = '%s')
print(f"Total time taken for this obs : {time.time()-start}")
