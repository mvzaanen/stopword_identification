#!/usr/bin/env python3

import argparse
import csv
from collections import Counter
from pathlib import Path
import logging
import math

def compute_frequency_list(texts):
    # flatten list of texts
    full_text = [item for sublist in texts for item in sublist]
    frequency = Counter(full_text)
    return frequency


def initialize_features(frequency, features):
    for word in frequency.keys():
        features["words"][word] = {}
    return features


def compute_stopword_feature(stopwords, features):
    for word in features["words"].keys():
        features["words"][word]["stopword"] = word in stopwords
    return features


def compute_local_word_features(text, frequency, features):
    for word, count in frequency.most_common():
        features["words"][word]["word"] = word
        features["words"][word]["length"] = len(word)
        features["words"][word]["tf_n"] = count
        features["words"][word]["tf_l"] = 1 + math.log(count)
        features["words"][word]["rank"] = features["rank"]
        features["total"] += count
        features["rank"] += 1
    # features that can only be computed when total is known
    for word in frequency.keys():
        features["words"][word]["ntf_n"] = features["words"][word]["tf_n"]/features["total"]
        features["words"][word]["ntf_l"] = 1 + math.log(features["words"][word]["ntf_n"])
    return features


def compute_global_word_features(texts, features):
    N = len(texts)
    text_sets = []
    for text in texts:
        text_sets.append(set(text))
    for word in features["words"].keys():
        document_count = 0
        for text_set in text_sets:
            if word in text_set:
                document_count += 1
        features["words"][word]["df"] = document_count/N
        features["words"][word]["log_df"] = math.log(features["words"][word]["df"]) if features["words"][word]["df"] > 0 else float('-inf')
        features["words"][word]["idf"] = N/document_count if document_count > 0 else 0
        features["words"][word]["log_idf"] = math.log(features["words"][word]["idf"]) if features["words"][word]["idf"] > 0 else float('-inf')
    return features


def compute_combined_features(texts, features):
    for word in features["words"].keys():
        features["words"][word]["tf_n*df"] = features["words"][word]["tf_n"] * features["words"][word]["df"] 
        features["words"][word]["tf_n*log_df"] = features["words"][word]["tf_n"] * features["words"][word]["log_df"] 
        features["words"][word]["tf_n*idf"] = features["words"][word]["tf_n"] * features["words"][word]["idf"] 
        features["words"][word]["tf_n*log_idf"] = features["words"][word]["tf_n"] * features["words"][word]["log_idf"] 
        features["words"][word]["tf_l*df"] = features["words"][word]["tf_l"] * features["words"][word]["df"] 
        features["words"][word]["tf_l*log_df"] = features["words"][word]["tf_l"] * features["words"][word]["log_df"] 
        features["words"][word]["tf_l*idf"] = features["words"][word]["tf_l"] * features["words"][word]["idf"] 
        features["words"][word]["tf_l*log_idf"] = features["words"][word]["tf_l"] * features["words"][word]["log_idf"] 
        features["words"][word]["ntf_n*df"] = features["words"][word]["ntf_n"] * features["words"][word]["df"] 
        features["words"][word]["ntf_n*log_df"] = features["words"][word]["ntf_n"] * features["words"][word]["log_df"] 
        features["words"][word]["ntf_n*idf"] = features["words"][word]["ntf_n"] * features["words"][word]["idf"] 
        features["words"][word]["ntf_n*log_idf"] = features["words"][word]["ntf_n"] * features["words"][word]["log_idf"] 
        features["words"][word]["ntf_l*df"] = features["words"][word]["ntf_l"] * features["words"][word]["df"] 
        features["words"][word]["ntf_l*log_df"] = features["words"][word]["ntf_l"] * features["words"][word]["log_df"] 
        features["words"][word]["ntf_l*idf"] = features["words"][word]["ntf_l"] * features["words"][word]["idf"] 
        features["words"][word]["ntf_l*log_idf"] = features["words"][word]["ntf_l"] * features["words"][word]["log_idf"] 
    return features



def write_output(output, features, frequency, stopwords):
    with open(output, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # header
        feature_names = ["word"] # the word itself
        feature_names.append("length") # word length
        feature_names.append("tf_n") # absolute natural term frequency
        feature_names.append("tf_l") # absolute logarithm term frequency
        feature_names.append("ntf_n") # normalized natural term frequency
        feature_names.append("ntf_l") # normalized logarithm term frequency
        feature_names.append("df") # normalized document frequency
        feature_names.append("log_df") # log normalized document frequency
        feature_names.append("idf") # absolute inverse document frequency
        feature_names.append("log_idf") # log inverse document frequency
        feature_names.append("tf_n*df")
        feature_names.append("tf_n*log_df")
        feature_names.append("tf_n*idf")
        feature_names.append("tf_n*log_idf")
        feature_names.append("tf_l*df")
        feature_names.append("tf_l*log_df")
        feature_names.append("tf_l*idf")
        feature_names.append("tf_l*log_idf")
        feature_names.append("ntf_n*df")
        feature_names.append("ntf_n*log_df")
        feature_names.append("ntf_n*idf")
        feature_names.append("ntf_n*log_idf")
        feature_names.append("ntf_l*df")
        feature_names.append("ntf_l*log_df")
        feature_names.append("ntf_l*idf")
        feature_names.append("ntf_l*log_idf")
        feature_names.append("rank") # rank
        feature_names.append("stopword") # whether the word is a stopword or not
        writer.writerow(feature_names)

        for word, rank in frequency.most_common():
            values = []
            for feature in feature_names:
                values.append(features["words"][word][feature])
            writer.writerow(values)


def main():
    parser = argparse.ArgumentParser(description = 'Extract features from potential stop words.')
    parser.add_argument("-t", "--text",
                        help = 'directory of tokenized text files, one word per line',
                        action = "store",
                        metavar = "DIR",
                        required = True)
    parser.add_argument("-s", "--stopword",
                        help = 'stopword list file',
                        action = "store",
                        metavar = "FILE",
                        required = True)
    parser.add_argument("-o", "--output",
                        help='output file',
                        action = "store",
                        metavar = "FILE",
                        required=True)
    parser.add_argument("-d", "--debug",
                        help='turn on debugging',
                        action = "store_true")

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    if args.debug:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        logger.setLevel(logging.DEBUG)  # Capture everything at the logger level

    texts = []


    # Define the directory path
    dir_path = Path(args.text)

    logger.info("Starting to read individual input files.")
    # Loop through all files in the directory
    for file_path in dir_path.iterdir():
        text = ""
        # Ensure it is a file, not a subfolder
        if file_path.is_file():
            try:
                text += file_path.read_text(encoding="utf-8")
            except PermissionError:
                None
            texts.append(text.splitlines())

    logger.info("Starting to read stopword file.")
    with open(args.stopword, "r") as file:
        stopwords = file.read().splitlines()

    logger.info("Starting to compute frequency list.")
    frequency = compute_frequency_list(texts)
    logger.info("Starting to compute features.")
    # Initialize features
    features = {"words": {},
                "total": 0,
                "rank": 1}
    features = initialize_features(frequency, features)
    logger.info("Starting to compute stopword features.")
    features = compute_stopword_feature(stopwords, features)
    logger.info("Starting to compute local word features.")
    features = compute_local_word_features(texts, frequency, features)
    logger.info("Starting to compute global word features.")
    features = compute_global_word_features(texts, features)
    logger.info("Starting to compute combined features.")
    features = compute_combined_features(texts, features)

    logger.info("Starting to write output.")
    write_output(args.output, features, frequency, stopwords)

if __name__ == '__main__':
    main()
