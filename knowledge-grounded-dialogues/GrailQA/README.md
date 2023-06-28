# GrailQA: Strongly <ins>G</ins>ene<ins>ra</ins>l<ins>i</ins>zab<ins>l</ins>e Question Answering
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg?style=flat-square)](https://github.com/dki-lab/GrailQA/issues)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![language-python3](https://img.shields.io/badge/Language-Python3-blue.svg?style=flat-square)](https://www.python.org/)
[![made-with-Pytorch](https://img.shields.io/badge/Made%20with-Pytorch-orange.svg?style=flat-square)](https://pytorch.org/)
[![paper](https://img.shields.io/badge/Paper-WWW2021-lightgrey?style=flat-square)](https://arxiv.org/abs/2011.07743)
<img width="1175" alt="image" src="https://user-images.githubusercontent.com/15921425/110228546-f2193380-7ecf-11eb-8cbd-c5097a064ee4.png">

>GrailQA is a new large-scale, high-quality KBQA dataset with 64,331 questions annotated with both answers and corresponding logical forms in different syntax (i.e., SPARQL, S-expression, etc.). It can be used to test three levels of generalization in KBQA: **i.i.d.**, **compositional**, and **zero-shot**.

>This is the accompanying code for the paper "[Beyond I.I.D.: Three Levels of Generalization for Question Answering on Knowledge Bases](https://arxiv.org/abs/2011.07743)" published at TheWebConf (previously WWW) 2021. For dataset and leaderboard, please refer to the [homepage of GrailQA](https://dki-lab.github.io/GrailQA/). In this repository, we provide the code for the baseline models for reproducibility and demonstrate how to work with this dataset.

## Package Description

This repository is structured as follows:

```
GrailQA/
├─ model_configs/
|    ├─ train/: Configuration files for training
|    └── test/: Configuration files for inference
├─ data/: Data files for training, validation, and test
├─ ontology/: Processed Freebase ontology files
|    ├─ domain_dict: Mapping from a domain in Freebase Commons to all schema items in it
|    ├─ domain_info: Mapping from a schema item to a Freebase Commons domain it belongs to
|    ├─ fb_roles: Domain and range information for a relation (Note that here domain means a different thing from domains in Freebase Commons)
|    ├─ fb_types: Class hierarchy in Freebase
|    └── reverse_properties: Reverse properties in Freebase 
├─ bert_configs/: BERT configuration used by pytorch_transformer, which you are very unlikely to modify
├─ entity_linking_results/: Entity linking results 
├─ entity_linker/: source code for the entity linker, which is a separate module from our main model
├─ vocabulary/: Preprocessed vocabulary, which is only required by our GloVe-based models
├─ cache/: Cached results for SPARQL queries, which are used to accelerate the experiments by caching many SPARQL query results offline
├─ saved_models/: Trained models
├─ utils/:
|    ├─ bert_interface.py: Interface to BERT 
|    ├─ logic_form_util: Tools related to logical forms, including the exact match checker for two logical forms
|    ├─ search_over_graphs.py: Generate candidate logical forms for our Ranking models
|    └── sparql_executor: Sparql-related tools
├─ bert_constrained_seq2seq.py: BERT-based model for both Ranking and Transduction
├─ bert_seq2seq_reader.py: Data reader for BERT-based models
├─ constrained_seq2seq.py: GloVe-based model for both Ranking and Transduction
├─ constrained_seq2seq_reader.py: Data reader for GloVe-based models
└── run.py: Main function
```

## Setup

Follow these steps if you want to reproduce the results in the paper.
1. Follow [Freebase Setup](https://github.com/dki-lab/Freebase-Setup) to set up a Virtuoso triplestore service. After starting your virtuoso service, replace the url in `utils/sparql_executer.py` with your own.
2. Download cache files from https://1drv.ms/u/s!AuJiG47gLqTznjfRRxdW5YDYFt3o?e=GawH1f and put all the files under `cache/`.
3. Download trained models from https://1drv.ms/u/s!AuJiG47gLqTznxbenfeRBrTuTbWz?e=g5Nazi and put all the files under `saved_models/`.
4. Download GrailQA dataset and put it under `data/`.
5. Install all required libraries:
```
$ pip install -r requirements.txt
```
**(Note: we have included our adapted version of AllenNLP in this repo so there's no need to separately install that.)**

## Reproduce Our Results

The predictions of our baseline models can be found via [CodaLab](https://worksheets.codalab.org/worksheets/0x53f31035f34e4b6194ebe16179944297).
Run `predict` command to reproduce the predictions. There are several arguments to configure to run `predict`:
```
python run.py predict
  [path_to_saved_model]
  [path_to_test_data]
  -c [path_to_the_config_file]
  --output-file [results_file_name] 
  --cuda-device [cuda_device_to_use]
```
Specifically, to run Ranking+BERT:
```
$ PYTHONHASHSEED=23 python run.py predict saved_models/BERT/model.tar.gz data/grailqa_v1.0_test_public.json --include-package bert_constrained_seq2seq --include-package bert_seq2seq_reader --include-package utils.bert_interface --use-dataset-reader --predictor seq2seq -c model_configs/test/bert_ranking.jsonnet --output-file bert_ranking.txt --cuda-device 0
```
To run Ranking+GloVe:
```
$ PYTHONHASHSEED=23 python run.py predict predict saved_models/GloVe/model.tar.gz data/grailqa_v1.0_test_public.json --include-package constrained_seq2seq --include-package constrained_seq2seq_reader --predictor seq2seq --use-dataset-reader -c model_configs/test/glove_ranking.jsonnet --output-file glove_ranking.txt --cuda-device 0
```
To run Transduction+BERT:
```
$ PYTHONHASHSEED=23 python run.py predict saved_models/BERT/model.tar.gz data/grailqa_v1.0_test_public.json --include-package bert_constrained_seq2seq --include-package bert_seq2seq_reader --include-package utils.bert_interface --use-dataset-reader --predictor seq2seq -c model_configs/test/bert_vp.jsonnet --output-file bert_vp.txt --cuda-device 0
```
To run Transduction+GloVe:
```
$ PYTHONHASHSEED=23 python run.py predict predict saved_models/GloVe/model.tar.gz data/grailqa_v1.0_test_public.json --include-package constrained_seq2seq --include-package constrained_seq2seq_reader --predictor seq2seq --use-dataset-reader -c model_configs/test/glove_vp.jsonnet --output-file glove_vp.txt --cuda-device 0
```

### Entity Linking
We also release our code for entity linking to facilitate future research. Similar to most other KBQA methods, entity linking is a separate module from our main model. If you just want to run our main models, you do not need to re-run our entity linking module because our models directly use the entity linking results under `entity_linking/`.

Our entity linker is based on [BERT-NER](https://github.com/kamalkraj/BERT-NER) and the popularity-based entity disambiguation in [aqqu](https://github.com/ad-freiburg/aqqu). Specifically, we use the NER model to identify a set of entity mentions, and then use the identified mentions to retieve Freebase entities from the entity memory constructed from Freebase entity mentions information (i.e., mentions in FACC1 and all alias in Freebase if not included in FACC1<sup>1</sup>). 

To run our entity linker, first download the mentions data from https://1drv.ms/u/s!AuJiG47gLqTznjl7VbnOESK6qPW2?e=HDy2Ye and put all data under `entity_linker/data/`.
Second, download our trained NER model from https://1drv.ms/u/s!AuJiG47gLqTznjge7wLqAZiSMIcU?e=5RpKaC, which is trained using the training data of GrailQA, and put it under `entity_linker/BERT_NER/`.
Then you should be all set! We provide a use example in `entity_linker/bert_entity_linker.py`. Follow the use example to identiy entities using our entity linker for your own data.

[1]: FACC1 containes the mentions information for around 1/8 of Freebase entities, including different mentions for those entities and the frequency for each mention. For entities not included in FACC1, we use the following properties to retrieve the mentions for each entity: `<http://rdf.freebase.com/ns/type.object.name>`, `<http://rdf.freebase.com/ns/common.topic.alias>`, `<http://rdf.freebase.com/key/wikipedia.en>`. Note that we don't have frequency information for those entity mentions, so we simply treat the number of occurences as 1 for all of them in our implementation.

## Train New Models
You can also use our code to train new models.

### Training Configuration
Following [AllenNLP](https://github.com/allenai/allennlp), our `train` command also takes a configuration file as input to specify all model hyperparameters and training related parameters such as learning rate, batch size, cuda device, etc. Most parameters in the training configuration files (i.e., files under `model_configs/train/`) are hopefully intutive based on their names, so we will only explain those parameters that might be confusing here.
```
- ranking: Ranking model or generation mode. True for Ranking, and false for Transduction.
- offline: Whether to use cached files under cache/.
- num_constants_per_group: Number of schema items in each chunk for BERT encoding.
- gq1: True for GraphQuestions, and false for GrailQA.
- use_sparql: Whether to use SPARQL as the target query. Set to be false, because in this paper we are using S-expressions.
- use_constrained_vocab: Whether to do vocabulary pruning or not.
- constrained_vocab: If we do vocabulary pruning, how to do it? Options include 1_step, 2_step and mix2.
- perfect_entity_linking: Whether to assume gold entities are given.
```

### Training Command
To train the BERT-based model, run:
```
$ PYTHONHASHSEED=23 python run.py train model_configs/train/train_bert.jsonnet --include-package bert_constrained_seq2seq --include-package bert_seq2seq_reader --include-package utils.bert_interface -s [your_path_specified_for_training]
```
To train the GloVe-based model, run:
```
$ PYTHONHASHSEED=23 python run.py train model_configs/train/train_glove.jsonnet --include-package constrained_seq2seq --include-package constrained_seq2seq_reader -s [your_path_specified_for_training]
```

### Online Running Time
We also show the running time of inference in online mode, in which offline caches are disabled. The aim of this setting is to mimic the real scenario in production. To report the average running time, we randomly sample 1,000 test questions for each model and run every model on a single GeoForce RTX 2080-ti GPU card with batch size 1. A comparison of different models is shown below:

|                        | Transduction   | Transduction-BERT   | Transduction-VP   | Transduction-BERT-VP   | Ranking   | Ranking-BERT   |
|------------------------|:--------------:|:-------------------:|:-----------------:|:----------------------:|:---------:|:--------------:|
| Running time (seconds) | 60.899         | 50.176              | 4.787             | 1.932                  | 115.459   | 80.892         |


The running time is quite significant when either ranking mode or vocabulary pruning is activated. This is because running SPARQL queries to query the 2-hop information (i.e., either candidate logical forms for ranking or 2-hop schema items for vocabulary pruning) is very time-consuming. This is also a general issue for the enumeration+ranking framework in KBQA, which is used by many existing methods. This issue has to some extent been underaddressed so far. A common practice is to use offline cache to store the exectuions of all related SPARQL queries, which assumes the test questions are known in advance. This assumption is true for existing KBQA benchmarks but is not realistic for a real production system. How to improve the efficiency of KBQA models while maintaining their efficacy is still an active area for research.

## Citation
Please please consider citing the following BibTeX entry if you find our work helpful to your research.
```
@inproceedings{gu2021beyond,
  title={Beyond IID: three levels of generalization for question answering on knowledge bases},
  author={Gu, Yu and Kase, Sue and Vanni, Michelle and Sadler, Brian and Liang, Percy and Yan, Xifeng and Su, Yu},
  booktitle={Proceedings of the Web Conference 2021},
  pages={3477--3488},
  organization={ACM}
}
```

## Acknowledgement
Many thanks to the feedbacks & helpful discussions from people in OSU NLP Group.

### &#8627; Stargazers
[![Stargazers repo roster for @nastyox/Repo-Roster](https://reporoster.com/stars/dki-lab/GrailQA)](https://github.com/dki-lab/GrailQA/stargazers)

### &#8627; Forkers
[![Forkers repo roster for @nastyox/Repo-Roster](https://reporoster.com/forks/dki-lab/GrailQA)](https://github.com/dki-lab/GrailQA/network/members)
