# Intro
This project contains natural language data for human-robot interaction in home domain which we collected and annotated for evaluating NLU Services/platforms.

If you use the data and publish the results please let us know and cite our [IWSDS 2019 paper](https://iwsds2019.unikore.it/program/):
#### (It is also available at [arXiv](https://arxiv.org/abs/1903.05566).)

```
@InProceedings{XLiu.etal:IWSDS2019,
  author    = {Xingkun Liu, Arash Eshghi, Pawel Swietojanski and Verena Rieser},
  title     = {Benchmarking Natural Language Understanding Services for building Conversational Agents},
  booktitle = {Proceedings of the Tenth International Workshop on Spoken Dialogue Systems Technology (IWSDS)},
  month     = {April},
  year      = {2019},
  address   = {Ortigia, Siracusa (SR), Italy},
  publisher = {Springer},
  pages     = {xxx--xxx},
  url       = {http://www.xx.xx/xx/}
}

```

## License
All data are released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You should have received a copy of the license along with this dataset. If not, see <http://creativecommons.org/licenses/by/4.0/>.


## Content
It contains

1. Collected-Original-Data (25K):  collected original data with normalization for numbers/date etc which contain the pre-designed human-robot interaction questions and the user answers. They are organized in CSV format.

2. AnnotatedData (25716 Lines): annotated for Intents and Entities, organized in csv format.

    The annotated csv file has following columns:
    userid, answerid, scenario, intent, status, answer_annotation, notes, suggested_entities,    answer_normalised, answer, question<br/>

    Most of them come from the original data collection, we keep them here for monitoring of
    the afterwards processing. 

    "answer" contains the original user answers.<br/>
    "answer_normalised" were normalised from "answer".<br/> 
    "notes" was used for the annotators. They put some notes there if they have changed anything.<br/>
    "status" was used for annotation and post processing. The utterance will be ignored by the post processing scripts if the column content starts with 'IRR_'.<br/>
    "answer_annotation" contains the annotated results, it will be used for generating the train/test datasets, along with "scenario", "intent" and "status".<br/>

3. The 10-fold cross-validation we used (here for reference only)

4. The Annotation Guidelines

    The uploaded annotation guidelines were used when we did the dataset annotations. They were based on our dataset originally designed and collected in the CSV format. Our processing scripts were also based on the same CSV format.

    You could use ( or convert them to) different formats as you like, e.g. the Markdown format.


  #### NB: The CSV file uses Semicolon(;) as the field/column delimiter! It may mess up with the data if using Colon(,).

CrossValidation contains the generated data for different NLU services we used for our evaluations which are uploaded here for reference only as they can be generated from the annotated csv data using our scripts. NB: the script will shuffle the data each time when runing the script, so the generated data may not be exact the same each time.


autoGeneFromRealAnno/: generated trainset and testset from the annotated csv file.
The other four subdirectories (out4ApiaiReal, out4LuisReal, out4RasaReal and out4WatsonReal) in CrossValidation/ are the converted NLU service input data for Dialogflow, LUIS, Rasa and Watson respectively. The inside 'merged' directory contains the trainning input data.


## Scripts for the Data Preparation and Evaluation
Java for preparing the data, evaluating the performances and Python scripts for querying the Services/Platforms are [Here](https://github.com/xliuhw/NLU-Evaluation-Scripts)

## Contact
Please contact x.liu@hw.ac.uk, if you have any questions

