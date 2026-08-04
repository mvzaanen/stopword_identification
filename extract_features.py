#!/usr/bin/env python3

import argparse
import csv
from collections import Counter
from pathlib import Path
import math

def compute_frequency_list(text):
    frequency = Counter(text.splitlines())
    return frequency

def compute_local_word_features(text, features):
    frequency = compute_frequency_list(text)
    for word, count in frequency.most_common():
        if word not in features["words"]:
            features["words"][word] = {}
        features["words"][word]["tf"] = count
        features["words"][word]["rank"] = features["rank"]
        features["total"] += count
        features["rank"] += 1
    return features

def write_output(output, features, stopwords):
    with open(output, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # header
        feature_names = ["word", "length"] # word itself and its length
        feature_names.append("tf") # absolute term frequency
        feature_names.append("ntf") # normalized term frequency
        feature_names.append("lntf") # log normalized term frequency
        feature_names.append("rank") # rank
        feature_names.append("stopword") # whether the word is a stopword or not
        writer.writerow(feature_names)

        for word in features["words"].keys():
            values = []
            # word itself
            values.append(word)
            # word length
            values.append(len(word))
            # tf
            values.append(features["words"][word]["tf"])
            # ntf
            values.append(features["words"][word]["tf"]/features["total"])
            # lntf
            values.append(math.log(features["words"][word]["tf"]/features["total"]))
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

    text = ""

    # Define the directory path
    dir_path = Path(args.text)

    # Loop through all files in the directory
    for file_path in dir_path.iterdir():
        # Ensure it is a file, not a subfolder
        if file_path.is_file():
            print(f"--- Reading: {file_path.name} ---")
            try:
                text += file_path.read_text(encoding="utf-8")
            except PermissionError:
                None

    with open(args.stopword, "r") as file:
        stopwords = file.read().splitlines()

    features = {"words": {},
                "total": 0,
                "rank": 1}
    features = compute_local_word_features(text, features)

    write_output(args.output, features, stopwords)

if __name__ == '__main__':
    main()
