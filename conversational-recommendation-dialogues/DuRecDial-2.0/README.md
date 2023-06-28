# DuRecDial

In this paper, we provide a **bilingual parallel** human-to-human recommendation dialog dataset, **DuRecDial 2.0**, to enable researchers to explore the challenging task of multilingual and cross-lingual conversational recommendation. The difference between DuRecDial 2.0 and existing conversational recommendation datasets is that the data item (Profile, Goal, Knowledge, Context, Response) in DuRecDial 2.0 is annotated in two languages, both English and Chinese, while other datasets are built with the setting of a single language. We collect **8.2k** dialogues aligned across English and Chinese languages (16.5k dialogs and 255k utterances in total) that are annotated by crowdsourced workers with strict quality control procedure. DuRecDial 2.0 provides a challenging testbed for future studies of monolingual, multilingual, and cross-lingual conversational recommendation. For a detailed introduction of DuRecDial 2.0, please refer to [DuRecDial](https://github.com/liuzeming01/Research/tree/master/NLP/ACL2020-DuRecDial) on [IEEE Xplore](https://ieeexplore.ieee.org/document/9699426), [ACL Anthology](https://aclanthology.org/2020.acl-main.98/) and [arXiv](https://arxiv.org/abs/2005.03954).

Our paper on [ACL Anthology](https://aclanthology.org/2021.emnlp-main.356/) and [arXiv](https://arxiv.org/abs/2109.08877) . If the corpus is helpful to your research, please kindly cite our paper:

```bib
@inproceedings{liu-etal-2021-durecdial,
    title = "{D}u{R}ec{D}ial 2.0: A Bilingual Parallel Corpus for Conversational Recommendation",
    author = "Liu, Zeming  and
      Wang, Haifeng  and
      Niu, Zheng-Yu  and
      Wu, Hua  and
      Che, Wanxiang",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.356",
    doi = "10.18653/v1/2021.emnlp-main.356",
    pages = "4335--4347",
}
```

## Data

**Note:If the first goal is "Greetings/寒暄", the seeker starts the conversation, otherwise, the user starts the conversation.**

An example of the conversation in DuRecDial 2.0:

![example](figs/example8-1.png)

DuRecDial 2.0 is an extension of the [DuRecDial](https://baidu-nlp.bj.bcebos.com/DuRecDial.zip). Specifically, we extend the DuRecDial to English by crowdsourced workers with strict quality control procedure.

If DuRecDial is helpful to your research, please kindly cite our papers:

```bib
@inproceedings{liu-etal-2020-towards-conversational,
    title = "Towards Conversational Recommendation over Multi-Type Dialogs",
    author = "Liu, Zeming  and
      Wang, Haifeng  and
      Niu, Zheng-Yu  and
      Wu, Hua  and
      Che, Wanxiang  and
      Liu, Ting",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.acl-main.98",
    doi = "10.18653/v1/2020.acl-main.98",
    pages = "1036--1049",
}
```
```bib
@ARTICLE{9699426,
  author={Liu, Zeming and Zhou, Ding and Liu, Hao and Wang, Haifeng and Niu, Zheng-Yu and Wu, Hua and Che, Wanxiang and Liu, Ting and Xiong, Hui},
  journal={IEEE Transactions on Knowledge and Data Engineering}, 
  title={Graph-Grounded Goal Planning for Conversational Recommendation}, 
  year={2023},
  volume={35},
  number={5},
  pages={4923-4939},
  doi={10.1109/TKDE.2022.3147210}
  }
```


## License

Apache License 2.0 and CC BY-NC-SA 4.0.

Since DuRecDial 2.0 is licensed under CC BY-NC-SA 4.0. Note the dataset may not be adopted for commercial use.
