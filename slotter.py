import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np

#%%
filename = '/Users/mehulagarwal/Downloads/1.txt'
cands = np.loadtxt(filename, dtype='str')
cands = cands[1:,:].astype(float)

time = cands[:,0]/20
boxcar = 20*cands[:,1]/400
DM = 20*cands[:,2]/40
SNR = cands[:,3]
'''
#based on SNR and time
#to check the scaling
#plt.plot(cands[:,0], cands[:,3], '.')
#plt.show()

cls_obj = DBSCAN(eps=1.1, min_samples=1)
clusters = cls_obj.fit(np.column_stack([time, SNR/max(SNR)])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    plt.plot(cand[:,0]/20, cand[:,3], '.')
plt.show()
print(max(clusters))
'''

'''
#based on DM and time
#to check the scaling
#plt.plot(cands[:,0], cands[:,2], '.')
#plt.show()

cls_obj = DBSCAN(eps=1.1, min_samples=1)
clusters = cls_obj.fit(np.column_stack([time, DM])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    plt.plot(cand[:,0]/20, 20*cand[:,2]/40, '.')
plt.show()
print(max(clusters))
'''

#based on Boxcar and time
#to check the scaling
plt.plot(cands[:,0], cands[:,1], '.')
plt.show()
'''
cls_obj = DBSCAN(eps=1.1, min_samples=1)
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
#plt.scatter(time, SNR, c=clusters, cmap='rainbow')
#plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
cls_obj = DBSCAN(eps=1, min_samples=1)
clusters = cls_obj.fit(np.column_stack([time, DM, boxcar])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)
for icluster in uniq_clusters:
    cand = cands[icluster == clusters]
    plt.plot(cand[:,0]/20, 20*cand[:,2]/40, '.')
    #plt.plot(cands_in_this_cluster[:,0]/20, cands_in_this_cluster[:,2]/2,'.')
plt.show()
'''
'''
cls_obj = DBSCAN(eps=20, min_samples=1)
clusters = cls_obj.fit(np.column_stack([time, DM])).labels_
uniq_clusters = np.unique(clusters)
nclusters = len(uniq_clusters)

for icluster in uniq_clusters:
    cands_in_this_cluster = cands[icluster == clusters]
    plt.plot(cands_in_this_cluster[:,0]/20, cands_in_this_cluster[:,2]/2,'.')
plt.show()
'''
'''
plt.plot(cands[:,1], np.zeros_like(cands[:,0]),'.')
plt.show()
plt.plot(cands[:,1], cands[:,2],'.')
plt.show()
plt.plot(cands[:,2], np.zeros_like(cands[:,0]),'.')
plt.show()
plt.plot(cands[:,2], cands[:,0],'.')
plt.show()
#plt.plot(cands[:,0], cands[:,1], '.')
#plt.show()
'''
'''
dx = np.random.randint(1,100,30)
dy = np.random.randint(1,100,30)
dz = np.random.randint(1,100,30)
R = 1.25 * dx
for i in range(len(dy)):
    sy = dx[i]/dy[i]
    sz = dx[i]/dz[i]
    x = np.transpose(cands[:,0]/dx[i])
    y = np.transpose(cands[:,1]/sy)
    z = np.transpose(cands[:,2]/sz)
    cls_obj = DBSCAN(eps=R[i], min_samples=1)
    clusters = cls_obj.fit(np.column_stack([x,y,z])).labels_
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, '.', c=clusters, cmap='rainbow')
    plt.show()
    print(dx[i], dy[i], dz[i], R[i])
    print(max(clusters))
'''
#%%
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, '.' )#c=clusters)
#ax.set_xlim([12800,13000])
#ax.set_ylim([110450,110500])
#ax.set_zlim([1000,1100])
plt.show()

fig = plt.figure()
ax = plt.axes(projection='3d')
print(5)
for i in range(len(clusters)):
    ax.scatter(cand[0], cand[1], cand[2], colors[i])
print(6)
plt.show()
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
