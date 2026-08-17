#!/bin/bash

# This script takes a list of files that are taken as corpora and for
# each of these, it cleans them up and then computes the overlap of
# these corpora by reducing the amount of data available.

stopword_dir="stopwords"
corpus_dir="corpus"
intermediate_dir="intermediate"
# This is the default output directory. Perhaps this will need to be
# moved to a specific commandline argument.
output_dir="out"

# Create directories if they does not yet exist.

echo "ENGLISH BROWN"
stopword="eng_stopwords.txt"
corpus="brown"

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


echo "AFRIKAANS WIKI"
stopword="afr_stopwords.txt"
corpus="afr_wiki"

echo "Cleanup corpus"
mkdir -p ${intermediate_dir}/${corpus}/original
./prepare_corpus.py \
    -i ${corpus_dir}/${corpus} \
    -o ${intermediate_dir}/${corpus}/original

mkdir -p ${intermediate_dir}/${corpus}/split500
./prepare_corpus.py \
    -i ${corpus_dir}/${corpus} \
    -o ${intermediate_dir}/${corpus}/split500 \
    -p 500

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


echo "AFRIKAANS WIKI gbvh"
stopword="afr_gbvh_stopwords.txt"
corpus="afr_wiki"

echo "Extract features"
mkdir -p ${output_dir}/${corpus}
./extract_features.py \
  -t ${intermediate_dir}/${corpus}/original \
  -s ${stopword_dir}/${stopword} \
  -o ${output_dir}/${corpus}/original_gbvh.csv

./extract_features.py \
  -t ${intermediate_dir}/${corpus}/split500 \
  -s ${stopword_dir}/${stopword} \
  -o ${output_dir}/${corpus}/split500_gbvh.csv


echo "SESOTHO WIKI"
stopword="sot_stopwords.txt"
corpus="sot_wiki"

echo "Cleanup corpus"
mkdir -p ${intermediate_dir}/${corpus}/original
./prepare_corpus.py \
    -i ${corpus_dir}/${corpus} \
    -o ${intermediate_dir}/${corpus}/original

mkdir -p ${intermediate_dir}/${corpus}/split500
./prepare_corpus.py \
    -i ${corpus_dir}/${corpus} \
    -o ${intermediate_dir}/${corpus}/split500 \
    -p 500

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



echo "ISIZULU WIKI"
stopword="zul_stopwords.txt"
corpus="zul_wiki"

echo "Cleanup corpus"
mkdir -p ${intermediate_dir}/${corpus}/original
./prepare_corpus.py \
    -i ${corpus_dir}/${corpus} \
    -o ${intermediate_dir}/${corpus}/original

mkdir -p ${intermediate_dir}/${corpus}/split500
./prepare_corpus.py \
    -i ${corpus_dir}/${corpus} \
    -o ${intermediate_dir}/${corpus}/split500 \
    -p 500

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
