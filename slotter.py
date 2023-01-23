import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
import sys
import os
#%%
#this porgram should go into each observation (327) and cluster data for all beams at once
#it take the location of observations number

file1 = '/u/aga017/Desktop/For_slotter'
beams = os.listdir(file1) 

cand_list = []
max = 0
for i in range(4):
    cands = np.loadtxt(file1+'/'+beams[i], dtype='str')
    cands = cands[1:,:].astype(float)
    if len(cands) > max:
        max = len(cands)
    cand_list.extend(cands)
cand_list = np.array(cand_list)
np.save('/u/aga017/Desktop/big_list.npy', cand_list)
print(max)

cands = np.load('/u/aga017/Desktop/big_list.npy')
time = cands[:,0]/20
boxcar = 20*cands[:,1]/400
DM = 20*cands[:,2]/40
SNR = cands[:,3]
cls_obj = DBSCAN(eps=1.1, min_samples=1)
print(1)

#based on SNR and time
#to check the scaling
#plt.plot(cands[:,0], cands[:,3], '.')
#plt.show()

clusters = cls_obj.fit(np.column_stack([time, SNR/np.max(SNR)])).labels_
print(2)
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
final_cands = []
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    final_cand = cand[np.where(cand[:,3]==np.max(cand[:,3]))][0]
    final_cands.append(final_cand)
    plt.plot(cand[:,0], cand[:,3], '.')
    #ax.scatter(final_cand[0], final_cand[1], final_cand[2], '.')
plt.show()
sys.exit(0)
final_cands = np.array(final_cands)
print(max(clusters))
print(len(final_cands))
#np.savetxt('/Users/mehulagarwal/Downloads/time_snr.txt', final_cands, fmt='%s')

	
'''	
	#based on DM and time
	#to check the scaling
	#plt.plot(cands[:,0], cands[:,2], '.')
	#plt.show()
	clusters = cls_obj.fit(np.column_stack([time, DM])).labels_
	uniq_clusters = np.unique(clusters)
	nclusters = len(uniq_clusters)
	fig = plt.figure()
	#ax = fig.add_subplot(111, projection='3d')
	final_cands = []
	for icluster in uniq_clusters:
	    cand = cands[icluster == clusters]
	    final_cand = cand[np.where(cand[:,3]==np.max(cand[:,3]))][0]
	    final_cands.append(final_cand)
	    y = cand[:,2]+(np.random.random(len(cand[:,2]))-0.5)*20
	    plt.plot(cand[:,0], y, '.', alpha=0.1)    
	    #ax.scatter(cand[:,0]/20, 20*cand[:,1]/400, 20*cand[:,2]/40, '.')
plt.show()
sys.exit(0)
final_cands = np.array(final_cands)
print(max(clusters))
#np.savetxt('/Users/mehulagarwal/Downloads/322.txt', final_cands, fmt='%s')
'''

'''
#based on Boxcar and time
#to check the scaling
#plt.plot(cands[:,0], cands[:,1], '.')
#plt.show()
clusters = cls_obj.fit(np.column_stack([time, boxcar])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
final_cands = []
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    final_cand = cand[np.where(cand[:,3]==np.max(cand[:,3]))][0]
    final_cands.append(final_cand)
    #plt.plot(cand[:,0], cand[:,1], '.')    
    ax.scatter(cand[:,0]/20, 20*cand[:,1]/400, 20*cand[:,2]/40, '.')
plt.show()
final_cands = np.array(final_cands)
print(max(clusters))
np.savetxt('/Users/mehulagarwal/Downloads/time_boxcar.txt', final_cands, fmt='%s')
'''

'''
#based on 3d
clusters = cls_obj.fit(np.column_stack([time, boxcar, DM])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
final_cands = []
final_cands.append(header)
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    final_cand = cand[np.where(cand[:,3]==np.max(cand[:,3]))][0]
    final_cands.append(final_cand)
    ax.scatter(cand[:,0]/20, 20*cand[:,1]/400, 20*cand[:,2]/40, '.')
plt.show()
final_cands = np.array(final_cands)
print(max(clusters))
np.savetxt('/Users/mehulagarwal/Downloads/final3d.txt', final_cands, fmt='%s')
'''

