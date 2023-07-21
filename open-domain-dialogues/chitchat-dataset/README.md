# chitchat-dataset

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chitchat_dataset)](https://pypi.org/project/chitchat-dataset/)
[![PyPI](https://img.shields.io/pypi/v/chitchat_dataset)](https://pypi.org/project/chitchat-dataset/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/chitchat_dataset)](https://pypi.org/project/chitchat-dataset/)

[![CI](https://github.com/BYU-PCCL/chitchat-dataset/workflows/CI/badge.svg)](https://github.com/BYU-PCCL/chitchat-dataset/actions?query=workflow%3ACI)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Open-domain conversational dataset from the BYU
[Perception, Control & Cognition] lab's [Chit-Chat Challenge].

## stats

- 7,168 conversations
- 258,145 utterances
- 1,315 unique participants

## format

The [dataset] is a mapping from conversation [UUID] to a conversation:

```json
{
  "prompt": "What's the most interesting thing you've learned recently?",
  "ratings": { "witty": "1", "int": 5, "upbeat": 5 },
  "start": "2018-04-20T01:57:41",
  "messages": [
    [
      {
        "text": "Hello",
        "timestamp": "2018-04-19T19:57:51",
        "sender": "22578ac2-6317-44d5-8052-0a59076e0b96"
      }
    ],
    [
      {
        "text": "I learned that the Queen of England's last corgi died",
        "timestamp": "2018-04-19T19:58:14",
        "sender": "bebad07e-15df-48c3-a04f-67db828503e3"
      }
    ],
    [
      {
        "text": "Wow that sounds so sad",
        "timestamp": "2018-04-19T19:58:18",
        "sender": "22578ac2-6317-44d5-8052-0a59076e0b96"
      },
      {
        "text": "was it a cardigan welsh corgi",
        "timestamp": "2018-04-19T19:58:22",
        "sender": "22578ac2-6317-44d5-8052-0a59076e0b96"
      },
      {
        "text": "?",
        "timestamp": "2018-04-19T19:58:24",
        "sender": "22578ac2-6317-44d5-8052-0a59076e0b96"
      }
    ]
  ]
}
```

This makes it convenient to represent multi-message conversational turns etc., preserving the structure/flow of the conversation.

# how to cite

If you extend or use this work, please cite the paper where it was introduced:

```
@article{myers2020conversational,
  title={Conversational Scaffolding: An Analogy-Based Approach to Response Prioritization in Open-Domain Dialogs},
  author={Myers, Will and Etchart, Tyler and Fulda, Nancy},
  year={2020}
}
```