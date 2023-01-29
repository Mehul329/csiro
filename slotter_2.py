#import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
import os
import time

def cluster_all_beams(tape, obs_no, time_scale, dm_scale, box_scale, beam_scale, radius):
    #dm_scale = within what range of DM would you consider it one cluster = 40
    #time_scale = within what range of time would you consider it one cluster = 50
    #beam_scale = within what range of beams would you consider it one cluster = 4
    #radius = radius under whihc you will mkae one cluster = 1.1  
    beam_cands = np.array([0,0,0,0,0])
    beams = np.linspace(2,352,352-2+1).astype(int)
    beams = np.core.defchararray.zfill(beams.astype(str), 3)
    for beam in beams:
        path = '/scratch2/aga017/output/'+tape+'/'+tape+'_'+obs_no+'_BEAM_'+beam+'.txt' 
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
    #fig.savefig('3d11dasdadasd11plt.png', format = 'png', dpi = 300)   
    print(f'Reduced from {len(beam_cands)} to {n_clusters} to {count} in {time.time()-start}')
    
    return final_cands

tape = 'SM0006L6'
obs_no = '2018-03-01-14:17:51'
final_cands = np.array(cluster_all_beams(tape, obs_no, 100, 40, 20, 5, 1.1))
header = np.array(['Time', 'Boxcar', 'DM', 'SNR', 'BEAM'])
final_cands = np.row_stack([header, final_cands])
outname = '/scratch2/aga017/output/'+tape+'/'+tape+'_'+obs_no+'__.txt'
np.savetxt(outname, final_cands, fmt = '%s')
#print(f"Total time taken for this obs : {time.time()-start}")


'''
cands1 = np.loadtxt('/Users/mehulagarwal/Desktop/Finder_Results/obs/this_235.txt', dtype='str')
cands1 = cands1[1:,:].astype(float)
cands1 = np.column_stack([cands1, 235*np.ones_like(cands1[:,0])]) 

cands2 = np.loadtxt('/Users/mehulagarwal/Desktop/Finder_Results/obs/this_236.txt', dtype='str')
cands2 = cands2[1:,:].astype(float)
cands2 = np.column_stack([cands2, 236*np.ones_like(cands2[:,0])]) 

cands3 = np.loadtxt('/Users/mehulagarwal/Desktop/Finder_Results/obs/this_237.txt', dtype='str')
cands3 = cands3[1:,:].astype(float)
cands3 = np.column_stack([cands3, 237*np.ones_like(cands3[:,0])]) 

cands4 = np.loadtxt('/Users/mehulagarwal/Desktop/Finder_Results/obs/this_238.txt', dtype='str')
cands4 = cands4[1:,:].astype(float)
cands4 = np.column_stack([cands4, 238*np.ones_like(cands4[:,0])]) 

cands5 = np.loadtxt('/Users/mehulagarwal/Desktop/Finder_Results/obs/this_239.txt', dtype='str')
cands5 = cands5[1:,:].astype(float)
cands5 = np.column_stack([cands5, 239*np.ones_like(cands5[:,0])]) 

cands = np.row_stack([cands1, cands2, cands3, cands4, cands5])

final_cands = cluster_all_beams(cands, 100, 40, 20, 5, 1.1)
'''
