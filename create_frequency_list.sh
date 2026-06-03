#!/bin/bash

# This script requires a corpus file as input. The corpus file should
# be tokenized and cleaned up (if required) with one token per line.
# The script then generates a frequency list and stores it with the
# same filename in the output directory.

corpus=$1
output_dir=$2

# Create the output directory if it does not exist.
mkdir -p ${output_dir}

# Generate the frequency list based on the corpus.

cat ${corpus}
        | sort \
        | uniq -c \
        | sort -n -r \
        > ${output_dir}/${corpus}
