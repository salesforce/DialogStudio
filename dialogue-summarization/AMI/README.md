# AMI Corpora
This is a python3 project that converts some annotations of the [AMI and ISCI Corpora](https://groups.inf.ed.ac.uk/ami/) from the original XML format into the JSON format.

The processed corpora can be directly downloaded from [here](https://drive.google.com/drive/folders/1BbmaZnzG9WrqOO-D3h211NOJePotqwQJ?usp=sharing) (last update 08/08/2022).

Click ► in below to see example and explication of each annotation.

If you want to run the code yourself, please follow the following instructions. Dependency requirements: [xmltodict](https://github.com/martinblech/xmltodict).

# AMI Corpus
1. Extract [AMI manual annotations v1.6.2 (ami_public_manual_1.6.2.zip)](http://groups.inf.ed.ac.uk/ami/download/) under `input/ami_public_manual_1.6.2`.

2. Run the following Python scripts to obtain respective annotations in JSON format under `output/`.

* **Manual meeting transcriptions** (dialogueActs.py). Note: you should run this script first.
<details>
  <summary>example</summary>

```json
[
   {
      "id":"ES2002a.B.dialog-act.dharshi.7",
      "speaker":"B",
      "starttime":"74.42",
      "startwordid":"ES2002a.B.words63",
      "endtime":"77.29",
      "endwordid":"ES2002a.B.words71",
      "text":"<vocalsound> Do you want to introduce yourself again ?",
      "label":"el.inf",
      "attributes":{ # reflexivity, addressee, comment, endtime
         "addressee":"A,D,C",
         "role":"PM",
         "participant":"FEE005"
      }
   },
  ...
]
```
`label` denotes dialogue act labels, the taxonomy can be found in the `/input/ami_public_manual_1.6.2/ontologies/da-types.xml`.

`participant` denotes speaker tags, their profiles (e.g., age) can be found in the `input/ami_public_manual_1.6.2/corpusResources/participants.xml`.
</details>

* **Abstractive summaries** (abstractive.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"ES2002a.rdhillon.s.1",
      "text":"The project manager introduced the upcoming project to the team members and then the team members participated in an exercise in which they drew their favorite animal and discussed what they liked about the animal.",
      "type":"abstract"
   },
   {
      "id":"ES2002a.rdhillon.s.2",
      "text":"The project manager talked about the project finances and selling prices.",
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
      "id":"ES2002a.B.dialog-act.dharshi.3",
      "speaker":"B",
      "starttime":"55.415",
      "startwordid":"ES2002a.B.words4",
      "endtime":"60.35",
      "endwordid":"ES2002a.B.words16",
      "text":"<vocalsound> Um well this is the kick-off meeting for our our project .",
      "label":"inf",
      "attributes":{
         "reflexivity":"true",
         "role":"PM",
         "participant":"FEE005"
      }
   },
   {
      "id":"ES2002a.B.dialog-act.dharshi.12",
      "speaker":"B",
      "starttime":"92.79",
      "startwordid":"ES2002a.B.words80",
      "endtime":"96.34",
      "endwordid":"ES2002a.B.words89",
      "text":"so we're designing a new remote control and um <disfmarker>",
      "label":"inf",
      "attributes":{
         "reflexivity":"true",
         "role":"PM",
         "participant":"FEE005"
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
...,
   {
      "abstractive":{
         "id":"ES2002a.rdhillon.s.7",
         "text":"The remote will sell for 25 Euro.",
         "type":"decisions"
      },
      "extractive":[
         {
            "id":"ES2002a.B.dialog-act.dharshi.89",
            "speaker":"B",
            "starttime":"470.01",
            "startwordid":"ES2002a.B.words636",
            "endtime":"476.53",
            "endwordid":"ES2002a.B.words654",
            "text":"Um so according to the brief um we're gonna be selling this remote control for twenty five Euro ,",
            "label":"inf",
            "attributes":{
               "role":"PM",
               "participant":"FEE005"
            }
         },
         {
            "id":"ES2002a.B.dialog-act.dharshi.129",
            "speaker":"B",
            "starttime":"681.66",
            "startwordid":"ES2002a.B.words912",
            "endtime":"687.09",
            "endwordid":"ES2002a.B.words928",
            "text":"Well twenty five Euro , I mean that's um that's about like eighteen pounds or something ,",
            "label":"inf",
            "attributes":{
               "role":"PM",
               "participant":"FEE005"
            }
         }
      ]
   },
  ...
]
```
</details>

* **Adjacency pairs** (adjacencyPairs.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"ES2002a.adjacency-pairs.dharshi.1",
      "type":"POS",
      "source":{
         "id":"ES2002a.B.dialog-act.dharshi.7",
         "speaker":"B",
         "starttime":"74.42",
         "startwordid":"ES2002a.B.words63",
         "endtime":"77.29",
         "endwordid":"ES2002a.B.words71",
         "text":"<vocalsound> Do you want to introduce yourself again ?",
         "label":"el.inf",
         "attributes":{
            "addressee":"A,D,C",
            "role":"PM",
            "participant":"FEE005"
         }
      },
      "target":{
         "id":"ES2002a.A.dialog-act.dharshi.1",
         "speaker":"A",
         "starttime":"77.44",
         "startwordid":"ES2002a.A.words0",
         "endtime":"80.87",
         "endwordid":"ES2002a.A.words12",
         "text":"Hi , I'm David and I'm supposed to be an industrial designer .",
         "label":"inf",
         "attributes":{
            "role":"ID",
            "participant":"MEE006"
         }
      }
   },
  ...
]
```
</details>

* **Topic segmentation** (topic.py)
<details>
  <summary>example</summary>

```json
[
  {
    "id": "ES2003d.topic.rdhillon.6",
    "topic": "evaluation of prototype(s)",
    "description": "None",
    "dialogueacts": [
      {
        "id": "ES2003d.C.dialog-act.vkaraisk.8",
        "speaker": "C",
        "starttime": "329.94",
        "startwordid": "ES2003d.C.words23",
        "endtime": "336.2",
        "endwordid": "ES2003d.C.words39",
        "text": "Basic point uh have a list of criteria that we need to rate the prototype by .",
        "aspect": "inf",
        "attributes": {
          "reflexivity": "true",
          "role": "ME",
          "participant":"MEE012"
        }
      },
      ... # more DAs
    ],
    "subtopics": [
      {
        "id": "ES2003d.topic.rdhillon.7",
        "topic": "how to find when misplaced",
        "description": "None",
        "dialogueacts": [
          {
            "id": "ES2003d.C.dialog-act.vkaraisk.34",
            "speaker": "C",
            "starttime": "421.78",
            "startwordid": "ES2003d.C.words229",
            "endtime": "423.51",
            "endwordid": "ES2003d.C.words230",
            "text": "So um",
            "aspect": "stl",
            "attributes": {
              "role": "ME",
              "participant":"MEE012"
            }
          },
          ... # more DAs
        ]
      },
      {
        "id": "ES2003d.topic.rdhillon.8",
        "topic": "agenda/equipment issues",
        "description": "None",
        "dialogueacts": [
          {
            "id": "ES2003d.B.dialog-act.vkaraisk.44",
            "speaker": "B",
            "starttime": "516.29",
            "startwordid": "ES2003d.B.words301",
            "endtime": "521.8",
            "endwordid": "ES2003d.B.words317",
            "text": "just before we go through all of the steps here , um well what we'll do is",
            "aspect": "fra",
            "attributes": {
              "role": "PM",
              "participant":"MEE009"
            }
          },
          ... # more DAs
        ]
      },
      ... # more subtopics
    ]
  },
  ... # more topics
]
```
</details>

For more details of these annotations, please refer to the [annotation guidelines](https://groups.inf.ed.ac.uk/ami/corpus/guidelines.shtml) or the citations in below.
