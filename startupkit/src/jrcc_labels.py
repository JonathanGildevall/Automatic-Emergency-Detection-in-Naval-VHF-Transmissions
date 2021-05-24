#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Helper script to pre-compute embeddings for a flashlight (previously called wav2letter++) dataset
"""

import argparse
import os
import pandas as pd


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv")
    parser.add_argument("csv")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--output-name", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    transcriptions = {}

    with open(args.tsv, "r") as tsv, open(
        os.path.join(args.output_dir, args.output_name + ".ltr"), "w"
    ) as ltr_out, open(
        os.path.join(args.output_dir, args.output_name + ".wrd"), "w"
    ) as wrd_out:
        _ = next(tsv).strip()
        labels = pd.read_csv(args.csv, index_col=1)
        for line in tsv:
            line = line.strip()
            file, _ = line.split('\t')
            if file not in transcriptions:
                items = labels.loc[file]["Transcription"].upper().strip().split()
                transcriptions[file] = " ".join(items)
            print(transcriptions[file], file=wrd_out)
            print(
                " ".join(list(transcriptions[file].replace(" ", "|"))) + " |",
                file=ltr_out,
            )


