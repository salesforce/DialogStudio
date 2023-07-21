<p align="center">
    <br>
    <img src="figures/logo.png" width="510"/>
    <br>
<!-- <p>
<div align="center"> -->
<a href="https://arxiv.org/abs/2307.10172" style="font-size:20px;">Paper</a>,
<a href="#datasets" style="font-size:20px;">Datasets</a>,
<a href="#documentation" style="font-size:20px;">Documentation</a>,
<a href="#model" style="font-size:20px;">Model</a>,
<a href="https://twitter.com/CaimingXiong/status/1674123308177178624" style="font-size:20px;">Twitter</a> 
<!-- </div> -->
 <p>

# DialogStudio: Towards Richest and Most Diverse Unified Dataset Collection for Conversational AI



### Datasets
<!-- Check [DialogStudio_datasets.csv](https://docs.google.com/spreadsheets/d/10U9I4GoHFTYxl3OlzbbV0gmXerMT9Itn2MZs8t6AIK0/edit#gid=461625820) for all supported datasets. -->
The figure below provides a summary of the general statistics associated with DialogStudio. DialogStudio unified each dataset while preserving their original information, and this aids in supporting research on both individual datasets and Large Language Model (LLM) training. 

For more granular and category-specific details, please refer to the individual folders corresponding to each category within the DialogStudio collection. 
<p align="center">
    <br>
    <img src="figures/DialogStudio_Stats.png" width="730"/>
    <br>
<p>

DialogStudio evaluates dialogue quality based on six critical criteria, namely Understanding, Relevance, Correctness, Coherence, Completeness, and Overall Quality. Each criterion is scored on a scale of 1 to 5, with the highest scores reserved for exceptional dialogues.

Given the vast number of datasets incorporated into DialogStudio, we utilized 'gpt-3.5-turbo' to assess 33 distinct datasets. The corresponding script used for this evaluation can be accessed through the [link](https://github.com/salesforce/DialogStudio/blob/main/code/openai_dialog_quality_evaluation.py). 

The results of our dialogue quality assessment are presented below. We intend to release evaluation scores for individual selected dialogues in the upcoming period.
<p align="center">
    <br>
    <img src="figures/DialogStudio_Quality_Scores.png" width="750"/>
    <br>
<p>

### Documentation
The datasets are split into several categories in this GitHub repository and [HuggingFace hub](https://huggingface.co/datasets/Salesforce/dialogstudio). You can check each category folder and each dataset folder for specific information.

```
Datasets/
├── Knowledge-Grounded-Dialogues
├── Natural-Language-Understanding
├── Open-Domain-Dialogues
├── Task-Oriented-Dialogues
├── Dialogue-Summarization
├── Conversational-Recommendation-Dialogs
```



### Load dataset


You can load any dataset in the DialogStudio from the [HuggingFace hub](https://huggingface.co/datasets/Salesforce/dialogstudio) by claiming the `{dataset_name}`.

Below is one example to load the MULTIWOZ_2_2 dataset:


```python
from datasets import load_dataset

dataset = load_dataset('Salesforce/dialogstudio', 'MULTIWOZ_2_2')
```
Here is the output structure of MultiWOZ 2.2
```python
DatasetDict({
    train: Dataset({
        features: ['original dialog id', 'new dialog id', 'dialog index', 'original dialog info', 'log', 'prompt', 'external knowledge non-flat', 'external knowledge', 'dst knowledge', 'intent knowledge'],
        num_rows: 8437
    })
    validation: Dataset({
        features: ['original dialog id', 'new dialog id', 'dialog index', 'original dialog info', 'log', 'prompt', 'external knowledge non-flat', 'external knowledge', 'dst knowledge', 'intent knowledge'],
        num_rows: 1000
    })
    test: Dataset({
        features: ['original dialog id', 'new dialog id', 'dialog index', 'original dialog info', 'log', 'prompt', 'external knowledge non-flat', 'external knowledge', 'dst knowledge', 'intent knowledge'],
        num_rows: 1000
    })
})
```

# Model
We've rolled out version 1.0 of models trained on a few selected DialogStudio datasets. Built on small-scale pre-trained models, this version does not incorporate datasets utilized for training large-scale models (>=7B) like Alpaca, ShareGPT, GPT4ALL, UltraChat from OpenAI's 'GPT-3.5/4', or other datasets such as OASST1 and WizardCoder (Note that DialogStudio has unified such datasets).  As a result, it has certain limitations in terms of writing and creative capabilities. Our initial focus is to update the model versions to enhance existing abilities. Further improvements, including expansion of other capabilities, are part of our roadmap and will be responsive to community requests.

# Contributing
We enthusiastically invite contributions from the community! Join us in our shared mission to propel the field of conversational AI forward!



# License

Our project follows the following structure with respect to licensing:

1. For all the modified datasets in DialogStudio: 
   - A portion of these datasets is under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
   - Some retain their original licenses even after modification.
   - For a few datasets that lacked a license, we have cited the relevant papers.
2. Original dataset licenses: For reference, we also put the original available licenses for each dataset into their respective dataset folders.
3. Code: Our codebase is under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

For detailed licensing information, please refer to the specific licenses accompanying the datasets. It is important to familiarize yourself with these terms as we do not assume responsibility for licensing issues.

# Citation
The data and code in this repository is mostly developed for or derived from the paper below. If you utilize datasets from DialogStudio, we kindly request that you cite both the original work and our own.

```
@misc{zhang2023dialogstudio,
      title={DialogStudio: Towards Richest and Most Diverse Unified Dataset Collection for Conversational AI}, 
      author={Jianguo Zhang and Kun Qian and Zhiwei Liu and Shelby Heinecke and Rui Meng and Ye Liu and Zhou Yu and and Huan Wang and Silvio Savarese and Caiming Xiong},
      year={2023},
      eprint={2307.10172},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```