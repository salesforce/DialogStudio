# OpenDialKG 

OpenDialKG is a dataset of conversations between two crowdsourcing agents engaging in a dialog about a given topic. Each dialog turn is paired with its corresponding “KG paths” that weave together the KG entities and relations that are mentioned in the dialog. More details can be found in the following paper:

Seungwhan Moon, Pararth Shah, Anuj Kumar, Rajen Subba. ["OpenDialKG: Explainable Conversational Reasoning with Attention-based Walks over Knowledge Graphs"](https://www.aclweb.org/anthology/P19-1081.pdf), ACL (2019).

## Data Format

The dataset release includes two parts: (1) the Dialog-KG Path Parallel Corpus where each dialog turn is paired with KG paths that connect its previous turn (annotated by chat participants themselves), and (2) the base knowledge graph used in both the dialog collection and in the experiments, which is a subset of the [Freebase Easy data](http://freebase-easy.cs.uni-freiburg.de/dump/). The data are made available in the following files:
```
[Dialog-KG Parallel Corpus]
- ./data/opendialkg.csv

[KG]
- ./data/opendialkg_entities.txt
- ./data/opendialkg_relations.txt
- ./data/opendialkg_triples.txt 
```

The Dialog-KG Parallel Corpus (`./data/opendialkg.csv`) is formatted as a csv file, where columns are: `Messages, User Rating, Assistant Rating`. Each row refers to a dialog session, which is a JSON-formatted `<list>` of each action formatted as follows::
```
{
	"type": // <str> indicating whether it's a message ("chat") or a KG walk selection action ("action")
	"sender": // <str> indicating indicating whether it is sent by "user" or "assistant"
	"message" (Optional): // <str> raw utterance (for "type": "chat"),
	"metadata" (Optional): {
		"path": [
			<float> // path score,
			<list> // of KG triples (subject, relation, object) that make up the path,
			<str> // rendering of the path
		]
	} // end of KG path JSON (if available)
}. ... // end of each action JSON
```

Note that the path annotation refers to the connection of two adjacent turns on the conceptual level. Given `utterance_1`, `utterance_2`, and their annotated entity path `A -> B -> C` that connect `utterance_1` and `utterance_2`, Entity `A` is assumed to be mentioned in `utterance_1`, and `C` to be mentioned in `utterance_2`. Entity `B` doesn't necessarily have to be mentioned since it is an intermediate step in the path. Note also that it is a paraphrased dataset, thus each mention is not enforced to have an exact surface match with its corresponding entity in the knowledge graph. After pre-processing and quality reviews we release the 13,802 dialog sessions (91,209 turns) across two tasks (Chit-chat and Recommendations) and four domains (movie, book, sports, and music).

All bi-directional KG triples used in the dataset collection and in the experiments (100,813 entities, 1358 relations, 1,190,658 triples) are included in `./data/opendialkg_triples.txt`, formatted as line-separated triples with tab-separated entities and relations:
```
subject \t relation \t object \n
...
```

All entities and relations are also listed in `./data/opendialkg_entities.txt` and `./data/opendialkg_relations.txt`, respectively. The prefix `~` in `opendialkg_relations.txt` refers to reverse relations.

## Reference

To cite this work please use:
```
@InProceedings{Moon2019opendialkg,
author = {Seungwhan Moon and Pararth Shah and Anuj Kumar and Rajen Subba},
title = {OpenDialKG: Explainable Conversational Reasoning with Attention-based Walks over Knowledge Graphs},
booktitle = {Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
month = {July},
year = {2019},
}
```

## License
OpenDialKG is released under [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/legalcode), see [LICENSE](LICENSE) for details.