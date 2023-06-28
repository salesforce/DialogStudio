Microsoft Research Sequential Question Answering (SQA) Dataset

-------------------------------------------------------------------------------------------------------
Contact Persons:
	Scott Wen-tau Yih        scottyih@microsoft.com
	Mohit Iyyer              m.iyyer@gmail.com
	Ming-Wei Chang           minchang@microsoft.com
-------------------------------------------------------------------------------------------------------

The SQA dataset was created to explore the task of answering sequences of inter-related questions on HTML tables. A detailed description of the dataset, as well as some experimental studies, can be found in the following paper: 

Mohit Iyyer, Wen-tau Yih, Ming-Wei Chang.
"Answering Complicated Question Intents Expressed in Decomposed Question Sequences."
arXiv preprint arXiv:1611.01242
https://arxiv.org/abs/1611.01242

-------------------------------------------------------------------------------------------------------

Version 1.0: November 9, 2016

-------------------------------------------------------------------------------------------------------
SUMMARY

Recent work in semantic parsing for question answering has focused on long and complicated questions, many of which would seem unnatural if asked in a normal conversation between two humans. In an effort to explore a conversational QA setting, we present a more realistic task: answering sequences of simple but inter-related questions.

We created SQA by asking crowdsourced workers to decompose 2,022 questions from WikiTableQuestions (WTQ)*, which contains highly-compositional questions about tables from Wikipedia. We had three workers decompose each WTQ question, resulting in a dataset of 6,066 sequences that contain 17,553 questions in total. Each question is also associated with answers in the form of cell locations in the tables.

* Panupong Pasupat, Percy Liang. "Compositional Semantic Parsing on Semi-Structured Tables" ACL-2015.
  http://www-nlp.stanford.edu/software/sempre/wikitable/

-------------------------------------------------------------------------------------------------------
LIST OF FILES

train.tsv       -- Training question sequences
test.tsv        -- Testing question sequences
table_csv       -- All the tables used in the questions (originally from WTQ)
random-split-*  -- Five different 80-20 training/dev splits based on training.tsv.  
                   The splits follow those provided in WTQ.
eval.py         -- The evaluation script in Python
rndfake.tsv     -- A fake output file for demonstrating the usage of eval.py
license.docx    -- License
readme.txt      -- This file

-------------------------------------------------------------------------------------------------------
DATA FORMAT

train.tsv, test.tsv, random-split-*
    -- id: question sequence id (the id is consistent with those in WTQ)
	-- annotator: 0, 1, 2 (the 3 annotators who annotated the question intent)
	-- position: the position of the question in the sequence
	-- question: the question given by the annotator
	-- table_file: the associated table
	-- answer_coordinates: the table cell coordinates of the answers (0-based, where 0 is the first row after the table header)
	-- answer_text: the content of the answer cells
	Note that some text fields may contain Tab or LF characters and thus start with quotes. 
	It is recommended to use a CSV parser like the Python CSV package to process the data.
	
table_csv (from WTQ; below is the original description in the WTQ release)
    -- Comma-separated table (The first row is treated as the column header)
       The escaped characters include:
         double quote (`"` => `\"`) and backslash (`\` => `\\`).
         Newlines are represented as quoted line breaks.
		 
rndfake.tsv
    -- A fake output file for the test questions; fields are: id, annotator, position, answer_coordinates

-------------------------------------------------------------------------------------------------------
EVALUATION

$ python eval.py test.tsv rndfake.tsv
Sequence Accuracy = 14.83% (152/1025)
Answer Accuracy =   50.33% (1516/3012)

-------------------------------------------------------------------------------------------------------
