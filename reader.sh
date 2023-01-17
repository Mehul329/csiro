#!/bin/bash

# define the tape device path
tape_device="/dev/tape/nst5"

#move to the beginning of the tape
mt -f $tape_device rewind

#loop through the files on the tape
while true; do
	#read the next file
	dd if=$tape_device bs=64k | tar -b 128 -xv

	if [ $? -ne 0 ]; then
		echo "An error occured"
		break
	fi

done
echo "All files have been read and extracted"

echo "Now starting the copy to petrichor"

dirname=`pwd | awk -F/ '{print $NF}'`
cd ..
echo "Executing rsync -av --progress $dirname petrichor.hpc.csiro.au:/scratch1/aga017/utmost_data/"
rsync -av --progress $dirname petrichor.hpc.csiro.au:/scratch1/aga017/utmost_data/

echo "All done"
