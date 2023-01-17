import os
import argparse
import numpy as np
#%% Input

#a = argparse.ArgumentParser()
#a.add_argument('-n', type = int, help = 'Type the node number (1-32)')
#a.add_argument('-c', type = str, help = 'Type path of finder code')
#args = a.parse_args()
#node = args.n
#code = args.c
code = 'finder.py'
node = 1

basedir = '/Users/mehulagarwal/Desktop/Tape1/'
observations = os.listdir(basedir)
observations = observations[1:]
obs_dir = np.core.defchararray.add(basedir, observations)
func = np.vectorize(lambda x:x+x.split('/')[5])

beam_blocks = (np.linspace(1,11,11)+(node-1)*11).astype(int)
beam_blocks = np.core.defchararray.zfill(beam_blocks.astype(str), 3)
beam_blocks = np.core.defchararray.add('/FB/beam_', beam_blocks)
beam_blocks = np.core.defchararray.add(beam_blocks, '/')
beam_dir = np.core.defchararray.add(np.repeat(obs_dir, beam_blocks.shape[0]), np.tile(beam_blocks, obs_dir.shape[0]))
filter_bank_path = np.core.defchararray.add(func(beam_dir), '.fil')
for filter_bank in filter_bank_path:
    if os.path.exists("filter_bank"):
        cmd = f"python3 {code} -f "+filter_bank
        os.system(cmd)
        print(f"Done : {np.array(cmd.split('/'))[np.array([-5,-4,-2])]}")
    else:
        print(f"{filter_bank} does not exist")

