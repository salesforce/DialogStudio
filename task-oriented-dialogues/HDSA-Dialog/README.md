# HDSA-Dialog
This is the code and data for ACL 2019 long paper "Semantically Conditioned Dialog Response Generation via Hierarchical Disentangled Self-Attention". The up-to-date version is in [http://arxiv.org/abs/1905.12866](http://arxiv.org/abs/1905.12866).

The full architecture is displayed as below:
<p>
<img src="resource/full_architecture.png" width="800">
</p>

The architecture consists of two components:
- Dialog act predictor (Fine-tuned BERT model)
- Response generator (Hierarchical Disentangled Self-Attention Network)

The basic idea of the paper is to do enable controlled reponse generation under the Transformer framework, where we construct a dialog act graph to represent the semantic space in MultiWOZ tasks. Then we particularly specify different heads in different levels to a specific node in the dialog act graph. For example, the picture above demonstrates the merge of two dialog acts "hotel->inform->location" and "hotel->inform->name". The generated sentence is controlled to deliever message about the name and location of a recommended hotel. 

## Requirements
- Python 3.5
- [Pytorch 1.0](https://pytorch.org/)
- [Pytorch-pretrained-BERT](https://github.com/huggingface/pytorch-pretrained-BERT)

Please see the instructions to install the required packages before running experiments.

## Folder
- data: all the needed training/evaluation/testing data
- transformer: all the baseline and proposed models, which include the hierarchical disentangled self-attention (class TableSemanticDecoder)
- preprocessing: the code for pre-processing the database and original downloaded data

## 1. Dialog Act Predictor
This module is used to predict the next-step dialog acts based on the conversation history. Here we adopt the state-of-the-art NLU module [BERT](https://arxiv.org/abs/1810.04805) to get the best prediction accuracy. Make sure that you install the [Pytorch-pretrained-BERT](https://github.com/huggingface/pytorch-pretrained-BERT) beforehand, which will automatically download pre-trained model into your tmp folder.
### Download pre-trained models and the delex.json (it is needed for calculating the inform/request success rate)
```
sh collect_data.sh
```
###
### Prepare data (optional, already in the github repo)
```
python preprocess_data_for_predictor.py
```
### Training (if you use multiple GPU, the batch size can be enlarged)
```
rm -r checkpoints/predictor/
CUDA_VISIBLE_DEVICES=0 python3.5 train_predictor.py --do_train --do_eval --train_batch_size 6 --eval_batch_size 6
```
### Testing (using the model saved at xxx step)
```
CUDA_VISIBLE_DEVICES=0 python3.5 train_predictor.py --do_eval --test_set dev --load_dir /tmp/output/save_step_xxx
CUDA_VISIBLE_DEVICES=0 python3.5 train_predictor.py --do_eval --test_set test --load_dir /tmp/output/save_step_xxx
```
The output values are saved in data/BERT_dev_prediction.json and data/BERT_dev_prediction.json, these two files need to be kept for the generator training.

## 2. Response Generator
This module is used to control the language generation based on the output of the pre-trained act predictor. The training data is already preprocessed and put in data/ folder (train.json, val.json and test.json).
### Training
```
CUDA_VISIBLE_DEVICES=0 python3.5 train_generator.py --option train --model BERT_dim128_w_domain_exp --batch_size 512 --max_seq_length 50 --field
```
### Delexicalized Testing (The entities are normalzied into placeholder like [restaurant_name])
```
CUDA_VISIBLE_DEVICES=0 python3.5 train_generator.py --option test --model BERT_dim128_w_domain_exp --batch_size 512 --max_seq_length 50 --field
```

### Non-Delexicalized Testing (The entities need to be restored from the database record)
```
CUDA_VISIBLE_DEVICES=0 python3.5 train_generator.py --option postprocess --output_file /tmp/results.txt.pred.BERT_dim128_w_domain_exp.pred --model BERT --non_delex
```

## 3. Reproducibility
- We release the pre-trained predictor model in checkpoints/predictor, you can put the zip file into checkpoints/predictor and unzip it to get the save_step_15120 folder.
```
CUDA_VISIBLE_DEVICES=0 python3.5 train_predictor.py --do_eval --test_set test --load_dir /tmp/output/save_step_15120
```
- We already put the pre-trained generator model under checkpoints/generator, you can use this model to obtain 23.6 BLEU on the delexicalized test set.
```
CUDA_VISIBLE_DEVICES=0 python3.5 train_generator.py --option test --model BERT_dim128_w_domain --batch_size 512 --max_seq_length 50 --field
CUDA_VISIBLE_DEVICES=0 python3.5 train_generator.py --option postprocess --output_file /tmp/results.txt.pred.BERT_dim128_w_domain.pred --model BERT --non_delex
```

## Acknowledgements
We sincerely thank University of Cambridge and PolyAI for releasing the dataset and [code](https://github.com/budzianowski/multiwoz)
