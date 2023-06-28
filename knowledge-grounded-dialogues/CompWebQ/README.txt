WebComplexQuestions - v1.1.0 - 2018-06-29
----------------------------------------------

This package contains ComplexWebQuestions, a dataset that contains a large set of complex questions in natural language.

(c) 2018.  Alon Talmor, Tel-Aviv University.

LICENSE

The software is licensed under the full GPL v2+.  Please see the file LICENCE.txt

For more information, bug reports, and fixes, contact:
    Alon Talmor
    alontalmor@mail.tau.ac.il
   

CONTACT

For questions about this distribution, please contact Tel-Aviv University NLP group
at alontalmor@mail.tau.ac.il.  We provide assistance on a best-effort
basis.


QUESTION FILES

The dataset contains 34,689 examples divided into 27,734 train, 3,480 dev, 3,475 test.
each containing:

"ID”: The unique ID of the example; 
"webqsp_ID": The original WebQuestionsSP ID from which the question was constructed; 
"webqsp_question": The WebQuestionsSP Question from which the question was constructed; 
"machine_question": The artificial complex question, before paraphrasing; 
"question": The natural language complex question; 
"sparql": Freebase SPARQL query for the question. Note that the SPARQL was constructed for the machine question, the actual question after paraphrasing
may differ from the SPARQL. 
"compositionality_type": An estimation of the type of compositionally. {composition, conjunction, comparative, superlative}. The estimation has not been manually verified,
 the question after paraphrasing may differ from this estimation.
"answers": a list of answers each containing answer: the actual answer; answer_id: the Freebase answer id; aliases: freebase extracted aliases for the answer.
"created": creation time

NOTE: test set does not contain “answer” field. For test evaluation please send email to 
alontalmor@mail.tau.ac.il.


WEB SNIPPET FILES


The snippets files consist of 12,725,989 snippets each containing
PLEASE DON”T USE CHROME WHEN DOWNLOADING THESE FROM DROPBOX (THE UNZIP COULD FAIL)

"question_ID”: the ID of related question, containing at least 3 instances of the same ID (full question, split1, split2); 
"question": The natural language complex question; 
"web_query": Query sent to the search engine. 
“split_source”: 'noisy supervision split' or ‘ptrnet split’, please train on examples containing “ptrnet split” when comparing to Split+Decomp  from https://arxiv.org/abs/1807.09623
“split_type”: 'full_question' or ‘split_part1' or ‘split_part2’ please use ‘composition_answer’ in question of type composition and split_type: “split_part1” when training a reading comprehension model on splits as in Split+Decomp  from https://arxiv.org/abs/1807.09623 (in the rest of the cases use the original answer).
"web_snippets": ~100 web snippets per query. Each snippet includes Title,Snippet. They are ordered according to Google results.

With a total of
10,035,571 training set snippets
1,350,950 dev set snippets
1,339,468 test set snippets


--------------------
CHANGES
--------------------

2018-06-29      1.1     Second release
The Question file format remains the same, except that we added an additional field related to the answer of decomposed questions. Average number of snippets per question increased. See https://arxiv.org/abs/1807.09623

2018-03-01      1.0     Initial release

