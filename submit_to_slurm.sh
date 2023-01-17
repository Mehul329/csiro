#!/bin/bash
#
#SBATCH --job-name=find_ulps_in_smirf
#SBATCH --ntasks=1
#SBATCH --time=02:20:00
#SBATCH --mem-per-cpu=1GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aga017
#SBATCH --array=1-32

myprogram=$1
name_of_tape=$2

list_of_obs=`ls -1d 2018*/`

for obs in $list_of_obs
do
	filt1=$obs/FB/BEAM_001/$obs.fil
	filt2=$obs/FB/BEAM_002/$obs.fil

obs_beams=`ls 2018*/FB/BEAM_*/2018*.fil`
pointings=`ls -1d $name_of_tape`

srun echo "All pointings include $pointings"
srun echo ""
srun echo ""
srun echo "This node will deal with ${pointings[$SLURM_ARRAY_TASK_ID]}"

srun /home/aga017/codes/csiro/launch_job.sh $myprogram ${pointings[$SLURM_ARRAY_TASK_ID]}
