# DART: Open-Domain Structured Data Record to Text Generation

DART is a large and open-domain structured **DA**ta **R**ecord to **T**ext generation corpus with high-quality sentence annotations with each input being a set of entity-relation triples following a tree-structured ontology.
It consists of 82191 examples across different domains with each input being a semantic triple set derived from data records in tables and the tree ontology of table schema, annotated with sentence description that covers all facts in the triple set.

DART is described with more details and baseline results in this [paper](https://aclanthology.org/2021.naacl-main.37/).

## Data Content and Format
The DART dataset is available in the `data/v1.1.1/` directory. The dataset consists of a JSON version and a XML version of train/dev/test files in `data/`. 

Each JSON file contains a list of tripleset-annotation pairs of the form:
```
  {
    "tripleset": [
      [
        "Ben Mauk",
        "High school",
        "Kenton"
      ],
      [
        "Ben Mauk",
        "College",
        "Wake Forest Cincinnati"
      ]
    ],
    "subtree_was_extended": false,
    "annotations": [
      {
        "source": "WikiTableQuestions_lily",
        "text": "Ben Mauk, who attended Kenton High School, attended Wake Forest Cincinnati for college."
      }
    ]
  }
```
Each XML file contains a list tripleset-lex pairs of the form:
```
  <entry category="MISC" eid="Id1" size="2">
    <modifiedtripleset>
      <mtriple>Mars Hill College | JOINED | 1973</mtriple>
      <mtriple>Mars Hill College | LOCATION | Mars Hill, North Carolina</mtriple>
    </modifiedtripleset>
    <lex comment="WikiSQL_decl_sents" lid="Id1">A school from Mars Hill, North Carolina, joined in 1973.</lex>
  </entry>
```

You can use `data/v1.1.1/select_partitions.py` to generate dataset that contains different partitions of DART, and note that different partitions have different sources of annotation. Specifically we have the following sources of annotation:
* `WikiTableQuestions_lily`, `WikiSQL_lily` ⇒ Instances that are manually annotated by internal annotators
* `WikiTableQuestions_mturk` ⇒ Instances that are manually annotated by MTurk workers
* `WikiSQL_decl_sents` ⇒ Instances that are automatically annotated by a procedure described in Sec 2.2 of our [paper](https://arxiv.org/abs/2007.02871)
* `webnlg`, `e2e` ⇒ Instances obtained by converting existing datasets, these partitions are less open-domained

In addition, we provide 4 settings of generating dataset for your research purpose:
* `manual`: this setting includes all manually annotated instances
* `manual_and_auto`: this setting includes both manually and automatically annotated instances, but excluding `webnlg` and `e2e` which are less open-domained partitions
* `full`: this setting includes all partitions of DART
* `custom`: you can choose any combination of partitions

## Models
We also provide implementations we use to produce results in our paper. Please refer to `model/` for more information.

## Leaderboard

We maintain a leaderboard on our test set.

<table style='font-size:80%'>
  <tr>
    <th>Model</th>
    <th>BLEU</th>
    <th>METEOR</th>
    <th>TER</th>
    <th>MoverScore</th>
    <th>BERTScore</th>
    <th>BLEURT</th>
    <th>PARENT</th>
  </tr>
  <tr>
    <td> Control Prefixes (T5-large) <a href="https://arxiv.org/pdf/2110.08329.pdf"> (Clive et al., 2021) </a></td>
    <td><b>51.95</b></td>
    <td><b>0.41</b></td>
    <td><b>0.43</b></td>
    <td><b>-</b></td>
    <td><b>0.95</b></td>
    <td><b>-</b></td>
    <td><b>-</b></td>
  </tr>
  <tr>
    <td> T5-large <a href="https://arxiv.org/pdf/1910.10683.pdf"> (Raffel et al., 2020) </a></td>
    <td><b>50.66</b></td>
    <td><b>0.40</b></td>
    <td><b>0.43</b></td>
    <td><b>0.54</b></td>
    <td><b>0.95</b></td>
    <td><b>0.44</b></td>
    <td><b>0.58</b></td>
  </tr>
  <tr>
    <td> BART-large <a href="https://arxiv.org/pdf/1910.13461.pdf"> (Lewis et al., 2020) </a></td>
    <td> 48.56 </td>
    <td> 0.39 </td>
    <td> 0.45 </td>
    <td> 0.52 </td>
    <td> 0.95 </td>
    <td> 0.41 </td>
    <td> 0.57 </td>
  </tr>
  <tr>
    <td> Seq2Seq-Att <a href="https://webnlg-challenge.loria.fr/files/melbourne_report.pdf"> (MELBOURNE) </a></td>
    <td> 29.66 </td>
    <td> 0.27 </td>
    <td> 0.63 </td>
    <td> 0.31 </td>
    <td> 0.90 </td>
    <td> -0.13 </td>
    <td> 0.35 </td>
  </tr>
  <tr>
    <td> End-to-End Transformer <a href="https://arxiv.org/pdf/1908.09022.pdf"> (Castro Ferreira et al., 2019) </a></td>
    <td> 27.24 </td>
    <td> 0.25 </td>
    <td> 0.65 </td>
    <td> 0.25 </td>
    <td> 0.89 </td>
    <td> -0.29 </td>
    <td> 0.28 </td>
  </tr>
</table>

## Citation
```
@inproceedings{nan-etal-2021-dart,
    title = "{DART}: Open-Domain Structured Data Record to Text Generation",
    author = "Nan, Linyong  and
      Radev, Dragomir  and
      Zhang, Rui  and
      Rau, Amrit  and
      Sivaprasad, Abhinand  and
      Hsieh, Chiachun  and
      Tang, Xiangru  and
      Vyas, Aadit  and
      Verma, Neha  and
      Krishna, Pranav  and
      Liu, Yangxiaokang  and
      Irwanto, Nadia  and
      Pan, Jessica  and
      Rahman, Faiaz  and
      Zaidi, Ahmad  and
      Mutuma, Mutethia  and
      Tarabar, Yasin  and
      Gupta, Ankit  and
      Yu, Tao  and
      Tan, Yi Chern  and
      Lin, Xi Victoria  and
      Xiong, Caiming  and
      Socher, Richard  and
      Rajani, Nazneen Fatema",
    booktitle = "Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
    month = jun,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.naacl-main.37",
    doi = "10.18653/v1/2021.naacl-main.37",
    pages = "432--447",
    abstract = "We present DART, an open domain structured DAta Record to Text generation dataset with over 82k instances (DARTs). Data-to-text annotations can be a costly process, especially when dealing with tables which are the major source of structured data and contain nontrivial structures. To this end, we propose a procedure of extracting semantic triples from tables that encodes their structures by exploiting the semantic dependencies among table headers and the table title. Our dataset construction framework effectively merged heterogeneous sources from open domain semantic parsing and spoken dialogue systems by utilizing techniques including tree ontology annotation, question-answer pair to declarative sentence conversion, and predicate unification, all with minimum post-editing. We present systematic evaluation on DART as well as new state-of-the-art results on WebNLG 2017 to show that DART (1) poses new challenges to existing data-to-text datasets and (2) facilitates out-of-domain generalization. Our data and code can be found at https://github.com/Yale-LILY/dart.",
}
```

