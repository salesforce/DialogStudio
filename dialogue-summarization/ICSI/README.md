# ICSI Corpus
1. Extract [ICSI core plus contributed annotations v1.0 (ICSI_plus_NXT.zip)](https://groups.inf.ed.ac.uk/ami/icsi/download/) under `input/ICSI_plus_NXT`.

2. Run the following Python scripts to obtain respective annotations in JSON format under `output/`.

* **Manual meeting transcriptions** (dialogueActs.py). Note: you should run this script first.
<details>
  <summary>example</summary>

```json
[
   {
      "id":"Bdb001.C.dialogueact0",
      "speaker":"C",
      "starttime":"0.216",
      "startwordid":"Bdb001.w.1",
      "endtime":"5.914",
      "endwordid":"Bdb001.w.25",
      "text":"Yeah , we had a long discussion about how much w how easy we want to make it for people to bleep things out .",
      "label":"z",
      "original_label":"z",
      "attributes":{ # role, participant, adjacency, channel
         "role":"Grad",
         "participant":"me011",
         "channel":"c3"
      }
   },
  ...
]
```
`label` denotes dialogue act labels.

`participant` denotes speaker tags, their profiles (e.g., age) can be found in the `input/ICSI_plus_NXT/ICSIplus/speakers.xml`.
</details>

* **Abstractive summaries** (abstractive.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"Bdb001.s.1",
      "text":"Two main options were discussed as to the organisation of the collected data.",
      "type":"abstract"
   },
   {
      "id":"Bdb001.s.2",
      "text":"On the one hand, a bespoke XML structure that connects transcriptions and annotations (down to the word-level) to a common timeline.",
      "type":"abstract"
   },
   ...
]
```
</details>

* **Extractive summaries** (extractive.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"Bdb001.F.dialogueact37",
      "speaker":"F",
      "starttime":"68.88",
      "startwordid":"Bdb001.w.335",
      "endtime":"89.054",
      "endwordid":"Bdb001.w.376",
      "text":"and <vocalsound> the main thing that I was gonna ask people to help with today is <pause> to give input on what kinds of database format we should <pause> use in starting to link up things like word transcripts and annotations of word transcripts ,",
      "label":"s",
      "original_label":"s",
      "attributes":{
         "role":"PhD",
         "participant":"fe016",
         "channel":"cB"
      }
   },
   {
      "id":"Bdb001.C.dialogueact44",
      "speaker":"C",
      "starttime":"113.159",
      "startwordid":"Bdb001.w.461",
      "endtime":"118.67",
      "endwordid":"Bdb001.w.487",
      "text":"I mean , we <disfmarker> I sort of already have developed an XML format for this sort of stuff .",
      "label":"s",
      "original_label":"s",
      "attributes":{
         "role":"Grad",
         "participant":"me011",
         "adjacency":"1b+",
         "channel":"c3"
      }
   },
   ...
]
```
</details>

* **Abstractive-Extractive linkings / Abstractive communities** (summlink.py)
<details>
  <summary>example</summary>

```json
[
   {
      "abstractive":{
         "id":"Bdb001.s.1",
         "text":"Two main options were discussed as to the organisation of the collected data.",
         "type":"abstract"
      },
      "extractive":[
         {
            "id":"Bdb001.F.dialogueact37",
            "speaker":"F",
            "starttime":"68.88",
            "startwordid":"Bdb001.w.335",
            "endtime":"89.054",
            "endwordid":"Bdb001.w.376",
            "text":"and <vocalsound> the main thing that I was gonna ask people to help with today is <pause> to give input on what kinds of database format we should <pause> use in starting to link up things like word transcripts and annotations of word transcripts ,",
            "label":"s",
            "original_label":"s",
            "attributes":{
               "role":"PhD",
               "participant":"fe016",
               "channel":"cB"
            }
         },
         {
            "id":"Bdb001.C.dialogueact404",
            "speaker":"C",
            "starttime":"790.456",
            "startwordid":"Bdb001.w.3,414",
            "endtime":"791.666",
            "endwordid":"Bdb001.w.3,422",
            "text":"Th - there are sort of two choices .",
            "label":"s",
            "original_label":"s",
            "attributes":{
               "role":"Grad",
               "participant":"me011",
               "channel":"c3"
            }
         }
      ]
   },
  ...
]
```
</details>

For more details of these annotations, please refer to the [annotation guidelines](https://groups.inf.ed.ac.uk/ami/corpus/guidelines.shtml) or the citations in below.

# Training, Validation, and Test Sets
For the AMI corpus, multiple official suggestions exist [here](https://groups.inf.ed.ac.uk/ami/corpus/datasets.shtml), "scenario-only partition of meetings" in below is the most adopted one in the litterature:
```python
def flatten(list_of_list):
    return [item for sublist in list_of_list for item in sublist]
 
ami_train = ['ES2002', 'ES2005', 'ES2006', 'ES2007', 'ES2008', 'ES2009', 'ES2010', 'ES2012', 'ES2013', 'ES2015', 'ES2016', 'IS1000', 'IS1001', 'IS1002', 'IS1003', 'IS1004', 'IS1005', 'IS1006', 'IS1007', 'TS3005', 'TS3008', 'TS3009', 'TS3010', 'TS3011', 'TS3012']
ami_train = flatten([[m_id+s_id for s_id in 'abcd'] for m_id in ami_train])
ami_train.remove('IS1002a')
ami_train.remove('IS1005d')

ami_validation = ['ES2003', 'ES2011', 'IS1008', 'TS3004', 'TS3006']
ami_validation = flatten([[m_id+s_id for s_id in 'abcd'] for m_id in ami_validation])

ami_test = ['ES2004', 'ES2014', 'IS1009', 'TS3003', 'TS3007']
ami_test = flatten([[m_id+s_id for s_id in 'abcd'] for m_id in ami_test])
```

For the ICSI corpus, the traditional test set (see citations [4]) is shown in below, training and validation sets are not specified. 
```
icsi_test = ['Bed004', 'Bed009', 'Bed016', 'Bmr005', 'Bmr019', 'Bro018']
```