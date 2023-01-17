import os, sys
import argparse
import numpy as np
#%% Input
'''
a = argparse.ArgumentParser()
<<<<<<< HEAD
a.add_argument('-f', type = str, help = 'Type the observation name')
args = a.parse_args()
pointing = args.f+'/'
'''

basedir = '/Users/mehulagarwal/Desktop/Tape1/'
observations = os.listdir(basedir)
observations = observations[1:]
obs_dir = np.core.defchararray.add(basedir, observations)
func = np.vectorize(lambda x:x+x.split('/')[5])
for i in range(1):
    beam_blocks = (np.linspace(1,11,11)+i*11).astype(int)
    beam_blocks = np.core.defchararray.zfill(beam_blocks.astype(str), 3)
    beam_blocks = np.core.defchararray.add('/FB/beam_', beam_blocks)
    beam_blocks = np.core.defchararray.add(beam_blocks, '/')
    beam_dir = np.core.defchararray.add(np.repeat(obs_dir, beam_blocks.shape[0]), np.tile(beam_blocks, obs_dir.shape[0]))
    filter_bank_path = np.core.defchararray.add(func(beam_dir), '.fil')
    print(filter_bank_path)
=======
a.add_argument('-f', type = str, help = 'Type the pointing name')
a.add_argument('-c', type = str, help = 'Type the path to the code that you want to execute')
args = a.parse_args()
pointing = args.f+'/'

#%%
observations = os.listdir(pointing)
#counter = 0
'''
#this is happening because there is . directory
final_observations = []
for observation in temp_observations:
    if observation[0] != '.':
        final_observations.append(observation+'/')
'''        
for observation in observations:
    beams = os.listdir(pointing+observation + "/FB/")
    for beam in beams:
#        counter += 1 
#        if counter > 2:
#            sys.exit(0)
        cmd = f"python3 {args.c} -f "+pointing+observation+"/FB/" +beam +"/"+ observation + ".fil"
        print(f"Now executing the following command : {cmd}")
        os.system(cmd)
>>>>>>> 8dc0b30f16c1cdc85fc4d2b9e473ed0da1951b17
