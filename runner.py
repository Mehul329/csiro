import os
import argparse
import time
import numpy as np
#%% Input

a = argparse.ArgumentParser()
a.add_argument('-n', type = int, help = 'Type the node number (1-44)')
a.add_argument('-t', type = str, help = 'Type the full path of tape directory with / at the end')
args = a.parse_args()
node = args.n
tape = args.t
code = '/home/aga017/codes/csiro/finder.py'

basedir = tape
observations = os.listdir(basedir)
observations = observations[1:]
obs_dir = np.core.defchararray.add(basedir, observations)
func = np.vectorize(lambda x:x+x.split('/')[-4])

beam_blocks = (np.linspace(1,8,8)+(node-1)*8).astype(int)
beam_blocks = np.core.defchararray.zfill(beam_blocks.astype(str), 3)
beam_blocks = np.core.defchararray.add('/FB/BEAM_', beam_blocks)
beam_blocks = np.core.defchararray.add(beam_blocks, '/')
beam_dir = np.core.defchararray.add(np.repeat(obs_dir, beam_blocks.shape[0]), np.tile(beam_blocks, obs_dir.shape[0]))
filter_bank_path = np.core.defchararray.add(func(beam_dir), '.fil')
for filter_bank in filter_bank_path:
    if 'BEAM_001' in filter_bank:
        print(f'Skipping {filter_bank}')
        continue
    if os.path.exists(filter_bank):
        start = time.time()
        cmd = f"python3 {code} -f "+filter_bank
        os.system(cmd)
        end = time.time()
        print(end-start, cmd)
	#print(f"Done : {np.array(cmd.split('/'))[np.array([-5,-4,-2])]}")
    else:
        print(f"{filter_bank} does not exist")

