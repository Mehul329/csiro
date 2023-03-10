#!/bin/bash
#
#SBATCH --job-name=find_ulps_in_smirf
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=10GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aga017@csiro.au
#SBATCH --array=6

tape=$1

srun /home/aga017/codes/csiro/launch_job_plotter.sh $SLURM_ARRAY_TASK_ID $tape
