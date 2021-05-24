# Automatic-Emergency-Detection-in-Naval-VHF-Transmissions
![Shipwreck accident, ship run aground sink in ocean](https://image.freepik.com/free-vector/shipwreck-accident-ship-run-aground-sink-ocean_33099-2210.jpg)

## Master's Thesis

Jonathan Gildevall & Niclas Johansson

Chalmers University of Technology

### Automatic Emergency Detection in Naval VHF Transmissions
#### Investigating the feasibility of self-supervised speech-to-text models for complex domains with large amounts of unlabelled data

As the proficiency of Speech-To-Text (STT) services increases, so does the possible applications. This thesis explores the use of such services in very special domain, naval VHF transmissions. It explores STT service performance and details the development of a domain specific Speech-To-Text model based on the self-supervised wav2vec 2.0 architecture. This enabled the recognition of emergency messages using keyword detection and also created a foundation for more advanced intent analysis in the future. The developed model outperforms Google on the naval domain and achieves good classification results using keyword detection, managing to discern most messages containing one or more keywords. This performance meant that the model could be used as an aid for actual emergency message detection by Sjöfartsverket. The research also shows that many of the pre-trained models does not have adequate performance on the intended domain, but it was noted that using semi-supervised methods such pre-trained models can be tuned to reach acceptable performance levels. This can be done with smaller sets of domain specific data to achieve good result on the specific domains without the need of a completely new model for each domain.

The complete thesis can be found [here](thesis.pdf)
## Structure
An overview of the file structure:

```
root
├── startupkit
│   ├── data
│   │   ├── manifest
│   │   └── README.md
│   ├── Docker
│   │   ├── build.sh
│   │   ├── Dockerfile
│   │   └── run.sh
│   ├── misc
│   │   └── requirement.txt
│   ├── src
│   │   ├── fine-tune
│   │   │   ├── large_en_1h.yaml
│   │   │   └── large_en_10m.yaml
│   │   ├── pre-train
│   │   │   ├── large_jrcc.yaml
│   │   │   └── large_librivox.yaml
│   │   ├── config.json
│   │   ├── convert_wav2vec2_original_pytorch_checkpoint_to_pytorch.py
│   │   ├── dict_generator.py
│   │   ├── jrcc_labels.py
│   │   └── prepare_lm_lexicon.py
│   ├── .dockerignore
│   ├── LICENSE
│   └── README.md
├── system
│   ├── keywords.csv
│   └── emergency_detection.py
├── .gitignore
├── LICENSE
├── README.md
├── fairseq.md
└── thesis.pdf
```

A detailed account of how to setup the docker environment for wav2vec 2.0 development can be found [here](startupkit/README.md)

A guide to prepare the data and perform the training of a new wav2vec 2.0 model can be found [here](fairseq.md)

Please note: No models or data are present in this repository due to confidentiality

## How to perform emergency detection

To try the emergency detection using one of the text distance measure, an example is provided [here](system/emergency_detection.py).

The ````function```` flag can be set to one of the five algorithms:

* Hamming Distance : hamming
* Levenshtein Distance: levenshtein
* Damerau-Levenshtein: damerau_levenshtein
* Match Rating Approach: mra
* Longest Common Substring Similarity: lcsstr

Please Note: You need to specify the model path in the file itself.

Usage example:

```shell script
python emergency_detection.py path/To/wav keywords.csv --function=hamming
```

## Contact

Jonathan: [jonathan.gildevall@gmail.com](mailto:jonathan.gildevall@gmail.com?subject=[GitHub]%20Master's%20Thesis)

Niclas: [niclas.johansson97@gmail.com](mailto:niclas.johansson97@gmail.com?subject=[GitHub]%20Master's%20Thesis)

## Acknowledgements
Done in collaboration with [Tenfifty AB](https://tenfifty.io/)

Image Credit: [Designed by vectorpouch / Freepik](https://www.freepik.com")
