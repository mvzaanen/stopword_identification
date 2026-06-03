#!/bin/bash

# This script requires a corpus file as input. The corpus file should
# be tokenized and cleaned up (if required) with one token per line.
# The script then generates a frequency list and stores it with the
# name of the second argument.

corpus_in=$1
corpus_out=$2

# Generate the frequency list based on the corpus.

cat ${corpus_in} \
        | sort \
        | uniq -c \
        | sort -n -r \
        > ${corpus_out}
