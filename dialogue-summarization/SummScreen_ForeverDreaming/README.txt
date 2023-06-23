Each line in the files is a dictionary object with three keys: "Recap" (i.e., short summary), "Transcript", and "filename", where "filename" contains information about show title, season and episode number (e.g., "Alias_01x02.json" suggests the 2nd episode in the 1st season for the show "Alias"). "*_anonymize_*.json" contains the anonymized instances. The recaps and transcripts are already tokenized using spaCy and segmented into subword units (using https://github.com/rsennrich/subword-nmt).

More details are in our paper:
SummScreen: A Dataset for Abstractive Screenplay Summarization
Mingda Chen, Zewei Chu, Sam Wiseman, Kevin Gimpel
https://arxiv.org/abs/2104.07091

Mingda Chen
04/20/2021
