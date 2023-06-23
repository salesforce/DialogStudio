# CaSiNo

This repository contains the dataset and the PyTorch code for **'CaSiNo: A Corpus of Campsite Negotiation Dialogues for Automatic Negotiation Systems'**.

We provide a novel dataset (referred to as CaSiNo) of 1030 negotiation dialogues. Two participants take the role of campsite neighbors and negotiate for *Food*, *Water*, and *Firewood* packages, based on their individual preferences and requirements. This design keeps the task tractable, while still facilitating linguistically rich and personal conversations.

# Repository Structure

**data**: The complete CaSiNo dataset along with the strategy annotations.\
**strategy_prediction**: Code for strategy prediction in a multi-task learning setup.

# Each Dialogue in the Dataset

**Participant Info**
* Demographics (Age, Gender, Ethnicity, Education)
* Personality attributes (SVO and Big-5)
* Preference order
* Arguments for needing or not needing a specific item

**Negotiation Dialogue**
* Alternating conversation between two participants
* 11.6 utterances on average
* Includes the use of four emoticons: Joy, Sadness, Anger, Surprise

**Negotiation Outcomes**
* Points scored
* Satisfaction (How satisfied are you with the negotiation outcome?)
* Opponent Likeness (How much do you like your opponent?)

**Strategy Annotations**
* Utterance-level annotations for various negotiation strategies used by the participants
* Available for 396 dialogues (4615 utterances)

# References

If you use data or code in this repository, please cite our paper: 
```
@inproceedings{chawla2021casino,
  title={CaSiNo: A Corpus of Campsite Negotiation Dialogues for Automatic Negotiation Systems},
  author={Chawla, Kushal and Ramirez, Jaysa and Clever, Rene and Lucas, Gale and May, Jonathan and Gratch, Jonathan},
  booktitle={Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies},
  pages={3167--3185},
  year={2021}
}
```

# LICENSE

Please refer to the LICENSE file in the root directory for more details.
