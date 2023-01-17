import os

basedir = "/DATA/DOLBY_1/SCRATCH/zombie_pulsars/SM0004L6/"
list_of_obs = os.listdir(basedir)
myblocks = []
for iblock in range(32):
    block_list = []
    for ibeam in range(352):
        beam_list = [obs + "/FB/BEAM_" + str(ibeam).zfill(3) + "/" + obs + ".fil" for obs in list_of_obs]
        if ibeam % 11 !=0 or ibeam == 0:
            block_list.extend(beam_list)
    myblocks.append(block_list)

