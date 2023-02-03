#!/bin/bash

#this code will run in this sequence 
#slurm_multi_slotter (this code) -> 33 * (pre_slurm_multi_slotter -> multi_slotter_caller -> multi_beam_slotter)

#SBATCH --job-name=find_ulps_in_smirf
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=10GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aga017@csiro.au
#SBATCH --array=1-33

tape=$1

srun /home/aga017/codes/csiro/Slotter/Multi_Beam/pre_slurm_multi_slotter.sh $SLURM_ARRAY_TASK_ID $tape
