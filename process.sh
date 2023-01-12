#!/bin/bash

basepath="/DATA/CETUS_4/gup037/SMIRF_EXAMPLE_TAPE_DATA_VIVEK/SMIRF_0810-2938/2018-06-01-05:33:09/FB/"
all_beams=`ls ${basepath}`
count=0
for ibeam in ${all_beams}
do
    let count=count+1
    if [ $count -lt 10 ]
    then
    	echo $count
    	python ~/codes/csiro/finder.py -f ${basepath}/${ibeam}/2018-06-01-05:33:09.fil &
    fi
done
