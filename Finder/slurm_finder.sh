#!/bin/bash
# this code will run in this sequence slurm_finder (this code) -> 44 * (pre_slurm_finder -> finder_caller -> finder)
#SBATCH --job-name=find_ulps_in_smirf
#SBATCH --ntasks=1
#SBATCH --time=08:00:00
#SBATCH --mem-per-cpu=10GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aga017@csiro.au
#SBATCH --array=1-44

tape=$1

srun /home/aga017/codes/csiro/Finder/pre_slurm_finder.sh $SLURM_ARRAY_TASK_ID $tape
