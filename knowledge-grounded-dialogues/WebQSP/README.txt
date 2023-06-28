List of files:

	ReadMe.txt - This file
	doc/WebQSP.pdf - The main document that details the usage, format and other specifics about this WebQuestionsSP dataset
	doc/LabelingInstructions.pdf - The annotation guidelines
	data/WebQSP.train.json - The training set of the primary dataset
	data/WebQSP.test.json - The testing set of the primary dataset
	data/WebQSP.train.partial.json - Partial annotations to bad or descriptive questions in the original training set
	data/WebQSP.test.partial.json - Partial annotations to bad or descriptive questions in the original testing set
	eval/eval.py - The evaluation script in Python
	eval/Pred.sem.json - Output of the STAGG system trained using the full semantic parses

For evaluation, please use "WebQSP.test.json".  Detailed descriptions of the roles of WebQSP.[train|test].[partial|_].json can be found in "WebQSP.pdf".
	
Usage of the evaluation script: 
	python eval.py goldData predAnswers

	$ python eval/eval.py data/WebQSP.test.json eval/Pred.sem.json
	Number of questions: 1639
	Average precision over questions: 0.709
	Average recall over questions: 0.803
	Average f1 over questions (accuracy): 0.717
	F1 of average recall and average precision: 0.753
	True accuracy (ratio of questions answered exactly correctly): 0.639
