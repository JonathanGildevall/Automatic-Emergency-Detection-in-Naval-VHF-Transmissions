import argparse


def generate_dict(ltr, output_dir):
    letters = open(ltr, encoding="utf-8")
    with open(output_dir + "dict.ltr.txt", "w", encoding="utf-8") as out:
        wordcount = {}
        for row in letters:
            words = row.split()

            for word in words:
                if word in wordcount.keys():
                    wordcount[word] = wordcount[word] + 1
                else:
                    wordcount[word] = 1

        res = sorted(wordcount.items(), key=lambda word: word[1], reverse=True)
        print(res)

        for i in res:
            print(i[0] + " " + str(i[1]), file=out)
        print("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ltr")
    parser.add_argument("--output-dir", default="./", type=str, help="Path to the output dict.ltr.txt file.")

    args = parser.parse_args()
    generate_dict(
        args.ltr, args.output_dir
    )
