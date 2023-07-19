<p align="center">
    <br>
    <img src="figures/logo.png" width="500"/>
    <br>
<p>
<!-- <div align="center">
<a href="">Benchmark</a>,
<a href="">Technical Report</a>,
<a href="">Documentation</a>,
<a href="">Jupyter Notebook Examples</a>,
<a href="">Blog</a>
</div> -->

# DialogStudio: Unified Dialog Datasets and Instruction-Aware Models for Conversational AI


### Datasets
<!-- Check [DialogStudio_datasets.csv](https://docs.google.com/spreadsheets/d/10U9I4GoHFTYxl3OlzbbV0gmXerMT9Itn2MZs8t6AIK0/edit#gid=461625820) for all supported datasets. -->
Below figure shows the general DialogStudio statistics. Please refer the folder of each category for more details.
<p align="center">
    <br>
    <img src="figures/DialogStudio_Stats.png" width="700"/>
    <br>
<p>

The datasets are split into several categories in this GitHub repository and [HuggingFace hub](https://huggingface.co/datasets/Salesforce/dialogstudio)
```
Datasets/
├── Knowledge-Grounded-Dialogues
├── Natural-Language-Understanding
├── Open-Domain-Dialogues
├── Task-Oriented-Dialogues
├── Dialogue-Summarization
├── Conversational-Recommendation-Dialogs
```

We assess dialogue quality based on six criterias, i.e., Understanding, Relevance, Correctness, Coherence, Completeness and Overall quality. The score is from range 1-5, and higher score only gives to exceptional dialogues. Since there are a lots of datasets in DialogStudio, we employ `gpt-3.5-turbo` to evaluate 33 datasets, and[dialog_quality_evaluation.py](https://github.com/salesforce/DialogStudio/blob/main/code/openai_dialog_quality_evaluation.py) shows the corresponding script. 

DialogStudio evaluates dialogue quality based on six critical criteria, namely Understanding, Relevance, Correctness, Coherence, Completeness, and Overall Quality. Each criterion is scored on a scale of 1 to 5, with the highest scores reserved for exceptional dialogues.

Given the vast number of datasets incorporated into DialogStudio, we utilized 'gpt-3.5-turbo' to assess 33 distinct datasets. The corresponding script used for this evaluation can be accessed through the [link](https://github.com/salesforce/DialogStudio/blob/main/code/openai_dialog_quality_evaluation.py)

The results of our dialogue quality assessment are presented below. 
<p align="center">
    <br>
    <img src="figures/DialogStudio_Quality_Scores.png" width="700"/>
    <br>
<p>

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

# License

Our project follows the following structure with respect to licensing:

1. For all the modified datasets in DialogStudio: 
   - A portion of these datasets is under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
   - Some retain their original licenses even after modification.
   - For a few datasets that lacked a license, we have cited the relevant papers.
2. Original dataset licenses: For reference, we also put the original avaliable licenses for each dataset into their respective dataset folders.
3. Code: Our codebase is under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

For detailed licensing information, please refer to the specific licenses accompanying the datasets. If you utilize datasets from DialogStudio, we kindly request that you cite our work.
