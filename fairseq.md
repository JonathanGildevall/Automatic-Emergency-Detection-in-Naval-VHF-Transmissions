
# wav2vec 2.0

## Training a new model with the CLI tools

Given a directory containing wav files to be used for pretraining (we recommend splitting each file into separate file 10 to 30 seconds in length)

### Prepare training data manifest:

First, install the `soundfile` library:
```shell script
pip install soundfile
```

Next, run:

```shell script
$ python examples/wav2vec/wav2vec_manifest.py /path/to/waves --dest /data/manifest --ext $ext --valid-percent $valid
```

$ext should be set to flac, wav, or whatever format your dataset happens to use that soundfile can read.

$valid should be set to some reasonable percentage (like 0.01) of training data to use for validation.
To use a pre-defined validation set (like dev-other from librispeech), set to it 0 and then overwrite valid.tsv with a
separately pre-processed manifest file.

### Train a wav2vec 2.0 large model:

This configuration was used for the large model trained on the Libri-light dataset in the wav2vec 2.0 paper
Note that the input is expected to be single channel, sampled at 16 kHz


```shell script
$ fairseq-hydra-train \
    task.data=/data/manifest \
    --config-dir /src/pretraining \
    --config-name large_librivox
```

### Fine-tune a pre-trained model with CTC:

Fine-tuning a model requires parallel audio and labels file, as well as a vocabulary file in fairseq format.

An example [script](libri_labels.py) that generates labels for the Librispeech dataset from the tsv file produced by wav2vec_manifest.py can be used as follows:

```shell script
split=train
$ python libri_labels.py /path/to/tsv --output-dir /data/manifest --output-name $split
```

An example [script](jrcc_labels.py) that generates labels for the JRCC dataset from the tsv file produced by wav2vec_manifest.py can be used as follows:

```shell script
split=train
$ python jrcc_labels.py /path/to/tsv --output-dir /data/manifest --output-name $split
```

A letter vocabulary can generated using the [script](dict_generator.py) on the generated train.ltr file:
```shell script
$ python dict_generator.py /path/to/ltr --output-dir /data/manifest
```

Fine-tuning on the Swedish part of the JRCC data with letter targets:
```shell script
$ fairseq-hydra-train \
    task.data=/data/manifest \
    model.w2v_path=/src/model.pt \
    --config-dir /src/finetuning \
    --config-name large_sv_10m
```

There are other config files in the config/finetuning directory that can be used to fine-tune on other splits.
You can specify the right config via the `--config-name` parameter.

Decoding with a language model during training requires flashlight [python bindings](https://github.com/facebookresearch/flashlight/tree/master/bindings/python) (previously called [wav2letter](https://github.com/facebookresearch/wav2letter).
If you want to use a language model, add `+criterion.wer_args='[/path/to/kenlm, /path/to/lexicon, 2, -1]'` to the command line.

### Evaluating a CTC model:

```shell script
python examples/speech_recognition/infer.py /data/manifest --task audio_pretraining \
--nbest 1 --path /path/to/model --gen-subset valid --results-path /path/to/save/results --w2l-decoder viterbi \
--criterion ctc --labels ltr --max-tokens 4000000 \
--post-process letter
```

Evaluating a CTC model with a language model requires [flashlight python bindings](https://github.com/facebookresearch/flashlight/tree/master/bindings/python) (previously called [wav2letter](https://github.com/facebookresearch/wav2letter) to be installed.

Fairseq transformer language model used in the wav2vec 2.0 paper can be obtained from the [wav2letter model repository](https://github.com/facebookresearch/wav2letter/tree/master/recipes/sota/2019).
Be sure to upper-case the language model vocab after downloading it.

Letter dictionary for pre-trained models can be found [here](https://dl.fbaipublicfiles.com/fairseq/wav2vec/dict.ltr.txt).

A lexicon for the KenLM models can be generated using the [script](prepare_lm_lexicon.py) as follows:

```shell script
$ python prepare_lm_lexicon.py /path/to/kenlm.arpa --output-dir /data/manifest
```

Next, run the evaluation command:

```shell script
$subset=dev_other
python examples/speech_recognition/infer.py /data/manifest --task audio_pretraining \
--nbest 1 --path /path/to/model --gen-subset $subset --results-path /path/to/save/results --w2l-decoder kenlm \
--lm-model /path/to/kenlm.bin --lm-weight 2 --word-score -1 --sil-weight 0 --criterion ctc --labels ltr --max-tokens 4000000 \
--lexicon /data/manifest/lexicon.txt --post-process letter
```

To get raw numbers, use --w2l-decoder viterbi and omit the lexicon. To use the transformer language model, use --w2l-decoder fairseqlm.

## Use wav2vec 2.0 with 🤗Transformers:

Wav2Vec2 is also available in the [🤗Transformers library](https://github.com/huggingface/transformers) since version 4.3.

Pretrained Models can be found on the [hub](https://huggingface.co/models?filter=wav2vec2) 
and documentation can be found [here](https://huggingface.co/transformers/master/model_doc/wav2vec2.html).

Convert checkpoint.pt to HuggingFace Model:
```shell script
python convert_wav2vec2_original_pytorch_checkpoint_to_pytorch --pytorch_dump_folder_path \
/path/to/model/destination --checkpoint_path /path/to/fairseq/checkpoint.pt --dict_path \
/path/to/dict/of/fine-tuned/model --config_path /path/to/hf/config.json
```

Usage example:

```python
# !pip install transformers
import soundfile as sf
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# load pretrained model
processor = Wav2Vec2Processor.from_pretrained("path/to/model")
model = Wav2Vec2ForCTC.from_pretrained("path/to/model")

# load audio
audio_input, _ = sf.read("path/to/audio/file")

# transcribe
input_values = processor(audio_input, sampling_rate=16_000, return_tensors="pt").input_values
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)[0]
```

There's also an example of the implemented system in this [script](system/emergency_detection.py).
