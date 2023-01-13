import os, sys
import argparse

#%% Input
a = argparse.ArgumentParser()
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
