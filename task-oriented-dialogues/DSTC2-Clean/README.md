# BERT-DST

Contact: Guan-Lin Chao (guanlinchao@cmu.edu)

Source code of our paper [BERT-DST: Scalable End-to-End Dialogue State Tracking with Bidirectional Encoder Representations from Transformer](https://arxiv.org/abs/1907.03040) (Interspeech 2019).
```
@inproceedings{chao2019bert,
title={{BERT-DST}: Scalable End-to-End Dialogue State Tracking with Bidirectional Encoder Representations from Transformer},
author={Chao, Guan-Lin and Lane, Ian},
booktitle={INTERSPEECH},
year={2019}
}
```

Tested on Python 3.6, Tensorflow==1.13.0rc0

## Required packages (no need to install, just provide the paths in code):
1. [bert](https://github.com/google-research/bert)
2. uncased_L-12_H-768_A-12: pretrained [BERT-Base, Uncased] model checkpoint. Download link in [bert](https://github.com/google-research/bert).

## Datasets:
[dstc2-clean](https://github.com/guanlinchao/bert-dst/blob/master/storage/dstc2-clean.zip), [woz_2.0](https://github.com/guanlinchao/bert-dst/blob/master/storage/woz_2.0.zip), [sim-M and sim-R](https://github.com/google-research-datasets/simulated-dialogue)