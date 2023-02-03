#!/bin/bash

#this code will run in this sequence 
#slurm_single_slotter (this code) -> 33 * (pre_slurm_single_slotter -> single_slotter_caller -> single_beam_slotter)

#SBATCH --job-name=find_ulps_in_smirf
#SBATCH --ntasks=1
#SBATCH --time=02:00:00
#SBATCH --mem-per-cpu=10GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aga017@csiro.au
#SBATCH --array=1-33

tape=$1

srun /home/aga017/codes/csiro/Slotter/Single_Beam/pre_slurm_single_slotter.sh $SLURM_ARRAY_TASK_ID $tape
