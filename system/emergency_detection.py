import argparse
import csv
import textdistance
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import soundfile as sf

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("config_file")
    parser.add_argument("--function", default="hamming", type=str, help="Text Similarity function to use")
    args = parser.parse_args()
    processor = Wav2Vec2Processor.from_pretrained("Path/To/Model")
    model = Wav2Vec2ForCTC.from_pretrained("Path/To/Model")
    functions = {"hamming": textdistance.hamming, "levenshtein": textdistance.levenshtein, "damerau_levenshtein":
        textdistance.damerau_levenshtein, "mra": textdistance.mra, "lcsstr": textdistance.lcsstr}
    function = functions[args.function]
    key_words = []
    thresholds = []
    csv_file = open(args.config_file)
    read_tsv = csv.reader(csv_file, delimiter=",")
    for row in read_tsv:
        key_words.append(row[0].upper())
        thresholds.append(float(row[1]))
    audio_input, _ = sf.read(args.input_file)
    inputs = processor(audio_input, sampling_rate=16_000, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    output = processor.batch_decode(predicted_ids)
    for i, key_word in enumerate(key_words):
        best = 0
        for word in output[0].split():
            word = word.upper()
            if best < function.normalized_similarity(word, key_word):
                best = function.normalized_similarity(word, key_word)
        if best > thresholds[i]:
            print("True")
        else:
            print("False")
