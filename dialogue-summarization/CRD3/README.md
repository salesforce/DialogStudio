# [ACL 2020] Storytelling with Dialogue: A *Critical Role* Dungeons and Dragons Dataset


# Overview

This paper describes the Critical Role Dungeons and Dragons Dataset (CRD3) and related analyses. Critical Role is an unscripted, live-streamed show where a fixed group of people play Dungeons and Dragons, an open-ended role-playing game. The dataset is collected from 159 Critical Role episodes transcribed to text dialogues, consisting of 398,682 turns. It also includes corresponding abstractive summaries collected from the Fandom wiki. The dataset is linguistically unique in that the narratives are generated entirely through player collaboration and spoken interaction. For each dialogue, there are a large number of turns, multiple abstractive summaries with varying levels of detail, and semantic ties to the previous dialogues. In addition, we provide a data augmentation method that produces 34,243 summary-dialogue chunk pairs to support current neural ML approaches, and we provide an abstractive summarization benchmark and evaluation.

Here is an example of a summary chunk aligned to a section in the dialogue, as shown in the paper:

<img src="images/figure 1.PNG" width="35%">

Here is a comparison of the dataset to similar datasets, as shown in the paper:

<img src="images/table 1.PNG" width="75%">

## Repo Structure
    .
    ├── baseline                  # The baseline folder will feature a frozen set of data and code to reproduce statistics and metrics calculated in the paper
    │   ├── data                  # Folder structure for data same as below
    │   │   └── ...
    │   └── ...
    ├── data                      # All of the data (including future updates) for the CRD3 Dataset will be available in the data folder
    │   ├── aligned data          # The final summary-dialogue chunk aligned data
    │   │   ├── c=2               # Alignments using summary chunk sizes of size 2
    │   │   ├── c=3               # ...of size 3
    │   │   ├── c=4               # ...of size 4
    │   │   ├── c=...n            # ...of size n if more sizes are added
    │   │   ├── test_files        # Campaign and episode numbers for files belonging to test set (format ex: 'C2E031')
    │   │   ├── val_files         # Campaign and episode numbers for files belonging to validation set
    │   │   └── train_files       # Campaign and episode numbers for files belonging to training set
    │   ├── cleaned data          # The cleaned transcript data and associated episode summary (cleaning described in paper)
    │   └── raw summary data      # The raw summary data as extracted from the wiki
    └── ...
					
Source files for helping with data exploration and iteration to be added soon!

## .../data/aligned data/ Usage

Each of json files in `.../data/aligned data/c=.../*.json` has the following filename format:
```
C<campaign number>E<episode number>_<summary chunk size>_<sentence offset>.json
```
Taking `C1E001_2_1.json` as an example: this is the aligned data for campaign 1, episode 1 with chunk size 2, chunks offset by 1.
The offset is the number of sentences after sentence 1 in the summary that the chunking starts from. For example, with a summary with sentences `[A,B,C,D,E]` a chunk size of 2 and offset of 1 would produce the chunks `[BC,CD,DE]`. Each dialogue and associated summary is chunked using all chunk sizes, thus the entire dialogue summary set is currently available in chunk sizes 2, 3, and 4 as described in the paper.

To see if a json file is in test, val, or train set (as defined in the paper), simply check if  the campaign and episode substring (ex: `C1E001`) are in one of the sets.

The JSON schema for the aligned data is as follows:
```
[
  {
    "CHUNK": (str) The summary chunk after the chunking process.,
    "ALIGNMENT": {
      "CHUNK ID": (int) The chunk position for the specified chunk size and offset,
      "TURN START": (int) The turn position of the dialogue that the alignment starts at,
      "TURN END": (int) The turn position of the dialogue that the alignment ends at,
      "ALIGNMENT SCORE": (float) The alignmed score of the summary chunk pair (details in paper)
    },
    "TURNS": [
      {
        "NAMES": [
          (str) List of names associated with that specific turn. If more than name is in list, the transcribers have associated the utterances with all specified names.
        ],
        "UTTERANCES": [
         (str) List of utterances in the turn, they are broken into chunks as specified by the transcribers.
        ],
        "NUMBER": (int) Turn position in the dialogue
      }
    ]
  },
  ...
]
```
Turn numbers for the dialogues start from 0 and go to `len([dialogue turns])-1`.

Example:
```
[
  {
    "CHUNK": "Matthew Mercer introduces himself and the concept of Critical Role. The introduction videos for Grog, Keyleth, Percy, Scanlan, Tiberius, Vax'ildan, and Vex'ahlia are shown.",
    "ALIGNMENT": {
      "CHUNK ID": 0,
      "TURN START": 0,
      "TURN END": 0,
      "ALIGNMENT SCORE": 0
    },
    "TURNS": [
      {
        "NAMES": [
          "MATT"
        ],
        "UTTERANCES": [
          "Hello everyone. My name is Matthew Mercer,",
          "voice actor and Dungeon Master for Critical Role",
          "on Geek & Sundry, where I take a bunch of other",
          "voice actors and run them through a fantastical",
          "fantasy adventure through the world of Dungeons &",
          "Dragons. We play every Thursday at 7:00pm Pacific",
          "Standard Time on Geek & Sundry's Twitch stream.",
          "Please come watch us live if you have the",
          "opportunity. Back episodes and future episodes",
          "will be uploaded on the Geek & Sundry website. You",
          "can also check them out there. In the meantime,",
          "enjoy!"
        ],
        "NUMBER": 0
      }
    ]
  },
  ...
]
```

## Citation

Please cite the following paper if you want to use this dataset in your research
```
R. Rameshkumar and P. Bailey. Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset. ACL 2020.

@inproceedings{
    title = "Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset",
    author = "Rameshkumar, Revanth  and
      Bailey, Peter",
    year = "2020",
    publisher = "Association for Computational Linguistics",
    conference = "ACL"
}
```

## Acknowledgements

We thank the [Critical Role](https://critrole.com/team/) team for creating a fun, entertaining, organized,and growing set of livestreams that we used in this dataset. We also thank the [CRTranscript](https://crtranscript.tumblr.com/about) team for providing high quality transcripts of the show for the community and we thank all the contributors of the [Critical Role Wiki](https://criticalrole.fandom.com/).

## Contact and Discuss!

Feel free to reach out to us via this repo with questions or comments!




This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License][cc-by-sa]., as corresponding to the Critical Role Wiki https://criticalrole.fandom.com/
