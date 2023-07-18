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

**--Note--:** More contents will be added soon after passing internal legal review process. 

### Datasets
<!-- Check [DialogStudio_datasets.csv](https://docs.google.com/spreadsheets/d/10U9I4GoHFTYxl3OlzbbV0gmXerMT9Itn2MZs8t6AIK0/edit#gid=461625820) for all supported datasets. -->
Below figure shows the general DialogStudio statistics. Please refer the folder of each category for more details.
<p align="center">
    <br>
    <img src="figures/DialogStudio_Stats.png" width="700"/>
    <br>
<p>



### Load dataset
The datasets are split into several categories in HuggingFace 
```
Datasets/
├── Knowledge-Grounded-Dialogues
├── Natural-Language-Understanding
├── Open-Domain-Dialogues
├── Task-Oriented-Dialogues
├── Dialogue-Summarization
├── Conversational-Recommendation-Dialogs
```

You can load any dataset in the DialogStudio from the HuggingFace hub by claiming the `{dataset_name}`. Below is one example to load the CoSQL dataset:

```python
from datasets import load_dataset

dataset = load_dataset("qbetterk/dialogstudio", 'CoSQL')
```
Here is the output structure of CoSQL
```python
DatasetDict({
    train: Dataset({
        features: ['original dialog id', 'dialog index', 'original dialog info', 'log', 'key'],
        num_rows: 4318
    })
    validation: Dataset({
        features: ['original dialog id', 'dialog index', 'original dialog info', 'log', 'key'],
        num_rows: 4904
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
