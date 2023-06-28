### Conversational Recommendation Dialogues

Conversational Recommendation Dialogues follow same format as task oriented dialogues. Below is the copy of ReadME from task oriented dialogues:

Below is a general format for task oriented dialogues:

```js
{
    "dataset_name--train/val/test--dialog_id": {
        "original dialog id": str,
        "dialog index": int,
        "original dialog info": dict,
        "log": [
            {
                "turn id": int,
                "user utterance": str,
                "system response": str,
                "dialog history": str,
                "original user side information": dict,
                "original system side information": dict,
                "dst": str,
                "dst accumulated": str
            },
         	...
        ],
        "external knowledge non-flat": {
            "metadata": dict,
            "slots and values": dict
            "intents": dict,
            ...
        },
        "external knowledge": str,
        "intent knowledge": str,
        "prompt": [
            "This is a bot helping users to get navigation. Given the dialog context and external database, please generate a relevant system response for the user.",
            ...
        ]
    },
    ...
}
```

In general, datasets have the "external knowledge non-flat" and "external knowledge"  in the whole dialogue level. There are also some datasets where every turn in "log" has own "external knowledge non-flat" and "external knowledge". 

Here are datasets with turn-level "external knowledge": 
```
'SimJointGEN', 'BiTOD', 'OpenDialKG', 'SimJointMovie', 'MS-DC', 'STAR', 'SimJointRestaurant', 'Taskmaster1', 'Taskmaster2', 'Taskmaster3'
```
And below is a general format for such datasets:
```js
{
    "dataset_name--train/val/test--dialog_id": {
        "original dialog id": str,
        "dialog index": int,
        "original dialog info": dict,
        "log": [
            {
                "turn id": int,
                "user utterance": str,
                "system response": str,
                "dialog history": str,
                "original user side information": dict,
                "original system side information": dict,
                "dst": str,
                "dst accumulated": str
                "external knowledge non-flat": list,
                "external knowledge": str,
            },
         	...
        ]
        "prompt": [
            "This is a bot helping users to get navigation. Given the dialog context and external database, please generate a relevant system response for the user.",
            ...
        ]
    },
    ...
}
```
Please refer to each dataset folder for more details.
