#!/usr/bin/env python3

import argparse
import csv
from collections import Counter
from pathlib import Path
import math

def compute_frequency_list(texts):
    # flatten list of texts
    full_text = [item for sublist in texts for item in sublist]
    frequency = Counter(full_text)
    return frequency


def compute_local_word_features(text, frequency, features):
    for word, count in frequency.most_common():
        if word not in features["words"]:
            features["words"][word] = {}
        features["words"][word]["tf_n"] = count
        features["words"][word]["tf_l"] = 1 + math.log(count)
        features["words"][word]["rank"] = features["rank"]
        features["total"] += count
        features["rank"] += 1
    return features


def compute_global_word_features(texts, frequency, features):
    N = len(texts)
    text_sets = []
    for text in texts:
        text_sets.append(set(text))
    for word in frequency.keys():
        document_count = 0
        for text_set in text_sets:
            if word in text_set:
                document_count += 1
        features["words"][word]["df"] = document_count/N
        features["words"][word]["log_df"] = math.log(features["words"][word]["df"]) if features["words"][word]["df"] > 0 else float('-inf')
        features["words"][word]["idf"] = N/document_count if document_count > 0 else 0
        features["words"][word]["log_idf"] = math.log(features["words"][word]["idf"]) if features["words"][word]["idf"] > 0 else float('-inf')

    return features


def write_output(output, features, stopwords):
    with open(output, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # header
        feature_names = ["word", "length"] # word itself and its length
        feature_names.append("tf_n") # absolute natural term frequency
        feature_names.append("tf_l") # absolute logarithm term frequency
        feature_names.append("ntf_n") # normalized natural term frequency
        feature_names.append("ntf_l") # normalized logarithm term frequency
        feature_names.append("df") # normalized document frequency
        feature_names.append("log_df") # log normalized document frequency
        feature_names.append("rank") # rank
        feature_names.append("stopword") # whether the word is a stopword or not
        writer.writerow(feature_names)

        for word in features["words"].keys():
            values = []
            # word itself
            values.append(word)
            # word length
            values.append(len(word))
            # tf_n
            values.append(features["words"][word]["tf_n"])
            # tf_l
            values.append(features["words"][word]["tf_l"])
            # ntf_n
            values.append(features["words"][word]["tf_n"]/features["total"])
            # ntf_l
            values.append(features["words"][word]["tf_l"]/features["total"])
            # df
            values.append(features["words"][word]["df"])
            # log_df
            values.append(features["words"][word]["log_df"])
            # idf
            values.append(features["words"][word]["idf"])
            # log_idf
            values.append(features["words"][word]["log_idf"])
            # word rank
            values.append(features["words"][word]["rank"])
            # is stopword
            values.append(word in stopwords)
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

    args = parser.parse_args()

    texts = []

    # Define the directory path
    dir_path = Path(args.text)

    # Loop through all files in the directory
    for file_path in dir_path.iterdir():
        text = ""
        # Ensure it is a file, not a subfolder
        if file_path.is_file():
            print(f"--- Reading: {file_path.name} ---")
            try:
                text += file_path.read_text(encoding="utf-8")
            except PermissionError:
                None
            texts.append(text.splitlines())

    with open(args.stopword, "r") as file:
        stopwords = file.read().splitlines()

    # Initialize features
    features = {"words": {},
                "total": 0,
                "rank": 1}
    frequency = compute_frequency_list(texts)
    features = compute_local_word_features(texts, frequency, features)
    features = compute_global_word_features(texts, frequency, features)

    write_output(args.output, features, stopwords)

if __name__ == '__main__':
    main()
