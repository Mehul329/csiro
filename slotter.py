import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np
#%%
filename = '/Users/mehulagarwal/Downloads/1.txt'
cands = np.loadtxt(filename, dtype='str')
cands = cands[1:,:].astype(float)
cls_obj = DBSCAN(eps=1000, min_samples=1)
clusters = cls_obj.fit(cands[:,:3]).labels_
#cands = np.column_stack([cands, clusters])

'''
fig = plt.figure()
ax = plt.axes(projection='3d')
for cand in cands:
    ax.scatter(cand[0], cand[1], cand[2])
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
