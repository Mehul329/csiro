#!/bin/bash

# Set the starting value and ending value
start=1
end=352

# Set the block size
block_size=11

# Initialize the counter
counter=$start

# Loop through the range of numbers
while [ $counter -le $end ]
do
    # Print the numbers in the current block
    for (( i=counter; i<counter+block_size; i++ ))
    do
        if [ $i -le $end ]
        then
            echo -n "$i "
        fi
    done
    echo "" # Print a newline

    # Update the counter
    counter=$((counter+block_size))
done

