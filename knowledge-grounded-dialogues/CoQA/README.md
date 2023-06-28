# coqa-baselines
We provide several baselines: conversational models, extractive reading comprehension models and their combined models for the [CoQA challenge](https://stanfordnlp.github.io/coqa/). See more details in the [paper](https://arxiv.org/abs/1808.07042). We also provide [instructions](codalab.md) on how to run pretrained models on Codalab -- our platform for evaluation on the test set.

As we use the [OpenNMT-py](https://github.com/OpenNMT/OpenNMT-py) library for all our seq2seq experiments, please use the following command to clone our repository.

```bash
  git clone --recurse-submodules git@github.com:stanfordnlp/coqa-baselines.git
```

This code repository was mostly written by [Danqi Chen](https://github.com/danqi), built on top of the [DrQA](https://github.com/facebookresearch/DrQA) and [OpenNMT-py](https://github.com/OpenNMT/OpenNMT-py) projects, with some help from [Shayne Longpre](https://github.com/Shayne13/) and [Siva Reddy](https://github.com/sivareddyg). If you have any questions about this repository, please use Github Issues.


## Requirements
```
torch>=0.4.0
torchtext==0.2.1
gensim
pycorenlp
```

## Download
Download the dataset:
```bash
  mkdir data
  wget -P data https://nlp.stanford.edu/data/coqa/coqa-train-v1.0.json
  wget -P data https://nlp.stanford.edu/data/coqa/coqa-dev-v1.0.json
```

Download pre-trained word vectors:
```bash
  mkdir wordvecs
  wget -P wordvecs http://nlp.stanford.edu/data/wordvecs/glove.42B.300d.zip
  unzip -d wordvecs wordvecs/glove.42B.300d.zip
  wget -P wordvecs http://nlp.stanford.edu/data/wordvecs/glove.840B.300d.zip
  unzip -d wordvecs wordvecs/glove.840B.300d.zip
```

## Start a CoreNLP server

```bash
  mkdir lib
  wget -P lib http://central.maven.org/maven2/edu/stanford/nlp/stanford-corenlp/3.9.1/stanford-corenlp-3.9.1.jar
  java -mx4g -cp lib/stanford-corenlp-3.9.1.jar edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```

## Conversational models
### Preprocessing
Generate the input files for seq2seq models --- needs to start a CoreNLP server (`n_history` can be changed to {0, 1, 2, ..} or -1):
```bash
  python scripts/gen_seq2seq_data.py --data_file data/coqa-train-v1.0.json --n_history 2 --lower --output_file data/seq2seq-train-h2
  python scripts/gen_seq2seq_data.py --data_file data/coqa-dev-v1.0.json --n_history 2 --lower --output_file data/seq2seq-dev-h2
```

Preprocess the data and embeddings:
```bash
  python seq2seq/preprocess.py -train_src data/seq2seq-train-h2-src.txt -train_tgt data/seq2seq-train-h2-tgt.txt -valid_src data/seq2seq-dev-h2-src.txt -valid_tgt data/seq2seq-dev-h2-tgt.txt -save_data data/seq2seq-h2 -lower -dynamic_dict -src_seq_length 10000
  PYTHONPATH=seq2seq python seq2seq/tools/embeddings_to_torch.py -emb_file_enc wordvecs/glove.42B.300d.txt -emb_file_dec wordvecs/glove.42B.300d.txt -dict_file data/seq2seq-h2.vocab.pt -output_file data/seq2seq-h2.embed
```

### Training
Run a seq2seq (with attention) model:
```bash
   python seq2seq/train.py -data data/seq2seq-h2 -save_model seq2seq_models/seq2seq -word_vec_size 300 -pre_word_vecs_enc data/seq2seq-h2.embed.enc.pt -pre_word_vecs_dec data/seq2seq-h2.embed.dec.pt -epochs 50 -gpuid 0 -seed 123
```

Run a seq2seq+copy model:
```bash
   python seq2seq/train.py -data data/seq2seq-h2 -save_model seq2seq_models/seq2seq_copy -copy_attn -reuse_copy_attn -word_vec_size 300 -pre_word_vecs_enc data/seq2seq.embed.enc.pt -pre_word_vecs_dec data/seq2seq.embed.dec.pt -epochs 50 -gpuid 0 -seed 123
```

### Testing
```bash
  python seq2seq/translate.py -model seq2seq_models/seq2seq_copy_acc_65.49_ppl_4.71_e15.pt -src data/seq2seq-dev-h2-src.txt -output seq2seq_models/pred.txt -replace_unk -verbose -gpu 0
  python scripts/gen_seq2seq_output.py --data_file data/coqa-dev-v1.0.json --pred_file seq2seq_models/pred.txt --output_file seq2seq_models/seq2seq_copy.prediction.json
```


## Reading comprehension models
### Preprocessing
Generate the input files for the reading comprehension (extractive question answering) model -- needs to start a CoreNLP server:
```bash
  python scripts/gen_drqa_data.py --data_file data/coqa-train-v1.0.json --output_file coqa.train.json
  python scripts/gen_drqa_data.py --data_file data/coqa-dev-v1.0.json --output_file coqa.dev.json
```

### Training
`n_history` can be changed to {0, 1, 2, ..} or -1.
```bash
  python rc/main.py --trainset data/coqa.train.json --devset data/coqa.dev.json --n_history 2 --dir rc_models --embed_file wordvecs/glove.840B.300d.txt
```


### Testing
```bash
  python rc/main.py --testset data/coqa.dev.json --n_history 2 --pretrained rc_models
```

## The pipeline model
### Preprocessing
```bash
  python scripts/gen_pipeline_data.py --data_file data/coqa-train-v1.0.json --output_file1 data/coqa.train.pipeline.json --output_file2 data/seq2seq-train-pipeline
  python scripts/gen_pipeline_data.py --data_file data/coqa-dev-v1.0.json --output_file1 data/coqa.dev.pipeline.json --output_file2 data/seq2seq-dev-pipeline
  python seq2seq/preprocess.py -train_src data/seq2seq-train-pipeline-src.txt -train_tgt data/seq2seq-train-pipeline-tgt.txt -valid_src data/seq2seq-dev-pipeline-src.txt -valid_tgt data/seq2seq-dev-pipeline-tgt.txt -save_data data/seq2seq-pipeline -lower -dynamic_dict -src_seq_length 10000
  PYTHONPATH=seq2seq python seq2seq/tools/embeddings_to_torch.py -emb_file_enc wordvecs/glove.42B.300d.txt -emb_file_dec wordvecs/glove.42B.300d.txt -dict_file data/seq2seq-pipeline.vocab.pt -output_file data/seq2seq-pipeline.embed
```

### Training
`n_history` can be changed to {0, 1, 2, ..} or -1.
```bash
  python rc/main.py --trainset data/coqa.train.pipeline.json --devset data/coqa.dev.pipeline.json --n_history 2 --dir pipeline_models --embed_file wordvecs/glove.840B.300d.txt --predict_raw_text n
  python seq2seq/train.py -data data/seq2seq-pipeline -save_model pipeline_models/seq2seq_copy -copy_attn -reuse_copy_attn -word_vec_size 300 -pre_word_vecs_enc data/seq2seq-pipeline.embed.enc.pt -pre_word_vecs_dec data/seq2seq-pipeline.embed.dec.pt -epochs 50 -gpuid 0 -seed 123
```

### Testing
```bash
  python rc/main.py --testset data/coqa.dev.pipeline.json --n_history 2 --pretrained pipeline_models
  python scripts/gen_pipeline_for_seq2seq.py --data_file data/coqa.dev.pipeline.json --output_file pipeline_models/pipeline-seq2seq-src.txt --pred_file pipeline_models/predictions.json
  python seq2seq/translate.py -model pipeline_models/seq2seq_copy_acc_85.00_ppl_2.18_e16.pt -src pipeline_models/pipeline-seq2seq-src.txt -output pipeline_models/pred.txt -replace_unk -verbose -gpu 0
  python scripts/gen_seq2seq_output.py --data_file data/coqa-dev-v1.0.json --pred_file pipeline_models/pred.txt --output_file pipeline_models/pipeline.prediction.json
```

## Results

All the results are based on `n_history = 2`:

| Model  | Dev F1 | Dev EM |
| ------------- | ------------- | ------------- |
| seq2seq | 20.9 | 17.7 |
| seq2seq_copy  | 45.2  | 38.0 |
| DrQA | 55.6 | 46.2 |
| pipeline | 65.0 | 54.9 |

## Citation

```
    @article{reddy2019coqa,
      title={{CoQA}: A Conversational Question Answering Challenge},
      author={Reddy, Siva and Chen, Danqi and Manning, Christopher D},
      journal={Transactions of the Association of Computational Linguistics (TACL)},
      year={2019}
    }
```

## License
MIT
