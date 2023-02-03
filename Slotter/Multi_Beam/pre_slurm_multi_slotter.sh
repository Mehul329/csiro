#!/bin/bash

#this code will run in this sequence pre_slurm_multi_slotter (this code) -> multi_slotter_caller -> multi_beam_slotter
. /home/aga017/.bashrc
conda activate csiro

node=$1
tape=$2

echo "which python returns `which python`"

echo "Executing: python runner.py -n $node -t $tape"
python /home/aga017/codes/csiro/Slotter/Multi_Beam/multi_slotter_caller.py -n $node -t $tape

echo "Done"

