#!/bin/bash

. /home/aga017/.bashrc
conda activate csiro

myprogram=$1
mypointing=$2

echo "which python returns `which python`"

echo "Executing: python $myprogram -f $mypointing"

python $myprogram -f $mypointing

echo "Done"
