# Multi-domain Coreference (MuDoCo) dataset

This is a dataset of authored short dialogs between an imagined user and an imagined conversational assistant. 
[Our LREC 2020 paper](http://www.lrec-conf.org/proceedings/lrec2020/pdf/2020.lrec-1.13.pdf) has more details
about the structure of the data and annotations.

## License
Please see the LICENSE.md file for details about use, copying and redistribution.

## Data format
The data itself is represented in JSON format, one file per domain (calling, messaging, music, news, reminders,
and weather). The JSON files are compressed to save space, with all whitespace removed.

## Data structure 

At the top level is the domain name, then each dialog (or "thread") is listed by its unique identifier. Each
dialog is tagged by split, either 'train', 'test', or 'eval'.
Within each dialog the turns are listed individually, with the turn's number, text, and any related annotations
contained within the turn itself. The named entity, reference, and link annotations all contain the text of 
the mention along with the start and end character indices of the mention and the turn number where the
mention occurrs (for redundancy). 

An example from dialog `0000f044-7e8e-c435-23f2-339d1432d27c` in the 'calling' domain:
```json
{
    "domain": "calling",
    "dialogs": {
        "0000f044-7e8e-c435-23f2-339d1432d27c": {
            "split": "test",
            "turns": [
                {
                    "number": 1,
                    "utterance": "Did Paula call me ?",
                    "named_entities": {
                        "person": [
                            {
                                "turn_id": 1,
                                "span": {
                                    "start": 4,
                                    "end": 9
                                },
                                "text": "Paula"
                            },
                            {
                                "turn_id": 1,
                                "span": {
                                    "start": 15,
                                    "end": 17
                                },
                                "text": "me"
                            }
                        ]
                    },
                    "references": {
                        "personal_pronoun": [
                            {
                                "turn_id": 1,
                                "span": {
                                    "start": 15,
                                    "end": 17
                                },
                                "text": "me"
                            }
                        ]
                    },
                    "links": []
                },
                {
                    "number": 2,
                    "utterance": "No sir , she didn't .",
                    "named_entities": {
                        "person": [
                            {
                                "turn_id": 2,
                                "span": {
                                    "start": 9,
                                    "end": 12
                                },
                                "text": "she"
                            }
                        ]
                    },
                    "references": {
                        "personal_pronoun": [
                            {
                                "turn_id": 2,
                                "span": {
                                    "start": 9,
                                    "end": 12
                                },
                                "text": "she"
                            }
                        ]
                    },
                    "links": [
                        [
                            {
                                "turn_id": 1,
                                "span": {
                                    "start": 4,
                                    "end": 9
                                },
                                "text": "Paula"
                            },
                            {
                                "turn_id": 2,
                                "span": {
                                    "start": 9,
                                    "end": 12
                                },
                                "text": "she"
                            }
                        ]
                    ]
                },
                {
                    "number": 3,
                    "utterance": "Just thought I'd check .",
                    "named_entities": {
                        "person": [
                            {
                                "turn_id": 3,
                                "span": {
                                    "start": 13,
                                    "end": 14
                                },
                                "text": "I"
                            }
                        ]
                    },
                    "references": {
                        "personal_pronoun": [
                            {
                                "turn_id": 3,
                                "span": {
                                    "start": 13,
                                    "end": 14
                                },
                                "text": "I"
                            }
                        ]
                    },
                    "links": [
                        [
                            {
                                "turn_id": 1,
                                "span": {
                                    "start": 15,
                                    "end": 17
                                },
                                "text": "me"
                            },
                            {
                                "turn_id": 3,
                                "span": {
                                    "start": 13,
                                    "end": 14
                                },
                                "text": "I"
                            }
                        ]
                    ]
                }
            ]
        }
    }
}

```

 
