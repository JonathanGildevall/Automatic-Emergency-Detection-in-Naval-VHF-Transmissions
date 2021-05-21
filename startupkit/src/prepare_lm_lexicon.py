from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import re


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KenLM lexicon creator")
    parser.add_argument(
        "lm", help="arpa"
    )
    parser.add_argument(
        "--output-dir", help="data destination directory", default="./"
    )

    args = parser.parse_args()
    path = args.output_dir
    os.makedirs(path, exist_ok=True)


    arpa_file = args.lm

    # prepare lexicon word -> tokens spelling
    # write words to lexicon.txt file
    lex_file = os.path.join(path, "lexicon.txt")
    print("Writing Lexicon file - {}...".format(lex_file))
    with open(lex_file, "w") as f:
        # get all the words in the arpa file
        with open(arpa_file, "r") as arpa:
            for line in arpa:
                # verify if the line corresponds to unigram
                if not re.match(r"[-]*[0-9\.]+\t\S+\t*[-]*[0-9\.]*$", line):
                    continue
                word = line.split("\t")[1]
                word = word.strip().lower()
                if word == "<unk>" or word == "<s>" or word == "</s>":
                    continue
                assert re.match("^[a-z']+$", word), "invalid word - {w}".format(w=word)
                f.write("{w}\t{s} |\n".format(w=word, s=" ".join(word)))

    print("Done!", flush=True)