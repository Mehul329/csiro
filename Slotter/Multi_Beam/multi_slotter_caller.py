#this program assumes that the path of the input is in the format:
#/scratch2/aga017/utmost_data/{tape_no}
#the input is actually the tape itslef because then it goes into the directory of tape
#extracts the observation number, stores it and passes it onto slotter to slaughter 
#useless candidates from that particulat observation

#this program also assumes that this code will be running on 33 different computers that 
#will be taking 10 observations from each tape (last set of obs will only take 4-7 based on
#number of obs in tape). 

#%% Importing modules

import os
import argparse
import numpy as np

#%% Input definition

a = argparse.ArgumentParser()
a.add_argument('-n', type = int, help = 'Type the node number (1-33)')
a.add_argument('-t', type = str, help = 'Type the tape number like SM0006L6')
args = a.parse_args()
node = args.n
tape_no = args.t
code = '/home/aga017/codes/csiro/Slotter/Multi_Beam/multi_beam_slotter.py'

#%%code caller

basedir = f"/scratch2/aga017/utmost_data/{tape_no}"
observations = np.array(os.listdir(basedir))
obs_blocks = (np.linspace(0,9,10)+(node-1)*10).astype(int)
if node == 33:
    if len(observations) - 1 < obs_blocks[-1]:
        rem = obs_blocks[-1] % (len(observations) - 1)
        obs_blocks = obs_blocks[:-rem]
        observations = observations[obs_blocks]
    else:
        observations = observations[obs_blocks]
else:
    observations = observations[obs_blocks]

for observation in observations:
    cmd = f"python3 {code} -t {tape_no} -o {observation}"
    print(cmd)    
    os.system(cmd)
