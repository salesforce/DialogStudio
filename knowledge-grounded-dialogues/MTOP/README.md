## Multilingual TOP dataset for semantic parsing

This repository contains the multilingual TOP dataset created in the paper:

_"Multilingual Neural Semantic Parsing for Low-Resourced Languages". Menglin Xia, Emilio Monti. *SEM2021._ [\[arxiv\]](https://arxiv.org/abs/2106.03469)

Please cite our paper if you use this dataset.


### Description

The multilingual TOP dataset is a multilingual semantic parsing dataset in English, Italian and Japanese, based on the public Facebook Task Oriented
Parsing (TOP) dataset in English. The original TOP dataset can be found here: [\[paper\]](https://research.fb.com/publications/semantic-parsing-for-task-oriented-dialog-using-hierarchical-representations/) [\[data\]](http://fb.me/semanticparsingdialog).

The Multilingual TOP dataset contains ˜30k training and validation data and ˜8k test data in English, Italian and Japanese. The Italian and Japanese training and validation data are machine-translated from English TOP, and the test data are manually translated.


### Abstract

Multilingual semantic parsing is a cost-effective method that allows a single model to understand different languages. However, researchers face a great imbalance of availability of training data, with English being resource rich, and other languages having much less data. To tackle the data limitation problem, we propose using machine translation to bootstrap multilingual training data from the more abundant English data. To compensate for the data quality of machine translated training data, we utilize transfer learning from pretrained multilingual encoders to further improve the model. To evaluate our multilingual models on human-written sentences as opposed to machine translated ones, we introduce a new multilingual semantic parsing dataset in English, Italian and Japanese based on the Facebook Task Oriented Parsing (TOP) dataset. We show that joint multilingual training with pretrained encoders substantially outperforms our baselines on the TOP dataset and outperforms the state-of-the-art model on the public NLMaps dataset. We also establish a new baseline for zero-shot learning on the TOP dataset. We find that a semantic parser trained only on English data achieves a zero-shot performance of 44.9% exact-match accuracy on Italian sentences. 

### Directories

The `raw_test_data` directory contains the manually translated test sets in Italian and Japanese in xml.

The `processed_data` directory contains the processed multilingual TOP semantic parsing data (train, dev, test) used in the paper.

### Citation

If you use the dataset, you can use the following citation:
```
@inproceedings{xia2021multilingual,
title={Multilingual Neural Semantic Parsing for Low-Resourced Languages},
author={Xia, Menglin and Monti, Emilio},
booktitle={The Tenth Joint Conference on Lexical and Computational Semantics},
year = {2021}
}
```


## License Summary

The documentation is made available under the Creative Commons Attribution-ShareAlike 4.0 International License. See the LICENSE file.

The sample code within this documentation is made available under the MIT-0 license. See the LICENSE-SAMPLECODE file.

