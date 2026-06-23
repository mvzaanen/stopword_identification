#!/usr/bin/env python3

import argparse
import csv
from collections import Counter

def read_text(file):
    return file.read().split()

def compute_frequency_list(text):
    frequency = Counter(text)
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

def main():
    parser = argparse.ArgumentParser(description = 'Extract features from potential stop words.')
    parser.add_argument("-t", "--text",
                        help = 'tokenized text file, one word per line',
                        action = "store",
                        metavar = "FILE",
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

    with open(args.text, "r") as file:
        text = read_text(file)

    with open(args.stopword, "r") as file:
        stopwords = file.read().splitlines()

    features = {"words": {},
                "total": 0,
                "rank": 1}
    features = compute_local_word_features(text, features)

    with open(args.output, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # header
        feature_names = ["word", "length"] # word itself and its length
        feature_names.append("tf") # absolute term frequency
        feature_names.append("ntf") # normalized term frequency
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
            # word rank
            values.append(features["words"][word]["rank"])
            # is stopword
            values.append(word in stopwords)
            writer.writerow(values)


if __name__ == '__main__':
    main()
