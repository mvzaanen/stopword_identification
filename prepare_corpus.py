#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


def preprocess_brown(content):
    return re.sub(r"/[^ ]*", "", content)

def preprocess(content):
    return map(lambda t: t.lower(), content.split())

def write_tokens(output, tokenlist):
    output.write_text("\n".join(tokenlist) , encoding="utf-8")


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
    parser.add_argument("-b", "--brown",
                        help = 'do preprocessing for Brown corpus',
                        action='store_true')

    args = parser.parse_args()

    # Define the directory path
    dir_path = Path(args.input)

    # Loop through all files in the directory
    for file_path in dir_path.iterdir():
        # Ensure it is a file, not a subfolder
        if file_path.is_file():
            print(f"--- Reading: {file_path.name} ---")
            try:
                content = file_path.read_text(encoding="utf-8")
                if args.brown:
                    content = preprocess_brown(content)
                tokenlist = preprocess(content) 
                write_tokens(Path(args.output) / file_path.name, tokenlist)
            except PermissionError:
                None

if __name__ == '__main__':
    main()
