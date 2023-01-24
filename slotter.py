import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
import os
#%%
#this porgram should go into each observation (327) and cluster data for all beams at once
#it take the location of observations number

file1 = '/u/aga017/Desktop/output'
beams = os.listdir(file1) 
cand_list = []

cls_obj = DBSCAN(eps=1.1, min_samples=1)
for i in range(len(beams)):
    beam_no = int(beams[i].split('_')[1].split('.')[0])
    if beam_no in [173,174]:#175,176,177,178,179]:
        print(beams[i])
        cands = np.loadtxt(file1+'/'+beams[i], dtype='str')
        cands = cands[1:,:].astype(float) / 20
        time = cands[:,0]
        DM = cands[:,2] / 2
        clusters = cls_obj.fit(np.column_stack([time, DM])).labels_
        final_cands = []
        n_clusters = max(clusters)+1
        plt.figure()
        for icluster in range(n_clusters):
            cand = cands[icluster == clusters]
            final_cand = cand[np.where(cand[:,3]==np.max(cand[:,3]))[0]]
            final_cand = np.append(final_cand, beam_no)
            final_cands.append(final_cand)
        print(n_clusters)
        final_cands = np.array(final_cands)
        final_cands[:, 3] *= 20
        cand_list.extend(final_cands)
        plt.plot(final_cands[:,0]*20, final_cands[:,1]*20, '.')
        plt.xlim([0,600000])
        plt.show()
cand_list = np.array(cand_list)
np.save('/u/aga017/Desktop/beams_clustered', cand_list)

