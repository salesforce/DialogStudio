<p align="center">
    <br>
    <img src="figures/logo.png" width="500"/>
    <br>
<p>
<div align="center">
<a href="">Benchmark</a>,
<a href="">Technical Report</a>,
<a href="">Documentation</a>,
<a href="">Jupyter Notebook Examples</a>,
<a href="">Blog</a>
</div>

# DialogStudio: Unified Dialog Datasets and Instruction-Aware Models for Conversational AI

**Note:** More contents will be added soon after passing internal review. 

### Datasets
Check [DialogStudio_datasets.csv](https://docs.google.com/spreadsheets/d/10U9I4GoHFTYxl3OlzbbV0gmXerMT9Itn2MZs8t6AIK0/edit#gid=461625820) for all supported datasets.

<p align="center">
    <br>
    <img src="figures/DialogStudio_Stats.png" width="700"/>
    <br>
<p>


Data Structure
```
Datasets/
├── Task-Oriented:
│   ├── KVRET
│   ├── MuDoCo
│   ├── AirDialogue
│   ├── DuRecDial-2.0
│   ├── SimJointGEN
│   ├── BiTOD
│   ├── DSTC2-Clean
│   ├── OpenDialKG
│   ├── Taskmaster1
│   ├── Taskmaster2
│   ├── Taskmaster3
│   ├── CaSiNo
│   ├── HDSA-Dialog
│   ├── MetaLWOZ
│   ├── FRAMES
│   ├── MULTIWOZ2_2
│   ├── SalesBot
│   ├── STAR
│   ├── ABCD
│   ├── SGD
│   ├── WOZ2_0
│   ├── CraigslistBargains
│   ├── MulDoGO
│   ├── SimJointMovie
│   ├── SimJointRestaurant
│   └── SimJointGEN
dialog-summarization
│   ├── AMI
│   ├── ConvoSumm
│   ├── DialogSum
│   ├── ICSI
│   ├── MediaSum
│   ├── QMSum
│   ├── SAMSum
│   ├── SummScreen_ForeverDreaming
│   ├── SummScreen_TVMegaSite
│   ├── TweetSumm
│   └── ECTSum
│   └── CRD3


```

# License

Our project follows the following structure with respect to licensing:

1. For all the modified datasets in DialogStudio: 
   - A portion of these datasets is under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
   - Some retain their original licenses even after modification.
   - For a few datasets that lacked a license, we have cited the relevant papers.
2. Original dataset licenses: For reference, we also put the original avaliable licenses for each dataset into their respective dataset folders.
3. Code: Our codebase is under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

For detailed information, please refer to the specific licenses.
