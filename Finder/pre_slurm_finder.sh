#!/bin/bash

#this code will run in this sequence pre_slurm_finder (this code) -> finder_caller -> finder
. /home/aga017/.bashrc
conda activate csiro

node=$1
tape=$2

echo "which python returns `which python`"

echo "Executing: python runner.py -n $node -t $tape"
python /home/aga017/codes/csiro/Finder/finder_caller.py -n $node -t $tape

echo "Done"
