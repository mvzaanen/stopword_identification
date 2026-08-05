#!/bin/bash

# This script takes a list of files that are taken as corpora and for
# each of these, it cleans them up and then computes the overlap of
# these corpora by reducing the amount of data available.

stopword_dir="stopwords"
stopword="english_stopwords.txt"

corpus_dir="corpus"
corpus="brown"
corpus_base=`basename ${corpus}`

intermediate_dir="intermediate"
# This is the default output directory. Perhaps this will need to be
# moved to a specific commandline argument.
output_dir="out"

# Create directories if they does not yet exist.

echo "Cleanup corpus"
mkdir -p ${intermediate_dir}/${corpus}/original
./prepare_corpus.py \
    -i ${corpus_dir}/${corpus} \
    -o ${intermediate_dir}/${corpus}/original \
    -b # is brown corpus

mkdir -p ${intermediate_dir}/${corpus}/split500
./prepare_corpus.py \
    -i ${corpus_dir}/${corpus} \
    -o ${intermediate_dir}/${corpus}/split500 \
    -p 500 \
    -b # is brown corpus

echo "Extract features"
mkdir -p ${output_dir}/${corpus}
./extract_features.py \
  -t ${intermediate_dir}/${corpus}/original \
  -s ${stopword_dir}/${stopword} \
  -o ${output_dir}/${corpus}/original.csv

./extract_features.py \
  -t ${intermediate_dir}/${corpus}/split500 \
  -s ${stopword_dir}/${stopword} \
  -o ${output_dir}/${corpus}/split500.csv
