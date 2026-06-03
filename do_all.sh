#!/bin/bash

# This script takes a list of files that are taken as corpora and for
# each of these, it cleans them up and then computes the overlap of
# these corpora by reducing the amount of data available.

stopword_dir="stopwords"
stopword="english_stopwords.txt"

corpus_dir="corpus"
corpus="brown.txt"
corpus_base=`basename ${corpus}`

# This is the default output directory. Perhaps this will need to be
# moved to a specific commandline argument.
output_dir="out"

# Create the output directory if it does not yet exist.
mkdir -p ${output_dir}

echo "Cleanup corpus"
./clean_up_corpus.sh \
    ${corpus_dir}/${corpus} \
    ${output_dir}/${corpus_base}.clean

echo "Create frequency list"
./create_frequency_list.sh \
    ${output_dir}/${corpus_base}.clean \
    ${output_dir}/${corpus_base}.freq

echo "Extract features"
./extract_features.py \
  -f ${output_dir}/${corpus_base}.freq \
  -s ${stopword_dir}/${stopword} \
  -o ${output_dir}/${corpus_base}.csv
