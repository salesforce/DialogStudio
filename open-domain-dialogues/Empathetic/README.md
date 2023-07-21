# EmpatheticDialogues

PyTorch original implementation of Towards Empathetic Open-domain Conversation Models: a New Benchmark and Dataset (https://arxiv.org/abs/1811.00207).

We provide a novel dataset of 25k conversations grounded in emotional situations. The code in this repo demonstrates that automated metrics (P@1,100 and BLEU) are improved both when using candidates from our dataset and when fine-tuning on it.

## Dataset

To download the EmpatheticDialogues dataset:

```
wget https://dl.fbaipublicfiles.com/parlai/empatheticdialogues/empatheticdialogues.tar.gz
```

## References

Please cite [[1]](https://arxiv.org/abs/1811.00207) if you found the resources in this repository useful.

### Towards Empathetic Open-domain Conversation Models: a New Benchmark and Dataset

[1] H. Rashkin, E. M. Smith, M. Li, Y. Boureau [*Towards Empathetic Open-domain Conversation Models: a New Benchmark and Dataset*](https://arxiv.org/abs/1811.00207)

```
@inproceedings{rashkin2019towards,
  title = {Towards Empathetic Open-domain Conversation Models: a New Benchmark and Dataset},
  author = {Hannah Rashkin and Eric Michael Smith and Margaret Li and Y-Lan Boureau},
  booktitle = {ACL},
  year = {2019},
}
```