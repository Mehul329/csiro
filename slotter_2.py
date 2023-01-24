import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
import os
#%%
#this porgram should go into each observation (327) and cluster data for all beams at once
#it take the location of observations number

file1 = '/u/aga017/Desktop/beams_clustered.npy'
data = np.load(file1)
plt.figure()
#plt.axes(projection='3d')
plt.plot(data[data[:,-1]==176][:,2], data[data[:,-1]==176][:,0], '.')
plt.show()

cls_obj = DBSCAN(eps=1.1, min_samples=1)

#3d time dm beam
clusters = cls_obj.fit(np.column_stack([data[:,-1]/5, data[:,2]/10, data[:,0]/100])).labels_

#time beam
#clusters = cls_obj.fit(np.column_stack([data[:,-1], 0.5*data[:,0]])).labels_

#dm beam
#clusters = cls_obj.fit(np.column_stack([data[:,-1], data[:,2]])).labels_

n_clusters = max(clusters)+1
plt.figure()
#plt.axes(projection='3d')
count = 0
plot_cands = []
for icluster in range(n_clusters):
    cand = data[icluster == clusters]
    min_beam = np.min(cand[:,-1])
    max_beam = np.max(cand[:,-1])
    if max_beam - min_beam < 3:
        candidate = cand[cand[:,-2] == np.max(cand[:,-2])][0]
        plot_cands.append(candidate)
        count+=1
        plt.plot(candidate[-1], candidate[0], '.')
        #plt.plot(cand[:,-1], cand[:,0], '.')
        #plt.plot(cand[:,-1], cand[:,0], cand[:,1], '.')
plt.show()
print(count)
print(n_clusters)
np.save('/u/aga017/Desktop/plot_cands', np.array(plot_cands))

