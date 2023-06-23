# QMSum

### Overview
This repository maintains dataset for NAACL 2021 paper: *[QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization](https://arxiv.org/abs/2104.05938)*.

**QMSum** is a new human-annotated benchmark for query-based multi-domain meeting summarization task, which consists of 1,808 query-summary pairs over 232 meetings in multiple domains.

If you use our dataset, please limit it to research purposes and cite our paper.

### Dataset
You can access the train/valid/test set of QMSum through the ```data/ALL``` folder. In addition, QMSum is composed of three domains: ```data/Academic```, ```data/Product``` and ```data/Committee``` contain data in a single domain.

Files in each folder:

* ```jsonl```: data in .jsonl format.
* ```all```: all data in .json format.
* ```train```: training data.
* ```val```: validation data.
* ```test```: test data.

The format of json data is as follows:

```
{
    "topic_list": [
        {
            "topic": "Introduction of petitions and prioritization of governmental matters",
            "relevant_text_span": [["0","19"]]
        },
        {
            "topic": "Financial assistance for vulnerable Canadians during the pandemic and beyond",
            "relevant_text_span": [["21","57"], ["113","119"], ["191","217"]]
        },
        ...
    ],
    "general_query_list": [
        {
            "query": "Summarize the whole meeting.",
            "answer": "The meeting of the standing committee took place to discuss matters pertinent to the Coronavirus pandemic. The main issue at stake was to ..."
        },
        ...
    ],
    "specific_query_list": [
        {
            "query": "Summarize the discussion about introduction of petitions and prioritization of government matters.",
            "answer": "The Chair brought the meeting to order, announcing that the purpose of the meeting was to discuss COVID-19 's impact on Canada. Five petitions were presented ...",
            "relevant_text_span": [["0","19"]]
        },
	{
            "query": "What did Paul-Hus think about the introduction of petitions and prioritization of government matters?",
            "answer": "Mr. Paul-Hus thought that the government should not take firearms away from law-abiding Canadian citizens. He inquired into ...",
            "relevant_text_span": [["9","18"]]
        },
        ...
    ],
    "meeting_transcripts": [
        {
            "speaker": "The Chair (Hon. Anthony Rota (NipissingTimiskaming, Lib.))",
            "content": "I call the meeting to order.  Welcome to the third meeting of the House of Commons Special Committee on the COVID-19 Pandemic ..."
        },
        {
            "speaker": "Mr. Garnett Genuis (Sherwood ParkFort Saskatchewan, CPC)",
            "content": "Mr. Chair, I'm pleased to be presenting two petitions today. The first petition is with respect to government Bill C-7 ..."
        },
        ...
	{
            "speaker": "Hon. Seamus O'Regan",
            "content": "Mr. Chair, we have been working with our provincial partners. We have been working with businesses of all sizes in the oil and gas industry ...."
        },
        {
            "speaker": "The Chair",
            "content": "That's all the time we have for questions today. I want to thank all the members for taking part. The committee stands adjourned until tomorrow at noon.  The committee stands adjourned until tomorrow at noon. Thank you."
        }
    ]
}
```
Please note that there may be multiple relevant text spans for a topic or a specific query. The general query has no corresponding text spans because it corresponds to the entire meeting transcript.

### Data Processing
We provide a notebook to convert our data into the format required by some seq2seq models like BART or PGNet. For details, see ```data_process.ipynb```. Besides, we set the maximum source length during training to 2048 for these two models.

### Models
We run many popular models in this paper. Here we provide the code that can be used to implement each model.

For our Locator, we use the code from [this link](https://github.com/maszhongming/Effective_Extractive_Summarization). Notably, we find that removing Transformers in Locator has little impact on performance, so the Locator without Transformer is used in all the experiments.

For PGNet, you can refer to the implementation of the original paper [here](https://github.com/abisee/pointer-generator).

For BART, we use the interface provided by [fairseq](https://github.com/pytorch/fairseq/blob/master/examples/bart/README.summarization.md), of course you can also refer to the implementation of [transformers](https://github.com/huggingface/transformers/tree/master/examples/pytorch/summarization).

For HMNet, please use the official implementation [here](https://github.com/microsoft/HMNet).

### Extracted Span
The spans extracted by our Locator as the input of the Summarizer can be found in ```/extracted_span```.

### Model Outputs
We provide the summary generated by HMNet (with golden input) in ```/model_output```. The ROUGE score of this output is 36.51/11.41/31.60 (R-1/R-2/R-L).

### Statistics
<p align="justify">
  <img src="https://github.com/Yale-LILY/QMSum/blob/main/figures/Statistics.jpg" alt="statistics">
</p>

### Experimental Results
<p align="center">
  <img src="https://github.com/Yale-LILY/QMSum/blob/main/figures/Experimental%20Results.jpg" width="350" alt="statistics">
</p>

### Citation
```
@inproceedings{zhong2021qmsum,
   title={{QMS}um: {A} {N}ew {B}enchmark for {Q}uery-based {M}ulti-domain {M}eeting {S}ummarization},
   author={Zhong, Ming and Yin, Da and Yu, Tao and Zaidi, Ahmad and Mutuma, Mutethia and Jha, Rahul and Hassan Awadallah, Ahmed and Celikyilmaz, Asli and Liu, Yang and Qiu, Xipeng and Radev, Dragomir},
   booktitle={North American Association for Computational Linguistics (NAACL)},
   year={2021}
}
```
