import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np

#%%
filename = '/u/aga017/Desktop/SM0005L6_2018-02-23-17:56:51_BEAM_004.txt'
cands = np.loadtxt(filename, dtype='str')
cands = cands[1:,:].astype(float)

time = cands[:,0]/20
boxcar = 20*cands[:,1]/400
DM = 20*cands[:,2]/40
SNR = cands[:,3]
cls_obj = DBSCAN(eps=1.1, min_samples=1)

#based on SNR and time
#to check the scaling
#plt.plot(cands[:,0], cands[:,3], '.')
#plt.show()

clusters = cls_obj.fit(np.column_stack([time, SNR/max(SNR)])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    idx = np.where(cand[:3]==np.max(cand[:3]))
    print(idx)#, cand[idx])
    #plt.plot(cand[:,0]/20, cand[:,3], '.')
    ax.scatter(cand[:,0]/20, 20*cand[:,1]/400, 20*cand[:,2]/40, '.')
plt.show()
print(max(clusters))


'''
#based on DM and time
#to check the scaling
#plt.plot(cands[:,0], cands[:,2], '.')
#plt.show()

clusters = cls_obj.fit(np.column_stack([time, DM])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    plt.plot(cand[:,0]/20, 20*cand[:,2]/40, '.')
plt.show()
print(max(clusters))
'''
'''
#based on Boxcar and time
#to check the scaling
#plt.plot(cands[:,0], cands[:,1], '.')
#plt.show()

clusters = cls_obj.fit(np.column_stack([time, boxcar])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    plt.plot(cand[:,0]/20, 20*cand[:,1]/400, '.')
plt.show()
print(max(clusters))
'''

'''
#based on 3d
clusters = cls_obj.fit(np.column_stack([time, boxcar, DM])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    ax.scatter(cand[:,0]/20, 20*cand[:,1]/400, 20*cand[:,2]/40, '.')
plt.show()
print(max(clusters))
'''

#%%
#this function will group the neighbouring points (used on first_seen_time)
'''
def groupBlocks(samp_list, bin_list):
    res = [[0]]

    for i in range(1, len(samp_list)):
        if samp_list[i] in range(int(samp_list[i-1]),int(samp_list[i-1]+bin_list[i-1])):
            res[-1].append(i)
        else:
            res.append([i])
    return res

a = groupBlocks(Times, Bins)

#this loop will extract the point that has the maximum S/R among the neighbouring points
for i in range(len(a)):
    if len(a[i]) == 1:
        a[i] = a[i][0]
    else:
        max_value = 0
        max_ind = 0
        for j in range(len(a[i])):
            if SNRs[a[i][j]] > max_value:
                max_value = SNRs[a[i][j]]
                max_ind = j
        a[i] = a[i][max_ind]

Times = list(np.array(Times)[a])
SNRs = list(np.array(Times)[a])
Bins = list(np.array(Times)[a])
DMs = list(np.array(Times)[a])
cands = cands[a]
cands = cands[cands[:,3].argsort()] #sorting it with respect to DMs
#%%
#this function will group the neighbouring duplicates (used on DMs)
def groupDuplicates(lst):
    res = [[0]]

    for i in range(1, len(lst)):
        if lst[i-1] == lst[i]:
            res[-1].append(i)

        else:
            res.append([i])
    return res

a = groupDuplicates(DM)

#this loop will sort the in_times in each DMs
for i in range(len(a)):
    if len(a[i]) > 1:
        start = a[i][0]
        end = a[i][-1]
        temp = cands[start:end+1, :]
        temp = temp[temp[:,0].argsort()]
        cands[start:end+1,:] = temp

#%%
name = np.array(['Initial Time', 'S/R', 'Bins', 'DM'])
cands = np.row_stack((name, cands))
np.save(filename, cands)
'''
