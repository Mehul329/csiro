#!/bin/bash

. /home/aga017/.bashrc
conda activate csiro

echo "which python returns `which python`"

echo "Executing: python slotter_2.py"
python /home/aga017/codes/csiro/slotter_2.py

echo "Done"
