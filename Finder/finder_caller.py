#this program assumes that the path of the input is in the format:
#/scratch2/aga017/utmost_data/tape_no/obs_no/FB/beam_no/filterbank.fil

#this program also assumes that this code will be running on 44 different computers that 
#will be taking 8 beams from each observation (min 324, max 329). 

#%%
import os
import argparse
import time
import numpy as np
#%% Input

a = argparse.ArgumentParser()
a.add_argument('-n', type = int, help = 'Type the node number (1-44)')
a.add_argument('-t', type = str, help = 'Type the name of the tape like SM0006L6')
args = a.parse_args()
node = args.n
tape = args.t
code = '/home/aga017/codes/csiro/Finder/finder.py'

basedir = '/scratch2/aga017/utmost_data'+tape
observations = os.listdir(basedir) #list of observations
obs_dir = np.core.defchararray.add(basedir, observations) #list of full path to observations
func = np.vectorize(lambda x:x+x.split('/')[-4])

beam_blocks = (np.linspace(1,8,8)+(node-1)*8).astype(int) #depending on the node, whihc number of 8 beams to consider
beam_blocks = np.core.defchararray.zfill(beam_blocks.astype(str), 3) #making beam numbers in the format of 004
beam_blocks = np.core.defchararray.add('/FB/BEAM_', beam_blocks) #creating a full path to beam blocks
beam_blocks = np.core.defchararray.add(beam_blocks, '/')
beam_dir = np.core.defchararray.add(np.repeat(obs_dir, beam_blocks.shape[0]), np.tile(beam_blocks, obs_dir.shape[0]))
filter_bank_path = np.core.defchararray.add(func(beam_dir), '.fil')
for filter_bank in filter_bank_path:
    if 'BEAM_001' in filter_bank:
        print(f'Skipping {filter_bank}') #removing beam 1 because it has too many problems
        continue #exiting the for loop
    if os.path.exists(filter_bank): #checking if the path exists
        start = time.time()
        cmd = f"python3 {code} -f "+filter_bank
        os.system(cmd)
        end = time.time()
        print(end-start, cmd) #time is to check how much each filter bank is taking to give out candidates
    else:
        print(f"{filter_bank} does not exist")

