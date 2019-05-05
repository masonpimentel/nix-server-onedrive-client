#!/bin/bash

num_from_dir=$(shuf -i 1-5 -n 1)
num_to_dir=$(shuf -i 1-5 -n 1)


mkdir .tmp_test

echo Making $num_from_dir directories

i=0
while [[ $i -lt $num_from_dir ]]; do
    mkdir .tmp_test/test_dir_$i

    num_files=$(shuf -i 0-10 -n 1)
    j=0
    while [[ $j -lt $num_files ]]; do
        echo Making file_$j in test_dir_$i        
        head -c 100 /dev/urandom > .tmp_test/test_dir_$i/file_$j
        
        ((j++))
    done

    ((i++))
done

#rm -rf .tmp_test

# 0 -> 1000 files


# 1 -> 5 from, to mappings


# 0 -> 10 737 418 B file sizes
