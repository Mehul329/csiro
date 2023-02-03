#!/bin/bash

#this code will run in this sequence pre_slurm_single_slotter (this code) -> single_slotter_caller -> single_beam_slotter
. /home/aga017/.bashrc
conda activate csiro

node=$1
tape=$2

echo "which python returns `which python`"

echo "Executing: python runner.py -n $node -t $tape"
python /home/aga017/codes/csiro/Slotter/Single_Beam/single_slotter_caller.py -n $node -t $tape

echo "Done"
