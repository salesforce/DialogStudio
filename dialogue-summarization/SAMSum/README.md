## Dataset Summary
The SAMSum dataset contains about 16k messenger-like conversations with summaries. Conversations were created and written down by linguists fluent in English. Linguists were asked to create conversations similar to those they write on a daily basis, reflecting the proportion of topics of their real-life messenger convesations. The style and register are diversified - conversations could be informal, semi-formal or formal, they may contain slang words, emoticons and typos. Then, the conversations were annotated with summaries. It was assumed that summaries should be a concise brief of what people talked about in the conversation in third person. The SAMSum dataset was prepared by Samsung R&D Institute Poland and is distributed for research purposes.


## Data Instances

The created dataset is made of 16369 conversations distributed uniformly into 4 groups based on the number of utterances in con- versations: 3-6, 7-12, 13-18 and 19-30. Each utterance contains the name of the speaker. Most conversations consist of dialogues between two interlocutors (about 75% of all conversations), the rest is between three or more people

The first instance in the training set: {'id': '13818513', 'summary': 'Amanda baked cookies and will bring Jerry some tomorrow.', 'dialogue': "Amanda: I baked cookies. Do you want some?\r\nJerry: Sure!\r\nAmanda: I'll bring you tomorrow :-)"}

## Data Fields

- dialogue: text of dialogue.
- summary: human written summary of the dialogue.
- id: unique id of an example.

## Data Splits

- train: 14732
- val: 818
- test: 819

## License 
non-commercial licence: CC BY-NC-ND 4.0