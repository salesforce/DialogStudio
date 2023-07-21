## A dataset for answering complex questions that require reasoning over multiple web snippets.

ComplexWebQuestions is a new dataset that contains a large set of complex questions in natural language, and can be used in multiple ways:

By interacting with a search engine, which is the focus of our paper (Talmor and Berant, 2018);

As a reading comprehension task: we release 12,725,989 web snippets that are relevant for the questions, and were collected during the development of our model; 

As a semantic parsing task: each question is paired with a SPARQL query that can be executed against Freebase to retrieve the answer.


### Citation


```
@inproceedings{talmor18compwebq,
  author = {A. Talmor and J. Berant},
  booktitle = {North American Association for Computational Linguistics (NAACL)},
  title = {The Web as a Knowledge-base for Answering Complex Questions},
  year = {2018},
}
```