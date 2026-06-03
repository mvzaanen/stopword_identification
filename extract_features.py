#!/usr/bin/env python3

import argparse
import csv

def extract_word_frequency(frequency_lines):
    word_frequency = {}
    for line in frequency_lines:
        components = line.split()
        word_frequency[components[1]] = int(components[0])
    return word_frequency

def main():
    parser = argparse.ArgumentParser(description = 'Extract features from potential stop words.')
    parser.add_argument("-f", "--frequency",
                        help = 'frequency list file',
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

    with open(args.frequency, "r") as file:
        frequency_lines = file.read().splitlines()
        frequency = extract_word_frequency(frequency_lines)
    with open(args.stopword, "r") as file:
        stopwords = file.read().splitlines()
    with open(args.output, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # header
        writer.writerow(["word", "length", "frequency", "stopword"])

        for word in frequency.keys():
            features = []
            # word itself
            features.append(word)
            # word length
            features.append(len(word))
            # word frequency
            features.append(frequency[word])
            # is stopword
            features.append(word in stopwords)
            writer.writerow(features)


if __name__ == '__main__':
    main()
