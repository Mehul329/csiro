import os
import argparse
import numpy as np
#%% Input

a = argparse.ArgumentParser()
a.add_argument('-n', type = int, help = 'Type the node number (1-33)')
a.add_argument('-t', type = str, help = 'Type the full path of tape directory with / at the end')
args = a.parse_args()
node = args.n
tape = args.t
code = '/home/aga017/codes/csiro/plotter.py'

basedir = tape
tape_no = tape.split('/')[-2]
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
    if observation == '2018-03-01-14:17:51':
        cmd = f"python3 {code} -t {tape_no} -o {observation}"
        print(cmd)    
        os.system(cmd)

