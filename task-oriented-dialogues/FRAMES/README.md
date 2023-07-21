# FRAMES-Corpus
Utilities for Processing the [FRAMES Corpus](https://www.aclweb.org/anthology/W17-5526/)
available [here](https://www.microsoft.com/en-us/research/project/frames-dataset/).
Frames is meant to encourage research towards conversational agents which can support decision-making in complex settings,
 in this case – booking a vacation including flights and a hotel.
The utilities process the original transcripts into plain text or json formats.

## Scripts
frames_to_json.py script processes the dialogues from the original format into .json files using the format
outlined below. Each dialogue set (train and test) is output as a separate .json file.
This format is intended to facilitate annotation of the dialogue using the 
[Conversation Analysis Modelling Schema](https://nathanduran.github.io/Conversation-Analysis-Modelling-Schema/).

frames_to_text.py processes the dialogues from the .json format into plain text files,
with one line per-utterance, using the format outlined below.
Setting the *utterance_only* flag to true will remove the speaker label from the output text files.

frames_utilities.py script contains various helper functions for loading/saving and processing the data.

## Data Format
The original slots and dialogue scenario has been preserved to maintain compatibility with the original dataset.
Where no dialogue act is present it is replaces with 'null'.
By default utterances are written one per line in the format *Speaker* | *Utterance Text* | *Dialogue Act Tag*.
This can be changed to only output the utterance text by setting the utterance_only_flag = True.

### Example Text Format
USR|I'd like to book a trip to Atlantis from Caprica on Saturday, August 13, 2016 for 8 adults.|inform

USR|I have a tight budget of 1700.|inform

SYS|Hi...I checked a few options for you, and unfortunately, we do not currently have any trips that meet this criteria.|sorry

SYS|Would you like to book an alternate travel option?|sorry

### Example JSON Format
The following is an example of the JSON format for the FRAMES corpus.

```json
    {
        "dataset": "dataset_name",
        "num_dialogues": 1,
        "dialogues": [
            {
                "dialogue_id": "dataset_name_1",
                "num_utterances": 2,
                "utterances": [
                    {
                        "speaker": "A",
                        "text": "Utterance 1 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label"
                    },
                    {
                        "speaker": "B",
                        "text": "Utterance 2 text.",
                        "ap_label": "AP-Label",
                        "da_label": "DA-Label",
                        "slots": { //Optional
                            "slot_name": "slot_value"
                        }
                    }
                ],
                "scenario": { //Optional
                    "db_id": "1",
                    "db_type": "i.e booking",
                    "task": "i.e book",
                    "items": []
                }
            }
        ]
    }
```
## Licensing and Attribution
The original paper for the FRAMES corpus: Asri, L. El, Schulz, H., Sharma, S., et al., (2017) [Frames: A Corpus for Adding Memory to Goal-Oriented Dialogue Systems](https://www.aclweb.org/anthology/W17-5526/).

The code within this repository is distributed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).