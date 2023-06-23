## Data from "Multi-Domain Goal-Oriented Dialogues (MultiDoGO): Strategies toward Curating and Annotating Large Scale Dialogue Data"

### Repository Structure

Under the top level ./data directory, you will find the following two sub-directories:

#### 1. unannotated: 

unannotated human to human conversations from the airline, fastfood, finance, insurance, media, and software domains. Conversations are split by domain and given in TSV format with columns: "conversationId", "turnNumber", "utteranceId", "utterance", "authorRole".

#### 2. paper_splits:

pre-processed training, development, and test splits for customer turns used to obtain intent classification and slot-labeling results in Table 7 of the paper. As in the paper, we partition these data by annotation granularity, either sentence level (located at ./data/paper_splits/splits_annotated_at_sentence_level) or turn level (located at ./data/paper_splits/splits_annotated_at_turn_level). Under each annotation granularity subdirectory, we provide splits for each domain: airline, fastfood, finance, insurance, media, and software. The splits are labeled as "train.tsv", "dev.tsv", "test.tsv" and contain the following tab separated columns: "conversationId", "turnNumber", "sentenceNumber" (only for sentence level splits), "utteranceId", "utterance", "slot-labels", and "intent". The labels in the slot-labels field are separated by spaces. In the case of multiple intents for a single input, we separate the intents with the special token \<div\>.

## License

This project is licensed under the CDLA Permissive License. Terms given in LICENSE.txt.

## Reference

For reference please cite our EMNLP-2019 paper: [Multi-Domain Goal-Oriented Dialogues (MultiDoGO): Strategies toward Curating and Annotating Large Scale Dialogue Data](https://www.aclweb.org/anthology/D19-1460/) (BibTex below)

```
@inproceedings{peskov-etal-2019-multi,
    title = "Multi-Domain Goal-Oriented Dialogues ({M}ulti{D}o{GO}): Strategies toward Curating and Annotating Large Scale Dialogue Data",
    author = "Peskov, Denis and Clarke, Nancy and Krone, Jason and Fodor, Brigi and Zhang, Yi and Youssef, Adel and Diab, Mona",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-1460",
    doi = "10.18653/v1/D19-1460",
    pages = "4526--4536",
}
```
