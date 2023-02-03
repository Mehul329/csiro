#this progrmam takes the tape number and observation number as the input and then
#clusters all the potential candidates in that observation (whihc is basically 352 beams * candidates)
#in 4 dimension using time, dm, average in width and beam number. This will prove to be useful if 
#we can break single filter banks to small chunks. Or techincally, when reading the text file, check 
#if the sample number is within the chosne chunk size. Right now the input for this program is tape number
#and observation number. It will combine all the candidates from each beam into one array and run the
#clustering. This program assumes that the potential canidates from finder program are stored 
#in the following way:
#/scratch2/aga017/output/tape_no/finder_results/tape_no_obs_no_Beam_no.txt

#%% importing modules

#import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
import os
import time
import argparse

#%% Input definition

a = argparse.ArgumentParser()
a.add_argument('-t', type = str, help = 'Type the tape no. like SM0006L6')
a.add_argument('-o', type = str, help = 'Type the observation no. like 2018-03-01-14:17:51')
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

#%% Function definitions

def cluster_all_beams(tape, obs_no, time_scale, dm_scale, box_scale, beam_scale, radius):
    #dm_scale = within what range of DM would you consider it one cluster = 40
    #time_scale = within what range of time would you consider it one cluster = 50
    #beam_scale = within what range of beams would you consider it one cluster = 4
    #radius = radius under whihc you will mkae one cluster = 1.1  
    beam_cands = np.array([0,0,0,0,0])
    beams = np.linspace(2,352,352-2+1).astype(int)
    beams = np.core.defchararray.zfill(beams.astype(str), 3)
    for beam in beams:
        path = '/scratch2/aga017/output/'+tape+'/'+'finder_results/'+tape+'_'+obs_no+'_BEAM_'+beam+'.txt' 
        print(path)
        if os.path.exists(path):
            beam_cand = np.loadtxt(path, dtype='str')
            beam_cand = beam_cand[1:,:].astype(float)  
            beam_cand = np.column_stack([beam_cand, int(beam)*np.ones_like(beam_cand[:,0])]) 
            beam_cands = np.row_stack([beam_cands, beam_cand])
        else:
            print(f"{path} does not exist")
    
    beam_cands = beam_cands[1:,:]
    cls_obj = DBSCAN(eps=radius, min_samples=1)
    times = beam_cands[:,0] / time_scale
    dms = beam_cands[:,2] / dm_scale
    boxcars = beam_cands[:,1] / box_scale   
    beams = beam_cands[:,-1] / beam_scale 

    start = time.time()
    clusters = cls_obj.fit(np.column_stack([times, dms, beams, boxcars])).labels_   
    
    final_cands = []
    
    n_clusters = max(clusters)+1
    count = 0
    #plt.figure()
    #fig, axs = plt.subplots(2, 3, figsize=(20, 10))
    for icluster in range(n_clusters):
        cand = beam_cands[icluster == clusters]
        #axs[0, 0].plot(cand[:,0], cand[:,1], '.')
        #axs[0, 1].plot(cand[:,0], cand[:,2], '.')
        #axs[0, 2].plot(cand[:,0], cand[:,3], '.')
        #axs[1, 0].plot(cand[:,1], cand[:,2], '.')
        #axs[1, 1].plot(cand[:,1], cand[:,3], '.')
        #axs[1, 2].plot(cand[:,2], cand[:,3], '.')  
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
    #plt.show()   
    print(f'Reduced from {len(beam_cands)} to {n_clusters} to {count} in {time.time()-start}')
    
    return final_cands

#%%Calling the function
final_cands = np.array(cluster_all_beams(tape, observation, time_scale, dm_scale, box_scale, beam_scale, radius))
header = np.array(['Time', 'Boxcar', 'DM', 'SNR', 'BEAM'])
final_cands = np.row_stack([header, final_cands])
outname = '/scratch2/aga017/output/'+tape+'/'+tape+'_'+observation+'__.txt'
np.savetxt(outname, final_cands, fmt = '%s')

