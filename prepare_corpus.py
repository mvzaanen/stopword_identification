#!/usr/bin/env python3

import argparse
import re
import random
from pathlib import Path

def create_filepointers(output_dir, parts):
    files = []
    if parts is None:
        return files
    for p in range(int(parts)):
        filename = f"{p:05}"
        files.append((Path(output_dir) / filename).open(mode = 'w'))
    return files

def preprocess_brown(content):
    return re.sub(r"/[^ ]*", "", content)

def preprocess(content):
    content = content.split()
    content = [word for word in content if word.isalpha()]
    return map(lambda t: t.lower(), content)

def write_tokens(output_files, tokenlist):
    for token in tokenlist:
        random.choice(output_files).write(token + "\n")


def main():
    parser = argparse.ArgumentParser(description = 'Prepare corpus for stopword analysis.')
    parser.add_argument("-i", "--input",
                        help = 'input directory',
                        action = "store",
                        metavar = "DIR",
                        required = True)
    parser.add_argument("-o", "--output",
                        help = 'output directory',
                        action = "store",
                        metavar = "DIR",
                        required = True)
    parser.add_argument("-p", "--parts",
                        help = 'shuffle text in this many parts',
                        action = "store",
                        metavar = "NUM",
                        required = False)
    parser.add_argument("-b", "--brown",
                        help = 'do preprocessing for Brown corpus',
                        action='store_true')

    args = parser.parse_args()

    # Define the directory path
    dir_path = Path(args.input)

    output_files = create_filepointers(args.output, args.parts)

    # Loop through all files in the directory
    for file_path in dir_path.iterdir():
        # Ensure it is a file, not a subfolder
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                if args.brown:
                    content = preprocess_brown(content)
                tokenlist = preprocess(content) 
                if args.parts is None:
                    output_files = [(Path(args.output) / file_path.name).open(mode='w')]
                write_tokens(output_files, tokenlist)
            except PermissionError:
                None

if __name__ == '__main__':
    main()
