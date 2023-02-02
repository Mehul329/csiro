#!/bin/bash

#define the tape device path
tape_device="/dev/tape/nst5"

#move to the beginning of the tape
mt -f $tape_device rewind

#initialize counter
counter=0

#loop through the files on the tape
while true; do
	#read the next file
	dd if=$tape_device bs=64k | tar -b 128 -xv
	#increment counter
	counter=$((counter+1))
	#check if counter has reached 330
	if [ $counter -eq 330 ]; then
		break
	fi
done
echo "All files have been read and extracted"

