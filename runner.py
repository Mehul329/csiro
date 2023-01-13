import os
import argparse

#%% Input
a = argparse.ArgumentParser()
a.add_argument('-f', type = str, help = 'Type the pointing name')
args = a.parse_args()
pointing = args.f+'/'

#%%
observations = os.listdir(pointing)
'''
#this is happening because there is . directory
final_observations = []
for observation in temp_observations:
    if observation[0] != '.':
        final_observations.append(observation+'/')
'''        
for observation in observations:
    beams = os.listdir(pointing+observation)
    for beam in beams:
        file = 'python3 code.py -f '+pointing+observation+beam
        os.system(file)
