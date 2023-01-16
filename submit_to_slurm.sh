#!/bin/bash
#
#SBATCH --job-name=find_ulps_in_smirf
#SBATCH --ntasks=1
#SBATCH --time=00:20:00
#SBATCH --mem-per-cpu=1GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aga017
#SBATCH --array=1-2

myprogram=$1
name_of_tape=$2

pointings=`ls -1d $name_of_tape`

srun echo "All pointings include $pointings"
srun echo ""
srun echo ""
srun echo "This node will deal with ${pointings[$SLURM_ARRAY_TASK_ID]}"

srun /home/aga017/codes/csiro/launch_job.sh $myprogram ${pointings[$SLURM_ARRAY_TASK_ID]}
