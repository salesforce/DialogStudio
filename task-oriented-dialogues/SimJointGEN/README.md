## Simulator Generated Dataset (sim-GEN)

This directory contains an expanded set of dialogues generated via dialogue
self-play between a user simulator and a system agent, as follows:

-   The dialogues collected using the M2M framework for the movie ticket booking
    task (sim-M) are used as a seed set to form a crowd-sourced corpus of
    natural language utterances for the user and the system agents.
-   Subsequently, many more dialogue outlines are generated using self-play
    between the simulated user and system agent.
-   The dialogue outlines are converted to natural language dialogues by
    replacing each dialogue act in the outline with an utterance sampled from
    the set of crowd-sourced utterances collected with M2M.

In this manner, we can generate an arbitrarily large number of dialogue outlines
and convert them automatically to natural language dialogues without any
additional crowd-sourcing step. Although the diversity of natural language in
the dataset does not increase, the number of unique dialogue states present in
the dataset will increase since a larger variety of dialogue outlines will be
available in the expanded dataset.

This dataset was used for experiments reported in [this
paper](https://arxiv.org/abs/1804.06512). Please cite the paper if you use or
discuss sim-GEN in your work:

```shell
@article{liu2018dialogue,
  title={Dialogue Learning with Human Teaching and Feedback in End-to-End Trainable Task-Oriented Dialogue Systems},
  author={Liu, Bing and Tur, Gokhan and Hakkani-Tur, Dilek and Shah, Pararth and Heck, Larry},
  journal={NAACL},
  year={2018}
}
```

## Data format

The data splits are made available as a .zip file containing dialogues in JSON
format. Each dialogue object contains the following fields:

*   **dialogue\_id** - *string* unique identifier for each dialogue.
*   **turns** - *list* of turn objects:
    *   **system\_acts** - *list* of system dialogue acts for this system turn:
        *   **name** - *string* system act name
        *   **slot\_values** - *optional dictionary* mapping slot names to
            values
    *   **system\_utterance** - *string* natural language utterance
        corresponding to the system acts for this turn
    *   **user\_utterance** - *string* natural language user utterance following
        the system utterance in this turn
    *   **dialogue\_state** - *dictionary* ground truth slot-value mapping after
        the user utterance
    *   **database\_state** - database results based on current dialogue state:
        *   **scores** - *list* of scores, between 0.0 and 1.0, of top 5
            database results. 1.0 means matches all constraints and 0.0 means no
            match
        *   **has\_more\_results** - *boolean* whether backend has more matching
            results
        *   **has\_no\_results** - *boolean* whether backend has no matching
            results

An additional file **db.json** is provided which contains the set of values for
each slot.

Note: The date values in the dataset are normalized as the constants,
"base_date_plus_X", for X from 0 to 6. X=0 corresponds to the current date (i.e.
'today'), X=1 is 'tomorrow', etc. This is done to allow handling of relative
references to dates (e.g. 'this weekend', 'next Wednesday', etc). The parsing of
such phrases should be done as a separate pre-processing step.
