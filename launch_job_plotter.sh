#!/bin/bash

. /home/aga017/.bashrc
conda activate csiro

node=$1
tape=$2

echo "which python returns `which python`"

echo "Executing: python runner.py -n $node -t $tape"
python /home/aga017/codes/csiro/runner_plotter.py -n $node -t $tape

echo "Done"
